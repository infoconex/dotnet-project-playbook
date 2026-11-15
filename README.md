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
| Begin AI-guided project setup or assessment | [Start here](start-here.md) |
| Approved engineering principles | [Engineering principles](docs/standards/engineering-principles.md) |
| How standards are authored and changed | [Standards governance](docs/governance/standards.md) |
| Repository layout and configuration | [Repository organization](docs/governance/repository-organization.md) |
| Template design and planned project types | [Template architecture](docs/architecture/template-model.md) |
| AI-first architecture decision | [ADR 0001](docs/decisions/0001-ai-first-playbook-architecture.md) |
| Architectural decisions | [Decision record index](docs/decisions/README.md) |
| Reference project and lessons | [.NET Binary Tools case study](examples/dotnet-binary-tools.md) |
| All documentation | [Documentation index](docs/README.md) |
| Contributing | [Contribution guide](CONTRIBUTING.md) |
| Security reporting | [Security policy](SECURITY.md) |

## Intended AI-assisted workflow

The [start-here guide](start-here.md) provides the conversational entry point for guiding a developer through discovery, assessment, a project-specific proposal, authorized changes, and later reassessment. A general-purpose AI assistant can follow this documented process when given access to the playbook and relevant project information. This does **not** constitute a verified adoption agent, installable project generator, or automated validation capability.

Standards define requirements and rationale; the start-here guide describes how to use them; future templates provide reusable implementation; future scripts validate behavior; examples demonstrate adoption. Each has a distinct [source of authority](docs/governance/standards.md).

## Reference implementation

[.NET Binary Tools](https://github.com/infoconex/dotnet-binary-tools) is the first reference for architecture boundaries, requirements traceability, CI evidence, and review governance. It is an **example**, not an installable starter and not a source of mandatory binary-inspection conventions.

## Current verification

For this documentation-only foundation, review changes for accuracy, navigation, and consistency with the authoritative standards. Automated validation is deferred until there is executable template or automation behavior worth verifying. Future acceptance will cover both AI-guided new-project creation and assessment of existing repositories, using disposable test repositories for repeatable checks and real projects for practical evaluation. Future executable checks should run locally and through CI when applicable.
