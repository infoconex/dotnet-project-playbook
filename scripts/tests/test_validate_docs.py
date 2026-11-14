"""Executable tests for the repository's documentation validator."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validate_docs import heading_anchors, markdown_links, validate_markdown, validate_repository


class MarkdownValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write(self, path: str, content: str) -> Path:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def test_valid_relative_link_and_anchor(self) -> None:
        self.write("docs/target.md", "# Target Heading\n")
        source = self.write("README.md", "See [target](docs/target.md#target-heading).\n")
        self.assertEqual(validate_markdown(source, self.root), ([], 1))

    def test_broken_target_is_reported(self) -> None:
        source = self.write("README.md", "[missing](docs/absent.md)\n")
        errors, count = validate_markdown(source, self.root)
        self.assertEqual(count, 1)
        self.assertIn("missing target", errors[0])

    def test_broken_heading_is_reported(self) -> None:
        self.write("target.md", "# Actual heading\n")
        source = self.write("README.md", "[wrong](target.md#not-here)\n")
        errors, _ = validate_markdown(source, self.root)
        self.assertIn("missing heading", errors[0])

    def test_directory_link_uses_readme(self) -> None:
        self.write("docs/README.md", "# Docs\n")
        source = self.write("README.md", "[docs](docs/)\n")
        self.assertEqual(validate_markdown(source, self.root), ([], 1))

    def test_external_links_are_ignored(self) -> None:
        source = self.write("README.md", "[external](https://example.com/thing#topic)\n")
        self.assertEqual(validate_markdown(source, self.root), ([], 1))

    def test_code_fences_and_inline_code_do_not_produce_links(self) -> None:
        links = markdown_links("`[inline](bad.md)`\n```markdown\n[fenced](bad.md)\n```\n[real](ok.md)\n")
        self.assertEqual(links, [(5, "ok.md")])

    def test_link_outside_repository_is_rejected(self) -> None:
        source = self.write("README.md", "[outside](../outside.md)\n")
        errors, _ = validate_markdown(source, self.root)
        self.assertIn("escapes repository", errors[0])

    def test_absolute_link_is_rejected(self) -> None:
        source = self.write("README.md", "[absolute](/tmp/example.md)\n")
        errors, _ = validate_markdown(source, self.root)
        self.assertIn("repository-relative", errors[0])

    def test_reference_style_definition_is_validated(self) -> None:
        self.write("docs/example.md", "# Example\n")
        source = self.write("README.md", "[example][reference]\n\n[reference]: docs/example.md\n")
        self.assertEqual(validate_markdown(source, self.root), ([], 1))

    def test_undefined_full_reference_is_rejected(self) -> None:
        source = self.write("README.md", "See [installation instructions][install-guide].\n")
        errors, count = validate_markdown(source, self.root)
        self.assertEqual(count, 0)
        self.assertIn("undefined reference", errors[0])
        self.assertIn("install-guide", errors[0])

    def test_undefined_collapsed_reference_is_rejected(self) -> None:
        source = self.write("README.md", "Read [installation guide][].\n")
        errors, count = validate_markdown(source, self.root)
        self.assertEqual(count, 0)
        self.assertIn("undefined reference", errors[0])
        self.assertIn("installation guide", errors[0])

    def test_reference_labels_are_case_and_whitespace_insensitive(self) -> None:
        self.write("docs/guide.md", "# Guide\n")
        source = self.write(
            "README.md",
            "Read [the guide][  INSTALL   GUIDE ].\n\n[Install Guide]: docs/guide.md\n",
        )
        self.assertEqual(validate_markdown(source, self.root), ([], 1))

    def test_ordinary_bracketed_text_is_not_an_undefined_reference(self) -> None:
        source = self.write("README.md", "A [note] is not necessarily a link.\n")
        self.assertEqual(validate_markdown(source, self.root), ([], 0))

    def test_undefined_reference_in_code_is_ignored(self) -> None:
        source = self.write(
            "README.md",
            "`[inline][unknown]`\n```markdown\n[fenced][unknown]\n```\n",
        )
        self.assertEqual(validate_markdown(source, self.root), ([], 0))

    def test_same_document_heading_link_is_valid(self) -> None:
        source = self.write(
            "docs/guide.md",
            "# Guide\n\n## Verification and applicability\n\n[Verification](#verification-and-applicability)\n",
        )
        self.assertEqual(validate_markdown(source, self.root), ([], 1))

    def test_same_document_missing_heading_is_reported(self) -> None:
        source = self.write("docs/guide.md", "# Guide\n\n[Missing](#not-a-heading)\n")
        errors, count = validate_markdown(source, self.root)
        self.assertEqual(count, 1)
        self.assertIn("missing heading", errors[0])

    def test_balanced_parentheses_in_destination_are_valid(self) -> None:
        self.write("docs/guide(v2).md", "# Guide\n")
        source = self.write("README.md", "[Guide](docs/guide(v2).md)\n")
        self.assertEqual(validate_markdown(source, self.root), ([], 1))

    def test_nested_parentheses_in_destination_are_valid(self) -> None:
        self.write("docs/guide(v2(beta)).md", "# Guide\n")
        source = self.write("README.md", "[Guide](docs/guide(v2(beta)).md)\n")
        self.assertEqual(validate_markdown(source, self.root), ([], 1))

    def test_escaped_parentheses_in_destination_are_unescaped(self) -> None:
        self.write("docs/guide(v2).md", "# Guide\n")
        source = self.write("README.md", r"[Guide](docs/guide\(v2\).md)" + "\n")
        self.assertEqual(validate_markdown(source, self.root), ([], 1))

    def test_parenthesized_destination_with_title_is_valid(self) -> None:
        self.write("docs/guide(v2).md", "# Guide\n")
        source = self.write("README.md", '[Guide](docs/guide(v2).md "Version 2")\n')
        self.assertEqual(validate_markdown(source, self.root), ([], 1))

    def test_angle_bracket_destination_with_spaces_is_valid(self) -> None:
        self.write("docs/guide (v2).md", "# Guide\n")
        source = self.write("README.md", "[Guide](<docs/guide (v2).md>)\n")
        self.assertEqual(validate_markdown(source, self.root), ([], 1))

    def test_duplicate_headings_have_distinct_anchors(self) -> None:
        anchors = heading_anchors("# One\n# One\n## Another heading\n")
        self.assertEqual(anchors, {"one", "one-1", "another-heading"})

    def test_required_foundation_files_are_checked(self) -> None:
        self.write("README.md", "# Root\n")
        errors, documents, links = validate_repository(self.root)
        self.assertEqual((documents, links), (1, 0))
        self.assertTrue(any("Missing required foundation file" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
