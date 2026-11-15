# Repository organization and configuration

The playbook maintains standards, AI-assisted adoption guidance, reusable project assets, executable verification, and case studies in separate areas. Create a directory only when it has useful content; a proposed folder name does not imply that its capability is implemented.

| Path | Responsibility | State |
| --- | --- | --- |
| `docs/standards/` | Normative engineering expectations with explicit applicability. | Initial principles available |
| `docs/governance/` | Standards lifecycle, contribution policy, and repository conventions. | Available |
| `docs/architecture/` | Decisions about template composition and technical design. | Design available |
| `docs/decisions/` | Sequential immutable ADR rationale and supersession history. | Available |
| `templates/` | Canonical generated-project source, profile-specific content, and reusable assets. | Planned; not created |
| `scripts/` | Directly executable validation and future packaging scripts. | Planned; not created |
| `scripts/tests/` | Focused tests for future nontrivial validation script behavior. | Planned; not created |
| `tests/` | Generated-template and integration acceptance tests. | Planned; not created |
| `examples/` | Evidence-backed reference-project decisions, not source templates. | First reference available |
| `.github/` | Issue forms and PR guidance; maintenance automation when justified. | Governance available; automation planned |

## Naming and authority

- Use descriptive lowercase, hyphenated Markdown names and folders; preserve established .NET build-file spelling and case where required by their tools.
- Number decisions `NNNN-short-description.md`; [ADR conventions](../decisions/README.md) govern their history.
- Name validation scripts after the operation they perform. Prefer descriptive functions and tests rather than project-specific names in a generic validator.
- Place future distributable assets under `templates/`; do not use this repository's own `.github` workflow as an implicit project starter.
- The [standards governance contract](standards.md) determines where each kind of rule or evidence is authoritative.

## Foundational files and rationale

| File | Why it exists |
| --- | --- |
| `.editorconfig` | Stable UTF-8, LF, indentation and whitespace defaults for the playbook's current documents. This is not yet a consumer-project C# style template. |
| `.gitattributes` | Predictable Git text normalization across operating systems; binary formats are exempt and Windows batch files keep CRLF. |
| `.gitignore` | Excludes common local tooling, IDE, generated build and verification outputs without hiding source files. |
| `start-here.md` | Canonical AI-guided usage flow for new-project setup and existing-repository assessment; documentation, not an executable agent. |
| Root `AGENTS.md` and `CONTRIBUTING.md` | Distinguish AI-assisted adoption guidance from rules for maintaining this repository; neither is a consumer-project template. |
| `SECURITY.md` | A private reporting path and honest statement of the unreleased security support scope. |
| `.github/ISSUE_TEMPLATE/` | Structured changes and safe defect reporting, both tied to the issue-first workflow. |
| `.github/pull_request_template.md` | Reviewable changes with actual checks and explicit owner-merge approval. |

No .NET solution, NuGet configuration, runtime manifest, or toolchain file is needed for the current documentation-only foundation. Automated validation belongs to later executable features when justified.

## Licensing decision

The repository is public, but no redistribution license has been selected. Accordingly, no `LICENSE` file is introduced by Issue #1. Before distributing templates, the owner must approve the licensing approach and verify compatibility with included assets and examples. Public visibility alone does not grant permission to reuse or redistribute the content.
