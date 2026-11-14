#!/usr/bin/env python3
"""Validate foundational documentation and repository-local Markdown links.

This checks playbook documentation, not future generated project behavior.
No third-party packages or GitHub environment variables are needed.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/engineering_change.yml",
    ".github/ISSUE_TEMPLATE/defect_report.yml",
    ".github/workflows/validate-foundation.yml",
    "docs/README.md",
    "docs/standards/engineering-principles.md",
    "docs/governance/standards.md",
    "docs/governance/repository-organization.md",
    "docs/architecture/template-model.md",
    "docs/decisions/README.md",
    "docs/decisions/0001-playbook-boundaries.md",
    "examples/dotnet-binary-tools.md",
)
INLINE_LINK_START = re.compile(r"(?<!\\)!?\[[^\]\n]*\]\(")
REFERENCE_LINK = re.compile(r"^\s{0,3}\[([^\]\n]+)\]:\s*(<[^>]+>|\S+)")
REFERENCE_USAGE = re.compile(r"(?<!\\)!?\[([^\]\n]+)\]\[([^\]\n]*)\]")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+).*?\1")
MARKDOWN_ESCAPES = re.compile(r"\\([\\`*_{}\[\]()#+\-.!])")


def visible_markdown(source: str) -> list[tuple[int, str]]:
    """Yield non-fenced lines with inline code removed."""
    visible = []
    fence_char = ""
    fence_length = 0
    for line_number, line in enumerate(source.splitlines(), start=1):
        match = FENCE.match(line)
        if fence_char:
            if match and match.group(1)[0] == fence_char and len(match.group(1)) >= fence_length:
                fence_char = ""
            continue
        if match:
            fence_char = match.group(1)[0]
            fence_length = len(match.group(1))
            continue
        visible.append((line_number, INLINE_CODE.sub("", line)))
    return visible


def unescape_markdown(value: str) -> str:
    """Decode backslash escapes allowed in Markdown link destinations."""
    return MARKDOWN_ESCAPES.sub(r"\1", value)


def inline_destination(line: str, start: int) -> str | None:
    """Read one link destination, allowing balanced and escaped parentheses.

    This is a focused link scanner, not a complete GitHub Flavored Markdown parser.
    """
    cursor = start
    while cursor < len(line) and line[cursor] in " \t":
        cursor += 1

    if cursor < len(line) and line[cursor] == "<":
        cursor += 1
        destination_start = cursor
        while cursor < len(line):
            if line[cursor] == "\\" and cursor + 1 < len(line):
                cursor += 2
            elif line[cursor] == ">":
                break
            else:
                cursor += 1
        if cursor == len(line):
            return None
        destination = line[destination_start:cursor]
        cursor += 1
    else:
        destination_start = cursor
        depth = 0
        while cursor < len(line):
            character = line[cursor]
            if character == "\\" and cursor + 1 < len(line):
                cursor += 2
            elif character == "(":
                depth += 1
                cursor += 1
            elif character == ")":
                if depth == 0:
                    break
                depth -= 1
                cursor += 1
            elif character.isspace() and depth == 0:
                break
            else:
                cursor += 1
        if depth:
            return None
        destination = line[destination_start:cursor]

    # A link may end here or contain an optional title before the closing ')'.
    if cursor < len(line) and line[cursor] == ")":
        return unescape_markdown(destination)
    if cursor >= len(line) or not line[cursor].isspace():
        return None
    remainder = line[cursor:].strip()
    if remainder.startswith(")") or (
        len(remainder) >= 3
        and remainder[0] in ('"', "'")
        and remainder[-1] == ")"
        and remainder[-2] == remainder[0]
    ):
        return unescape_markdown(destination)
    return None


def markdown_links(source: str) -> list[tuple[int, str]]:
    """Collect inline destinations and reference-definition destinations."""
    links = []
    for line_number, line in visible_markdown(source):
        for match in INLINE_LINK_START.finditer(line):
            destination = inline_destination(line, match.end())
            if destination is not None:
                links.append((line_number, destination))
        reference = REFERENCE_LINK.match(line)
        if reference:
            destination = reference.group(2).strip("<>")
            links.append((line_number, unescape_markdown(destination)))
    return links


def undefined_references(source: str) -> list[tuple[int, str]]:
    """Find explicit full or collapsed references with no matching definition.

    Bare shortcut references cannot be distinguished from ordinary bracketed text
    when no definition exists, so they are intentionally not linted.
    """
    visible = visible_markdown(source)

    def normalize(label: str) -> str:
        return " ".join(label.split()).casefold()

    definitions = {
        normalize(match.group(1))
        for _, line in visible
        if (match := REFERENCE_LINK.match(line))
    }
    undefined = []
    for line_number, line in visible:
        if REFERENCE_LINK.match(line):
            continue
        for match in REFERENCE_USAGE.finditer(line):
            label = match.group(2) or match.group(1)
            if normalize(label) not in definitions:
                undefined.append((line_number, label))
    return undefined


def heading_anchors(source: str) -> set[str]:
    """Calculate anchors for standard Markdown ATX headings."""
    counts: dict[str, int] = defaultdict(int)
    anchors = set()
    for _, line in visible_markdown(source):
        match = HEADING.match(line)
        if not match:
            continue
        title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", match.group(1))
        title = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        occurrence = counts[title]
        counts[title] += 1
        anchors.add(f"{title}-{occurrence}" if occurrence else title)
    return anchors


def validate_markdown(path: Path, root: Path) -> tuple[list[str], int]:
    errors = []
    text = path.read_text(encoding="utf-8")
    for line_number, label in undefined_references(text):
        errors.append(f"{path.relative_to(root)}:{line_number}: undefined reference: {label}")
    links = markdown_links(text)
    for line_number, destination in links:
        try:
            parsed = urlsplit(destination)
        except ValueError as exc:
            errors.append(f"{path.relative_to(root)}:{line_number}: invalid link {destination!r}: {exc}")
            continue
        if parsed.scheme or parsed.netloc or destination.startswith("//"):
            continue
        local_path = unquote(parsed.path)
        if local_path.startswith("/"):
            errors.append(f"{path.relative_to(root)}:{line_number}: use repository-relative links: {destination}")
            continue
        target = (path.parent / local_path).resolve() if local_path else path.resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(root)}:{line_number}: link escapes repository: {destination}")
            continue
        if target.is_dir():
            target = target / "README.md"
        if not target.is_file():
            errors.append(f"{path.relative_to(root)}:{line_number}: missing target: {destination}")
            continue
        if parsed.fragment and target.suffix.lower() == ".md":
            anchor = unquote(parsed.fragment)
            if anchor not in heading_anchors(target.read_text(encoding="utf-8")):
                errors.append(f"{path.relative_to(root)}:{line_number}: missing heading #{anchor} in {target.relative_to(root)}")
    return errors, len(links)


def validate_repository(root: Path) -> tuple[list[str], int, int]:
    root = root.resolve()
    errors = [f"Missing required foundation file: {path}" for path in REQUIRED_FILES if not (root / path).is_file()]
    documents = sorted(
        path for path in root.rglob("*.md")
        if not any(part in {".git", ".venv", "artifacts"} for part in path.relative_to(root).parts)
    )
    if not documents:
        errors.append("No Markdown documentation found")
    link_count = 0
    for path in documents:
        file_errors, file_links = validate_markdown(path, root)
        errors.extend(file_errors)
        link_count += file_links
    return errors, len(documents), link_count


def main() -> int:
    try:
        errors, document_count, link_count = validate_repository(ROOT)
    except (OSError, UnicodeError) as exc:
        print(f"Documentation validation could not complete: {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Documentation validation failed with {len(errors)} issue(s).", file=sys.stderr)
        return 1
    print(f"Validated {document_count} Markdown files and {link_count} link destinations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
