# Reference example: .NET Binary Tools

[.NET Binary Tools](https://github.com/infoconex/dotnet-binary-tools) is the initial engineering reference. Its [merged foundation commit](https://github.com/infoconex/dotnet-binary-tools/tree/9bf8e13471fa2a8fedd458d2da76476b448ecae5) established a modern .NET solution with Domain, Application, Infrastructure, and CLI projects, extensive capability/requirement/scenario specifications, documented TDD, and cross-platform CI.

## Patterns worth adapting

- Explicit dependencies and ports owned by inner application boundaries.
- Stable requirement and scenario identifiers, with verification state maintained in one authoritative traceability location.
- Clear distinction between planned features, implemented code, and observed acceptance evidence.
- Centralized code style, MSBuild and NuGet configuration when justified by the project.
- Review gates that distinguish PR acceptance, merges, tags, and releases.
- CI with observed SDK/OS context and locally executable validation operations.

## What does not become a universal requirement

- Binary inspection behavior, metadata parsing, CLI commands, and safeguards specific to untrusted assemblies.
- A mandatory four-project structure for every .NET application.
- Native AOT distribution or the exact framework version, package identity, or OS matrix.
- The reference project's fixed capability IDs, scenario counts, or hardcoded architecture validator paths.

The reference repository is a case study, not a template package. Additional work in its [engineering foundation issue](https://github.com/infoconex/dotnet-binary-tools/issues/2) should only be adopted as tested playbook guidance after its actual behavior is independently evaluated.
