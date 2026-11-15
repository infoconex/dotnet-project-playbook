# Instructions for agents using or maintaining the playbook

This file guides AI agents asked either to help a developer **use** this playbook or to **contribute** to its repository. The playbook's own `AGENTS.md` is not a template to copy into a consumer project. A future consumer `AGENTS.md` template will be a separate asset, adapted to the target project's decisions and conventions.

Read the [README](README.md) for available versus planned capabilities, [engineering principles](docs/standards/engineering-principles.md) for the normative baseline, and [standards governance](docs/governance/standards.md) for authority and applicability.

## Helping a developer adopt the playbook

The intended adoption process is [AI-first and interactive](docs/decisions/0001-ai-first-playbook-architecture.md), but no working installer, discovery agent, or project-template implementation is available in this foundation yet. Do not present the following guidance as implemented automation.

- Confirm the developer's objective: create a new project, assess an existing repository, or implement previously approved improvements. Confirm access to the target repository; do not assume it or this playbook will be discovered automatically by another agent.
- Guide discovery through focused questions, one at a time by default. For an existing repository, inspect its actual structure, standards, toolchain, and documentation before recommending changes. Do not assume a particular project graph.
- Distinguish **Required**, **Recommended**, and **Optional** standards by project context. Use canonical standards and implemented reusable assets when available; do not invent templates or treat illustrative examples as defaults.
- Explain compatibility differences between modern .NET and traditional .NET Framework where they affect the recommendation. Base platform claims on applicable authoritative guidance and project-specific evidence.
- Present an assessment and proposed changes, distinguishing verified gaps from existing project choices and uncertainty. Do not classify an unexplained difference as a violation without checking its applicability and intent.
- Respect the authorization in the current request. Assessment-only means no target-repository changes; implementation requires the requested scope and the target repository's own governance. The contribution rules below apply to this playbook, not automatically to every consumer.
- When authorized to implement, adapt assets for the target project and execute meaningful available checks. Report observed results, skipped checks, and unverified capabilities accurately. Do not impose a playbook-specific adoption manifest; use existing project content for later reassessment and record change provenance in the relevant review.
- Keep the underlying standards provider-neutral. Tool-specific agent instructions may facilitate adoption but must not redefine the canonical rules.

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
- When automated checks are introduced, GitHub Actions should orchestrate repository-owned validation scripts; GitHub-managed platform services are documented exceptions.
- Never confuse unavailable or skipped checks with passing validation. A documentation review does not establish a successful build or template-generation test.

## Current verification

This documentation-only foundation has no executable validator or CI verification workflow. Review links, navigation, accuracy, and standards consistency manually. Future generator and product-template tests must be added when those assets exist. See the [template architecture](docs/architecture/template-model.md).
