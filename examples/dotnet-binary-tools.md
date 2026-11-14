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

## Documented guidance and repository-specific verification

The [.NET Binary Tools technical-decision change](https://github.com/infoconex/dotnet-binary-tools/commit/6731d1cd34508a9e93471416b78b7edf3017b8c4) documents a useful lesson from NuGet lock files and cross-platform runtime identifiers (RIDs): consult the established contracts before designing a broad exploration.

- **Documented:** Microsoft's [runtime identifier guidance](https://learn.microsoft.com/en-us/visualstudio/msbuild/net-sdk-multitargeting#specify-runtime-identifiers), [NuGet dependency locking guidance](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files#locking-dependencies), and [NU1004 reference](https://learn.microsoft.com/en-us/nuget/reference/errors-and-warnings/nu1004) describe the relevant restore inputs and locked-mode behavior. Those are not discoveries unique to the project.
- **Verified:** Only observed repository runs can establish which restore graph works with the application's dependencies, CI operating systems, Native AOT publishing, and clean .NET Tool installation. The exact tested scope and evidence belong in PR #3; a documented rule alone does not prove those scenarios passed.
- **Experimental:** A focused investigation is appropriate when guidance leaves a material question unanswered, such as the actual behavior of Apple Silicon restore environments for this application's dependency graph. Record the narrow question and limits of the result.

The [source PR](https://github.com/infoconex/dotnet-binary-tools/pull/3) is the location for exact-SHA results and current validation state. The reference commit documents the decision workflow; it should not be interpreted as proof that every platform and release gate passed. This example demonstrates the [playbook's research-first principle](../docs/standards/engineering-principles.md#evidence-based-technical-decisions) without requiring research reports for routine implementation.
