# Instructions for human and AI contributors

Follow [CONTRIBUTING.md](CONTRIBUTING.md) for the change workflow and [engineering principles](docs/standards/engineering-principles.md) for the normative technical baseline. The [standards governance document](docs/governance/standards.md) explains where authority lives.

## Scope and quality

- Keep standards, distributable templates, validation scripts, and reference examples distinct. Do not place a project-specific assumption into a universal template.
- Maintain SOLID and test-first development as mandatory expectations. Prefer hexagonal architecture, with physical project boundaries determined by responsibilities and actual dependencies.
- A proposed template is not a working generator. Do not claim runtime, installation, security, coverage, or cross-platform acceptance without observed evidence.
- For platform, framework, dependency, or tooling decisions, follow the [evidence-based technical decision standard](docs/standards/engineering-principles.md#evidence-based-technical-decisions): research applicable authoritative guidance first, identify remaining uncertainty, verify project-specific behavior, and justify deviations. Routine changes need no research write-up.
- Prefer one authoritative definition for each policy or verification status. Link to it rather than maintaining synchronized copies.
- Do not add placeholders, tools, dependencies, or configuration files without a demonstrated purpose.

## Changes and review

- Work from a GitHub issue on an issue-specific branch. Ordinarily use one issue and one pull request.
- Do not commit directly to `main`, merge, tag, publish, or release without explicit owner authorization. The repository's one-time bootstrap commit was an approved exception.
- For behavior changes, use TDD: meaningful failing test, minimum implementation, then refactoring. State why a documentation-only change does not need a behavior test.
- Run relevant locally executable checks when they exist and capture actual results, environment versions, commit SHA, and applicable CI links in the pull request. For documentation-only changes, record the review performed.
- When automated checks are introduced, GitHub Actions should orchestrate repository-owned validation scripts; GitHub-managed platform services are documented exceptions.
- Never confuse unavailable or skipped checks with passing validation. A documentation review does not establish a successful build or template-generation test.

## Current verification

This documentation-only foundation has no executable validator or CI verification workflow. Review links, navigation, accuracy, and standards consistency manually. Future generator and product-template tests must be added when those assets exist. See the [template architecture](docs/architecture/template-model.md).
