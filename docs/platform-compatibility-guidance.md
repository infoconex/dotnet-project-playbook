# Platform compatibility, cross-platform, and .NET Framework guidance

This **non-normative, on-demand guide** helps teams choose and assess compatibility claims for .NET libraries, CLIs, web APIs, workers, applications and mixed solutions. The central rule is to distinguish **targeted APIs**, **tooling capable of producing an artifact**, **tests actually executed**, and **environments where that artifact actually operates**. Building successfully on one computer is not evidence of reliable operation on every OS or CPU architecture.

**Research reviewed:** November 15, 2026 (America/Los_Angeles). .NET versions, OS support, SDK/MSBuild/Visual Studio requirements, NuGet behavior and CI evidence evolve; recheck official documentation for the actual project and revision. This page does not declare any consumer repository compatible, install tooling, run a test, or supply a validator.

**Authority and boundaries:** [Engineering principles](standards/engineering-principles.md#evidence-based-technical-decisions) already require documented-versus-verified claims and research-first technical decisions. [STD-002](standards/engineering-principles.md#std-002) owns CI/local parity, [STD-006](standards/csharp.md#std-006) new compatible-project nullability, [STD-008](standards/csharp.md#std-008) compiler/analyzer enforcement, and conditional [STD-009](standards/testing.md#std-009) representative external-boundary verification. [Build and dependency guidance](build-dependency-guidance.md) owns SDK resolution, MSBuild imports, NuGet configuration and dependency locking; [security standards](standards/security.md) own security obligations. This guide adds **no STD-022** and no mandatory compatibility questionnaire, matrix file, RID list, TFM set, test platform, or migration.

## Begin with the actual consumer and execution requirement

For a **new project**, establish what will consume or run the artifact, the OS and CPU architectures that matter, the expected .NET runtime availability, native/third-party dependencies, deployment method, and support lifetime. Select the fewest target frameworks and tools that meet these known needs. A pure calculation library rarely requires a RID; an application that ships native executables may.

For an **existing repository**, inspect the solution/project formats, effective framework/language settings, package files, MSBuild imports, installed/tooling constraints, platform APIs, native dependencies, deployment instructions, release/consumer contract, and actual test/CI evidence before suggesting change. An old TFM, non-SDK project, packages.config or absent optional configuration is **not by itself a defect**. An untested environment is **unknown**, not automatically supported or broken.

When a requirement remains unclear, ask only the question that materially changes a recommendation: for example, whether an existing .NET Framework 4.8 consumer must remain supported, or whether users will execute a shipped binary on Linux arm64.

## Ten independently assessable compatibility dimensions

| Dimension | Documentary or static evidence can establish | What needs observed project-specific evidence |
| --- | --- | --- |
| 1. Target framework | TFM, available compile-time APIs, official compatibility table and project-specific conditions | Whether a real consumer can load and use the produced assembly and its dependencies |
| 2. Package restore | NuGet framework/RID asset selection rules and declared packages/sources | Actual restore result and resolved direct/transitive assets for each relevant TFM/RID |
| 3. Compilation/build | SDK/MSBuild support, project type, reference assemblies and documented tasks | Successful compilation, resource generation, targets and tooling on the specified build host |
| 4. Test execution | Test runner/framework support for a given TFM/OS | Discovered, passed, failed and skipped tests on that actual host/runtime |
| 5. Runtime execution | Microsoft runtime and OS support contract; declared runtime prerequisites | Application startup, significant flows, native binding, environment-specific behavior and failures |
| 6. Publish/package | Supported publish modes and package layout rules | Artifacts produced with actual output/dependencies and inspection of their contents |
| 7. Distribution/consumer | NuGet/.NET Tool and deployment consumption requirements | Installation, load, launch and important workflows in a representative consumer environment |
| 8. Operating system | Official OS support and presence of platform-specific APIs | Behavior on each claimed OS and version, including filesystem, security and hosting assumptions |
| 9. CPU architecture | Supported RIDs and build/runtime architecture dependencies | Launch/native asset resolution on each claimed architecture, with x86/x64/arm64 boundaries |
| 10. Toolchain/language | Supported SDK/MSBuild/VS/compiler pairing and language-feature contracts | Effective versions, successful commands and diagnostics in the repository's real configurations |

These are **questions**, not ten required CI jobs. The needed depth depends on the claim and its consequences. Microsoft's [TFM reference](https://learn.microsoft.com/en-us/dotnet/standard/frameworks), [SDK/MSBuild/Visual Studio version policy](https://learn.microsoft.com/en-us/dotnet/core/porting/versioning-sdk-msbuild-vs), [NuGet package compatibility](https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/nuget-package-compatibility-rules), [RID catalog](https://learn.microsoft.com/en-us/dotnet/core/rid-catalog), and [runtime support policy](https://learn.microsoft.com/en-us/dotnet/core/releases-and-support) are sources for documented contracts, not substitute application tests.

### Evidence strength and how to describe it

- **Documented:** The vendor's published contract applies to identified .NET/tool versions, OS and architectures; the repository's execution is not thereby verified.
- **Inspected:** Source, configuration, dependency metadata or a workflow declares an intent or capability; no result is inferred from configuration alone.
- **Built/restored:** An exact command passed in a named environment; this does not establish tests or runtime execution.
- **Tested/executed:** The actual test runner or application ran on a named OS/runtime/architecture with recorded outcome and meaningful coverage. Passing tests cover what they exercise, not all behavior.
- **Published/consumed:** Output was packaged and a representative consumer actually installed/loaded/executed it; this is narrower than universal compatibility.
- **Unverified/unavailable/skipped:** Explicitly retain the gap. A conditional or skipped CI job is not a pass. Failed and not-run operations have different meanings.

Record exact commit/ref, artifact, SDK/MSBuild and runtime versions, OS and architecture, direct/native dependencies, command or workflow URL, output, date and significant omissions when making a consequential claim. A branch name alone is movable; an immutable SHA provides stronger provenance. Keep changing status in the issue/PR or target's authoritative traceability location, not in copied playbook indexes.

### Lightweight compatibility evidence matrix

Use one row per meaningful operation, particularly when multiple TFMs, OSes, architectures or distribution forms create distinct results. Columns can be adjusted to context; **there is no requirement to check this matrix into every repository**.

| Project / artifact | TFM | SDK / build tool | OS | Arch / RID | Dependencies | Operation | Result / evidence class | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Illustrative pure library | netstandard2.0 | Compatible SDK | Not yet selected | AnyCPU | Consumer-specific | TFM review | Documented API compatibility only | Restore/build and a real .NET Framework consumer are unverified |
| Illustrative modern CLI | net11.0 | Compatible SDK 11 | Linux | linux-x64 | Native library, if any | Publish command (proposed) | **Not executed** | No artifact, launch or consumer evidence |

Never fill the result column with “passed” for an illustrative command. For an existing system, supply each actual environment/operation as a separate row and disclose missing test discovery or native dependency coverage.

## Target framework selection and consumer compatibility

A **target framework moniker (TFM)** describes the API set used to compile and select compatible package assets; it is not the installed runtime or a complete operating-system guarantee. For example, net11.0 targets modern .NET 11 APIs; net48 targets .NET Framework 4.8; net11.0-windows exposes Windows-specific APIs. An OS-specific TFM helps compile intended APIs and affects package selection; it does not verify the customer's OS version or correct behavior. [.NET target frameworks](https://learn.microsoft.com/en-us/dotnet/standard/frameworks).

| Consumer need | Proportionate starting point | Important tradeoff |
| --- | --- | --- |
| Modern .NET-only application/service | One currently supported modern .NET TFM, chosen for support horizon and hosting | An app ordinarily targets its actual runtime rather than .NET Standard |
| Modern .NET-only reusable library | One suitable supported modern .NET TFM | Modern APIs and simpler testing; no benefit from .NET Standard merely for its name |
| Library also used by .NET Framework | Evaluate netstandard2.0 with real Framework consumer tests | .NET Framework does **not** implement netstandard2.1; .NET Framework 4.6.1 has known .NET Standard 2.0 consumption issues, so Microsoft recommends Framework 4.7.2 or later for those consumers |
| Consumers need different APIs or package assets | Multi-target the minimum necessary TFMs (for example, netstandard2.0 plus a current net TFM) | Per-TFM conditional compilation, dependencies, tests, package/API surface and maintenance grow |
| Windows-specific app or library | Use a compatible Windows platform-specific TFM or .NET Framework TFM as applicable | A Windows-specific TFM/API removes or restricts non-Windows execution claims |
| Existing public .NET Framework library | Preserve supported binary and package contracts unless consumer evidence justifies migration | Retargeting, recompilation or adding a TFM can change API/assembly/package compatibility |

[.NET Standard](https://learn.microsoft.com/en-us/dotnet/standard/net-standard) is an API contract for libraries, **not an executable runtime**. It remains useful especially for .NET Framework interoperability, but Microsoft recommends targeting modern .NET directly when older framework implementations are not consumers. Multi-targeting is useful when one common API surface or binary is insufficient, not merely because it is possible. [Cross-platform library targeting](https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/cross-platform-targeting).

Distinguish **source compatibility** (code can be compiled against another set of APIs), **binary/API compatibility** (existing compiled consumers can link/load), **NuGet compatibility** (a suitable asset and dependencies are selected), and **runtime compatibility** (the app actually behaves correctly on its host). Source recompilation or a successful NuGet restore is not proof of the other three.

The support lifecycle is a separate decision: as reviewed in November 2026, .NET 11 is STS and .NET 10 is LTS. Do not use the newest release merely because it exists, or keep an unsupported runtime indefinitely without an explicitly understood risk/modernization plan. Verify current [supported .NET versions](https://learn.microsoft.com/en-us/dotnet/core/releases-and-support) and the hosting/consumer upgrade policy.

## Build and run environments: modern and traditional projects

| Project kind | Suitable restore/build starting point | Important environment and execution boundary |
| --- | --- | --- |
| Modern SDK-style .NET | dotnet restore/build/test with a compatible SDK and workloads | The SDK is cross-platform, but a workload, target, task or native dependency may not be |
| SDK-style .NET Framework | Compatible SDK/MSBuild with target Framework reference assemblies | Cross-OS **compilation may be possible for suitable projects**; Microsoft .NET Framework **execution remains Windows-only** |
| Traditional non-SDK Framework + PackageReference | Supported Windows Visual Studio MSBuild/Build Tools; msbuild restore/build | Check old imports, custom targets, compiler and targeting packs; do not assume dotnet build supports the project |
| Traditional non-SDK Framework + packages.config | NuGet CLI restore, then supported Windows MSBuild/Build Tools; a supported MSBuild packages.config restore path is also documented | NuGet package installation semantics, project imports, NUnit/VSTest runner and real Windows Framework runtime matter |
| Mixed solution | Select compatible restore/build tools for **all included project systems** | One Windows-only project/target may require a Windows solution job even if other projects build on Linux/macOS |

Reference assemblies expose target APIs for **compilation**. They are not implementation assemblies and cannot make a Windows-only Framework runtime run on Linux. Microsoft's [Framework reference assemblies guidance](https://learn.microsoft.com/en-us/dotnet/framework/migration-guide/reference-assemblies) describes both developer packs and NuGet reference-assembly packages; suitable compilation does not prove that every legacy project imports, task, test runner or COM dependency works on a non-Windows build host. The [Framework installation guide](https://learn.microsoft.com/en-us/dotnet/framework/install/on-windows-10) identifies .NET Framework as Windows-only. Third-party runtimes such as Mono must be assessed as distinct consumer contracts, not silently equated with Microsoft's .NET Framework.

The SDK used by a command, the project's TFM, and the runtime installed to **execute** it are distinct. An optional global.json controls **SDK resolution** (including roll-forward and search from the effective working directory); it does not install or pin the execution runtime or standalone Visual Studio MSBuild. See [Issue #7 guidance](build-dependency-guidance.md#sdk-resolution-targeting-and-tooling) and [global.json](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json).

C# syntax depends on the compiler and configured language version as well as TFM. A legacy project explicitly using C# 7.3 must not receive unguarded C# 8+ syntax or modern nullability/analyzer settings. [C# language versioning](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning) and [existing C# guidance](csharp-guidance.md#nullability-and-language-features) govern selection; STD-006's conditional new-project obligation remains separate. Record effective versions (for example, dotnet --info, dotnet --list-sdks, relevant MSBuild and runner versions) rather than assuming installed tools match the tool that built an artifact.

## Runtime identifiers, publishing and distribution

A **runtime identifier (RID)** such as win-x64, linux-x64 or osx-arm64 selects target-specific runtime/native package assets and publish behavior where needed. Prefer the [portable RID graph](https://learn.microsoft.com/en-us/dotnet/core/rid-catalog). Modern SDKs no longer use the historical distro/version-specific RID graph by default. Do not add RuntimeIdentifier or RuntimeIdentifiers to every library or project just to signal an aspirational compatibility list.

| Deployment choice | When it adds value | Evidence/limitation |
| --- | --- | --- |
| Portable framework-dependent DLL | Shared installed .NET runtime is an acceptable prerequisite | Verify the required runtime/shared framework exists and actual launch works |
| RID-specific framework-dependent apphost | Native assets or a platform-specific launcher is needed, while runtime stays shared | RID selection does not by itself imply self-contained deployment in .NET 8+ |
| Self-contained publish | Consumer cannot reasonably install the runtime or deployment must carry it | Publish explicitly self-contained; verify OS/architecture/native prerequisites and servicing responsibility |
| Single-file | One-file distribution materially simplifies delivery | The bundle is OS/architecture-specific; extraction and file-access semantics need review where relevant |
| Native AOT | Startup, runtime-independent delivery or constrained distribution justifies its restrictions | Publish for an actual RID with required native tools; Native AOT does **not** support cross-OS compilation; verify each target host separately |
| NuGet library or .NET Tool package | Developer/consumer acquisition through NuGet is the desired delivery channel | Inspect framework/RID assets, package metadata, clean install and real consumer execution |

[Publishing overview](https://learn.microsoft.com/en-us/dotnet/core/deploying/), [.NET 8 RID/self-contained change](https://learn.microsoft.com/en-us/dotnet/core/compatibility/sdk/8.0/runtimespecific-app-default), [Native AOT cross-compilation](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/cross-compile), and [RID-specific .NET tools](https://learn.microsoft.com/en-us/dotnet/core/tools/rid-specific-tools) describe these distinct contracts. Single-file or AOT is optional, not a general reliability upgrade. A successful publish proves output creation, **not** successful launch on its target host.

## Platform-sensitive APIs and dependencies

Review code and transitive dependencies where OS differences plausibly affect the product:

- **Filesystem:** case sensitivity, Unicode normalization, reserved names, separators, permissions, temporary paths, symbolic links, file locking and path lengths.
- **Process and hosting:** executable discovery, shell commands, environment variables, service/daemon and container assumptions, working directory, signals and terminal behavior.
- **Windows-bound facilities:** Registry, Windows services, COM, Windows identity/security and platform-specific desktop APIs.
- **Native integration:** P/Invoke libraries, architecture and C ABI assumptions, loader paths, cryptography provider availability and packaged native assets.
- **Network/identity/security:** trust stores, certificates, authentication protocols, proxy configuration, DNS and OS-specific cryptography.
- **Localization and execution:** culture/encoding differences, line endings, time zone data, architecture-specific behavior and resource availability.

For supported modern TFMs, [CA1416](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1416) and relevant SupportedOSPlatform/UnsupportedOSPlatform attributes and recognized OS guards help detect unguarded platform-specific calls. The analyzer is **static risk evidence**, not universal OS testing; rule activation and behavior differ by TFM, SDK and project system. Do not prescribe unsupported modern analyzer properties for a C# 7.3 non-SDK project or duplicate [STD-008](standards/csharp.md#std-008)'s risk-based enforcement policy. Where analyzer support is unavailable, review known platform APIs, native imports and representative behavior explicitly. Use an OS-specific target only when the product intentionally needs it.

NuGet selects framework-specific compile/runtime assets and, when applicable, RID-specific native/runtime assets. **Compile-time ref assets, runtime lib assets, and runtimes/{rid} assets are not interchangeable.** PackageReference may select distinct direct/transitive graphs per TFM/RID; conditional references add more cases. A packages.config repository has different installation and asset behavior, including limits around modern ref/runtime conventions. See [NuGet target frameworks](https://learn.microsoft.com/en-us/nuget/reference/target-frameworks), [multi-target package layout](https://learn.microsoft.com/en-us/nuget/create-packages/supporting-multiple-target-frameworks), [NuGet native files](https://learn.microsoft.com/en-us/nuget/create-packages/native-files-in-net-packages), [PackageReference](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files), and [packages.config](https://learn.microsoft.com/en-us/nuget/reference/packages-config). A successful restore only verifies a compatible resolution **for those inputs**; runtime behavior and third-party native dependencies may still fail. [Build/dependency guidance](build-dependency-guidance.md#dependency-ownership-and-version-selection) remains authoritative for package configuration, and [STD-020](standards/security.md#std-020) for applicable dependency-vulnerability obligations.

## Worked selection example: a portable modern library

Suppose a new, pure calculation library has only supported modern .NET consumers, no native dependencies, and a preference for the current LTS support horizon. One suitable illustrative project file is:

~~~xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
  </PropertyGroup>
</Project>
~~~

No RuntimeIdentifier, additional TFM, .NET Standard target, or deployment setting is needed merely to compile this library. Keep behavioral tests in a compatible separate test project. If the product **claims** Windows, Linux and macOS support, run the relevant tests and representative library consumers on the supported hosts and architecture combinations; check for unexpected platform-specific APIs and dependencies. Example operations for those later project-specific checks, **not commands executed by this guide**:

~~~text
dotnet --info
dotnet restore
dotnet build --no-restore -c Release
dotnet test --no-restore -c Release
~~~

A successful sequence on Linux alone does not establish Windows or macOS behavior. If real .NET Framework consumers emerge, re-evaluate netstandard2.0 or the smallest justified multi-target set, package dependencies, and consumer execution. The choice of net10.0 here is **illustrative for the stated support horizon**, not a universal playbook default.

## Reference-project illustrations: do not generalize their choices

### RecordSift: a Windows-bound legacy library

At inspected main revision [1809d06c0fade59e4769d16e0f8eaf10fa426004](https://github.com/infoconex/RecordSift/tree/1809d06c0fade59e4769d16e0f8eaf10fa426004), production and test project files use traditional non-SDK MSBuild, TargetFrameworkVersion v4.8 and LangVersion 7.3; tests use packages.config and NUnit. The [Windows CI workflow](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/windows-net48.yml) declares Windows 2022, NuGet CLI restore, Visual Studio MSBuild, and NUnit executable tests. Its [README](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/README.md) explicitly limits its published 0.1.0 package to Windows/.NET Framework 4.8.

**Observed for this guide:** Source, project configuration and workflow contents were inspected at the named revision. **Not performed:** NuGet restore, compilation, NUnit execution, package installation or runtime testing; a configured workflow is not evidence of a passing latest run. The Windows-specific constraints belong to this product, not every library targeting .NET Framework.

### .NET Binary Tools: modern multi-OS distribution goals

At inspected main revision [3744abdb1e84c212db8ef5cc279ae49acdca8cac](https://github.com/infoconex/dotnet-binary-tools/tree/3744abdb1e84c212db8ef5cc279ae49acdca8cac), Directory.Build.props targets net11.0; global.json specifies SDK 11.0.100 with latestFeature roll-forward. The CLI project configures Native AOT, .NET Tool packing, win-x64/linux-x64/osx-x64 tool package RIDs, and an additional osx-arm64 RID for restore, **not** arm64 packaged support. Its [managed workflow](https://github.com/infoconex/dotnet-binary-tools/blob/3744abdb1e84c212db8ef5cc279ae49acdca8cac/.github/workflows/build-test.yml) declares Windows/Linux/macOS jobs; its [AOT workflow](https://github.com/infoconex/dotnet-binary-tools/blob/3744abdb1e84c212db8ef5cc279ae49acdca8cac/.github/workflows/native-aot-smoke.yml) declares three x64 RIDs and conditionally skips irrelevant changes.

**Observed for this guide:** Source/workflow configuration was inspected. [Merged CAP-004 PR #19](https://github.com/infoconex/dotnet-binary-tools/pull/19) records previously passing managed three-OS and AOT workflows, including [managed run 43810796285](https://github.com/infoconex/dotnet-binary-tools/actions/runs/43810796285) and [AOT run 43810796179](https://github.com/infoconex/dotnet-binary-tools/actions/runs/43810796179), at its final PR candidate SHA ab59a712b346109a243bcab9effed03ae657d62e. These are **prior PR evidence**, not newly executed tests on the inspected main SHA. PR #19 explicitly identifies independent Windows/macOS SDK-free Native AOT consumer execution as still unverified and tracks it under Issue #4. A CI matrix is not an unconditional promise for every version, OS variant, native library or consumer machine.

The existing [playbook reference example](../examples/dotnet-binary-tools.md) separately illustrates research-first RID/dependency locking decisions. Its project-specific architecture, SDK pinning, AOT, RID and CI matrix are not universal playbook rules.

## Applying the guide during AI-assisted adoption

**New project:** From the known project type and actual consumers, propose one suitable supported framework and ordinary SDK-style tooling when possible. Add an OS-specific TFM, extra TFM, RID, native/AOT publishing, dedicated runtime images, or legacy tool only if a real requirement demands it. State which compatibility outcomes should be verified when implementation occurs; do not claim generated or executed evidence that does not exist.

**Existing repository assessment:** Read project files and inherited MSBuild/EditorConfig, package formats and dependency assets, native/OS-specific code, tool resolution, CI job conditions, actual logs/results and consumer contract. Separate observed facts from unknowns, then suggest focused checks or incremental changes where a significant gap affects a real required platform. Do not automatically retarget a supported legacy Framework app, replace packages.config, or add a global.json because modern examples use them.

**Mixed solutions or modernization:** Inventory each compiled project and its transitive constraints. Keep a working Windows-only legacy verification lane if still required while modern components gain separately verified cross-OS paths. Treat source migration, ABI/API preservation, integration behavior and final deployment as separate acceptance risks. When a significant external adapter changes, check conditional [STD-009](standards/testing.md#std-009); for sensitive dependencies and deployment controls, apply [security guidance](security-guidance.md). Preserve the target repository's own decisions and authorization boundaries.

When the user asks “Does this work on Linux/macOS/Windows?” answer with **the exact tested artifact, framework, OS version, architecture, dependencies, operations and observed evidence**, followed by clear untested limits. If only Microsoft platform documentation applies, say “documented as supported under these prerequisites,” not “we tested it.” A useful proposal can be complete without a compatibility questionnaire or executable template.

## Microsoft reference map

- [Target frameworks and OS-specific TFMs](https://learn.microsoft.com/en-us/dotnet/standard/frameworks)
- [.NET Standard contract and Framework compatibility](https://learn.microsoft.com/en-us/dotnet/standard/net-standard)
- [Cross-platform library targeting and multi-target tradeoffs](https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/cross-platform-targeting)
- [.NET releases and lifecycle](https://learn.microsoft.com/en-us/dotnet/core/releases-and-support)
- [.NET SDK/MSBuild/Visual Studio versioning](https://learn.microsoft.com/en-us/dotnet/core/porting/versioning-sdk-msbuild-vs)
- [.NET Framework reference assemblies](https://learn.microsoft.com/en-us/dotnet/framework/migration-guide/reference-assemblies)
- [Framework Windows runtime limitations](https://learn.microsoft.com/en-us/dotnet/framework/install/on-windows-10)
- [global.json and SDK selection](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json)
- [C# language-version mapping](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning)
- [Runtime Identifier catalog and portable graph](https://learn.microsoft.com/en-us/dotnet/core/rid-catalog)
- [Publishing options](https://learn.microsoft.com/en-us/dotnet/core/deploying/)
- [RuntimeIdentifier and self-contained behavior in .NET 8+](https://learn.microsoft.com/en-us/dotnet/core/compatibility/sdk/8.0/runtimespecific-app-default)
- [Native AOT cross-compilation limits](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/cross-compile)
- [Native AOT and RID-specific .NET tools](https://learn.microsoft.com/en-us/dotnet/core/tools/rid-specific-tools)
- [CA1416 platform compatibility analysis](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1416)
- [NuGet package compatibility rules](https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/nuget-package-compatibility-rules)
- [NuGet framework-specific and RID-specific package assets](https://learn.microsoft.com/en-us/nuget/create-packages/supporting-multiple-target-frameworks)
- [NuGet native/runtime assets](https://learn.microsoft.com/en-us/nuget/create-packages/native-files-in-net-packages)

This document is guidance, not a consumer template, executable check, feature announcement, or promise of OS compatibility.
