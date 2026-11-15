# .NET Project Playbook

An AI-first engineering foundation for establishing, assessing, and improving dependable .NET repositories. It will combine opinionated engineering standards, reusable assets, and evidence-based verification through interactive project discovery. AI will help adapt the playbook to a project's actual needs; executable checks will verify behavior where applicable.

It is intended for individual developers and maintainers of both new and existing repositories. The initial technology scope is primarily C#, including modern SDK-style .NET and traditional .NET Framework projects. Planned project profiles include class libraries, CLI tools, web APIs, and workers; no installable profile is available yet.

The longer-term direction is to consolidate this .NET-specific foundation into a technology-independent `project-playbook`, with .NET as its first technology module. This is a direction for future work, not a current repository migration; the destination repository is not currently a public adoption resource.

## Current state

**Documentation and governance foundation only.** The current foundation provides governing principles, contribution guidance, and a planned AI-assisted adoption and template architecture. No interactive adoption agent, consumer-project AI instruction template, installable .NET project template, automated documentation validator, or bootstrap command is available yet. [Issue #1](https://github.com/infoconex/dotnet-project-playbook/issues/1) establishes this foundation; subsequent issues will deliver usable assets and acceptance tests.

**Licensing:** This repository is public, but no redistribution license has been selected. Public visibility alone does not grant permission to reuse or redistribute its contents. See the [licensing decision](docs/governance/repository-organization.md#licensing-decision) before adopting or distributing playbook assets.

## Navigate the playbook

| Topic | Start here |
| --- | --- |
| Approved engineering principles | [Engineering principles](docs/standards/engineering-principles.md) |
| How standards are authored and changed | [Standards governance](docs/governance/standards.md) |
| Repository layout and configuration | [Repository organization](docs/governance/repository-organization.md) |
| Template design and planned project types | [Template architecture](docs/architecture/template-model.md) |
| Planned AI-first adoption decision | [ADR 0002](docs/decisions/0002-ai-first-adoption.md) |
| Architectural decisions | [Decision record index](docs/decisions/README.md) |
| Reference project and lessons | [.NET Binary Tools case study](examples/dotnet-binary-tools.md) |
| All documentation | [Documentation index](docs/README.md) |
| Contributing | [Contribution guide](CONTRIBUTING.md) |
| Security reporting | [Security policy](SECURITY.md) |

## Intended AI-assisted adoption workflow

When the necessary assets and guidance exist, a developer will point an AI coding agent to this playbook and a target repository. The agent must be given access to the relevant content; it cannot be assumed to discover an unrelated repository automatically.

1. **Discover:** Guide the developer through project decisions with focused questions, one at a time by default. For existing repositories, inspect current files and conventions to inform those questions.
2. **Assess:** Identify applicable Required, Recommended, and Optional standards; distinguish actual gaps from intentional choices and unresolved questions.
3. **Propose:** Explain a project-specific foundation or improvement plan, including affected files, alternatives, and verification. The developer controls whether the task is assessment-only or authorizes implementation.
4. **Apply and verify when authorized:** Adapt canonical assets, create or modify relevant project structures, and run proportionate checks. Report actual results and unverified claims separately.
5. **Reassess on demand:** Compare an existing repository with updated playbook guidance without silently overwriting its local decisions.

The planned workflow does not require a playbook-specific tracking file in the target repository. It should rely on existing project content, ask when an intentional exception cannot be determined, and record the provenance of applied changes in the relevant change review. It should support manual reuse of assets as well as AI-assisted adaptation.

**This is a future workflow, not a currently supported command or verified AI capability.**

Standards define requirements and rationale; AI adoption guidance determines how to discover and apply them; templates provide reusable implementation; scripts validate behavior; examples demonstrate adoption. Each has a distinct [source of authority](docs/governance/standards.md). Not every practice requires the same project layout: SOLID and test-first development apply broadly, while separate compiled layers and deployment mechanisms depend on the application.

## Reference implementation

[.NET Binary Tools](https://github.com/infoconex/dotnet-binary-tools) is the first reference for architecture boundaries, requirements traceability, CI evidence, and review governance. It is an **example**, not an installable starter and not a source of mandatory binary-inspection conventions.

## Current verification

For this documentation-only foundation, review changes for accuracy, navigation, and consistency with the authoritative standards. Automated validation is deferred until there is executable template or automation behavior worth verifying. Future acceptance will cover both AI-guided new-project creation and assessment of existing repositories, using disposable test repositories for repeatable checks and real projects for practical evaluation. Future executable checks should run locally and through CI when applicable.
