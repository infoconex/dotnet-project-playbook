# .NET Project Playbook

An engineering playbook for creating and maintaining dependable .NET repositories. It will combine documented standards, reusable project templates, and automated verification so a newly generated repository starts with coherent development and delivery practices.

It is intended for maintainers creating .NET class libraries, CLI tools, web APIs, workers, and related repositories; these project profiles are planned, not yet available as installable templates.

## Current state

**Engineering foundation established.** This repository provides its governing principles, contribution workflow, and planned template architecture. No automated documentation validator, installable .NET project templates, or bootstrap commands are available yet. [Issue #1](https://github.com/infoconex/dotnet-project-playbook/issues/1) establishes the foundation; subsequent issues will deliver executable templates and their acceptance tests.

## Navigate the playbook

| Topic | Start here |
| --- | --- |
| Approved engineering principles | [Engineering principles](docs/standards/engineering-principles.md) |
| How standards are authored and changed | [Standards governance](docs/governance/standards.md) |
| Repository layout and configuration | [Repository organization](docs/governance/repository-organization.md) |
| Template design and planned project types | [Template architecture](docs/architecture/template-model.md) |
| Architectural decisions | [Decision record index](docs/decisions/README.md) |
| Reference project and lessons | [.NET Binary Tools case study](examples/dotnet-binary-tools.md) |
| All documentation | [Documentation index](docs/README.md) |
| Contributing | [Contribution guide](CONTRIBUTING.md) |
| Security reporting | [Security policy](SECURITY.md) |

## Intended adoption workflow

Once project templates have been implemented and verified, a maintainer will select a project profile, generate an appropriately named solution and repository foundation, run the included validation scripts, and configure GitHub's repository-level protection and security features. **This is a future workflow, not a currently supported command.**

Standards define requirements and rationale; templates provide reusable implementation; scripts validate behavior; examples demonstrate adoption. Each has a distinct [source of authority](docs/governance/standards.md). Not every practice requires the same project layout: SOLID and test-first development apply broadly, while separate compiled layers and deployment mechanisms depend on the application.

## Reference implementation

[.NET Binary Tools](https://github.com/infoconex/dotnet-binary-tools) is the first reference for architecture boundaries, requirements traceability, CI evidence, and review governance. It is an **example**, not an installable starter and not a source of mandatory binary-inspection conventions.

## Current verification

For this documentation-only foundation, review changes for accuracy, navigation, and consistency with the authoritative standards. Automated validation is deferred until there is executable template or automation behavior worth verifying. Future checks should run locally and through CI when applicable.
