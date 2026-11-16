# Instructions for agents using or maintaining the playbook

This file guides AI agents asked either to help a developer **use** this playbook or to **contribute** to its repository. The playbook's own `AGENTS.md` is not a template to copy into a consumer project. A future consumer `AGENTS.md` template will be a separate asset, adapted to the target project's decisions and conventions.

Read the [README](README.md) for available versus planned capabilities, [engineering principles](docs/standards/engineering-principles.md) for the normative baseline, and [standards governance](docs/governance/standards.md) for authority and applicability.

## Helping a developer use the playbook

Read and follow [start-here.md](start-here.md) as the authoritative conversational workflow for helping a developer create, assess, or improve a project. Follow its discovery, applicability, authorization, proposal, and verification guidance without repeating those instructions here. The [AI-first architecture decision](docs/decisions/0001-ai-first-playbook-architecture.md) explains the rationale.

No working installer, dedicated discovery agent, consumer template, or executable project generator is available in this foundation. Do not present the documented process as implemented automation. The contribution rules below govern this playbook's repository and must not be imposed automatically on a consumer project.

## Contributing to this repository

Follow [CONTRIBUTING.md](CONTRIBUTING.md) for the change workflow. These rules govern maintenance of the playbook itself.

## Scope and quality

- Keep standards, AI adoption guidance, distributable templates, validation scripts, and reference examples distinct. Do not place a project-specific assumption into a universal template.
- Maintain SOLID and test-first development as mandatory expectations. Prefer hexagonal architecture, with physical project boundaries determined by responsibilities and actual dependencies.
- A proposed template is not a working generator. Do not claim runtime, installation, security, coverage, or cross-platform acceptance without observed evidence.
- For platform, framework, dependency, or tooling decisions, follow the [evidence-based technical decision standard](docs/standards/engineering-principles.md#evidence-based-technical-decisions): research applicable authoritative guidance first, identify remaining uncertainty, verify project-specific behavior, and justify deviations. Routine changes need no research write-up.
- Prefer one authoritative definition for each policy or verification status. Link to it rather than maintaining synchronized copies.
- Do not add placeholders, tools, dependencies, or configuration files without a demonstrated purpose.

## Changes and review

- Work from a GitHub issue on an issue-specific branch. Ordinarily use one issue and one pull request.
- Do not commit directly to `main`, merge, tag, publish, or release without explicit owner authorization. The repository's one-time bootstrap commit was an approved exception.
- For executable behavior changes, use TDD: meaningful failing test, minimum implementation, then refactoring. Documentation-only edits do not require behavioral tests or an exception; review their accuracy and navigation instead.
- Run relevant locally executable checks when they exist and capture actual results, environment versions, commit SHA, and applicable CI links in the pull request. For documentation-only changes, record the review performed.
- When automated checks are introduced, GitHub Actions should invoke equivalent repository-controlled native commands or validation scripts as appropriate; GitHub-managed platform services are documented exceptions.
- Never confuse unavailable or skipped checks with passing validation. A documentation review does not establish a successful build or template-generation test.

## Current verification

This documentation-only foundation has no executable validator or CI verification workflow. Review links, navigation, accuracy, and standards consistency manually. Future generator and product-template tests must be added when those assets exist. See the [template architecture](docs/architecture/template-model.md).
