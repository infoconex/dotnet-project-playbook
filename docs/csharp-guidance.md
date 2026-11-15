# Applying Microsoft's C# engineering guidance

Microsoft's published language, API-design, coding-style, and tooling guidance is the primary technical reference for C# projects using this playbook. This page helps a developer find and interpret that guidance; it is **not** a second normative rulebook. Only deliberate playbook obligations are defined in the [C# standards](standards/csharp.md) and indexed in the [standards catalog](standards/README.md).

**References reviewed:** November 14, 2026. Recheck the linked Microsoft documentation against the target project's C# compiler, language version, target framework, SDK, MSBuild version, and IDE before applying a recommendation. Documentation of a feature is not evidence that a particular repository supports or verifies it.

## Choosing the appropriate Microsoft reference

| Concern | Primary Microsoft reference | How to use it |
| --- | --- | --- |
| Public .NET API design | [Framework Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/) | Apply to externally consumable APIs, accounting for backward compatibility. |
| C# identifier names | [Identifier naming conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names) | Treat the documented conventions as the baseline; see the [stronger playbook obligation for public names](standards/csharp.md#std-004). |
| General source style | [C# coding conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions) | Distinguish guidance for Microsoft documentation samples from language requirements. |
| Formatting preferences | [C# formatting options](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/csharp-formatting-options) | Choose consistent brace, indentation, spacing, and newline preferences rather than treating them as correctness rules. |
| Namespaces and imports | [Namespaces and using directives](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/program-structure/namespaces) | Use constructs available in the project's C# version. |
| Language features | [C# language versioning](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning) | Check the compiler/target-framework combination before adopting syntax. |
| Nullability | [Nullable reference types](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/null-safety/nullable-reference-types) and [migration strategies](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/update-applications/nullable-migration-strategies) | Separate new compatible projects from existing applications; see [STD-006](standards/csharp.md#std-006). |
| EditorConfig | [Visual Studio EditorConfig guidance](https://learn.microsoft.com/en-us/visualstudio/ide/create-portable-custom-editor-options?view=visualstudio) and [.NET naming rules](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/naming-rules) | Understand scope, supported keys, IDE behavior, and build enforcement; see [STD-007](standards/csharp.md#std-007). |
| Quality and style analysis | [.NET code analysis](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview) and [configuration options](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/configuration-options) | Distinguish analyzer availability, enabled rules, and severity; see [STD-008](standards/csharp.md#std-008). |
| Command-line verification | [`dotnet format`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format) | Check prerequisites and which kinds of fixable findings each subcommand can verify. |

Microsoft's .NET Runtime and compiler repositories may use different project-specific styles from Microsoft's documentation examples. Those repositories are useful implementation examples, not a single universal C# style contract. Where Microsoft offers alternatives, consider existing project conventions and the tradeoffs before choosing; do not create a playbook-wide rule merely to pick one.

## Naming, formatting, and file organization

Microsoft's [identifier guidance](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names) describes PascalCase for types and visible members, `I`-prefixed interfaces, camelCase for parameters and locals, and field patterns such as `_camelCase` for instances and `s_camelCase` for private static fields. Naming conventions are not C# compiler syntax requirements. [STD-004](standards/csharp.md#std-004) makes Microsoft's public-naming conventions a stronger playbook requirement in its stated scope; implementation naming otherwise follows applicable Microsoft guidance.

For formatting, Microsoft's C# examples typically use four-space indentation, Allman braces, and one declaration per line. Keep related whitespace and line-ending settings coherent with the repository's Git attributes and existing conventions. Do not mandate LF or CRLF for every consumer regardless of platform. For example, this is a *style illustration*, not a distributable configuration:

```csharp
public interface IRecordReader
{
    string ReadNext();
}

public sealed class RecordProcessor
{
    private readonly IRecordReader _reader;

    public RecordProcessor(IRecordReader reader)
    {
        _reader = reader;
    }
}
```

The snippet illustrates naming and formatting; actual code should also satisfy the project's nullability and design contracts. The playbook's [source organization preference](standards/csharp.md#std-005) covers one primary top-level type per file, so the two declarations above would normally live in separate files.

For `using` directives and namespace declarations, follow Microsoft's guidance within the supported language version. File-scoped namespaces require C# 10 or later; block-scoped namespaces remain valid and appropriate in C# 7.3 projects. No universal member ordering (such as all public methods before all private methods) is required. Prefer discoverability and grouping of related functionality without mechanically reordering legacy code.

## Nullability and language features

Nullable reference types are a C# 8 feature: annotations communicate intent and compiler analysis reports potential null-state problems. New projects using supported language and framework/toolchain combinations must follow [STD-006](standards/csharp.md#std-006). New .NET 6+ templates normally enable nullable analysis, but that template default does not establish compatibility for every historical project.

For an existing application, Microsoft's [migration guidance](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/update-applications/nullable-migration-strategies) recommends planning and incremental adoption. File-level `#nullable` directives can be temporary migration tools; avoiding warnings by scattering `!` operators is not a substitute for establishing actual contracts. Do not classify a C# 7.3 project as noncompliant for lacking nullable reference annotations.

```csharp
// For a compatible C# 8+ project with nullable annotations enabled.
public static string DisplayName(string? name)
{
    return string.IsNullOrWhiteSpace(name) ? "Unknown" : name.Trim();
}
```

For C# 7.3, write appropriate defensive checks without using unsupported nullable-reference syntax. This example documents behavior rather than claiming compiler-assisted nullable analysis:

```csharp
public static string DisplayName(string name)
{
    return string.IsNullOrWhiteSpace(name) ? "Unknown" : name.Trim();
}
```

Favor clarity over either novelty or unnecessary verbosity. Microsoft's C# conventions encourage modern features when appropriate, but constructs such as target-typed `new()`, file-scoped namespaces, and collection expressions have their own version requirements. Do not globally force `LangVersion=latest` simply to use newer syntax on an older target; consult [language versioning](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning) first.

## EditorConfig and severity configuration

An applicable `.editorconfig` travels with the repository and overrides relevant developer-specific editor preferences. Visual Studio can generate an EditorConfig from its current code-style settings, and the file can be edited directly. A new C# project must have a checked-in applicable configuration under [STD-007](standards/csharp.md#std-007); an existing project should review and improve its current configuration before considering broader changes.

As a *partial illustration only*, not a consumer template:

```ini
root = true

[*.{cs,csx}]
indent_style = space
indent_size = 4
```

Editor settings, analyzer preferences, and actual build enforcement are distinct. A naming rule's `dotnet_naming_rule.*.severity` primarily describes IDE behavior; the naming diagnostic is `IDE1006`, and build enforcement requires supported rule-level severity configuration and code-style analysis enabled on build. The details vary with the SDK/analyzer version. Follow [Microsoft's naming rules documentation](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/naming-rules) rather than assuming an IDE suggestion is a CI failure.

For individual analyzer severities, Microsoft documents `dotnet_diagnostic.<rule ID>.severity`; broader category/all-rules configuration has different precedence and limitations. An `AnalysisMode` or `AnalysisLevel` selection can change which CA rules are enabled, and bulk EditorConfig severity does not necessarily activate rules disabled by default. Prefer [risk-based selection](standards/csharp.md#std-008) to copying a blanket setting without reviewing its effects.

## Compiler, CA, and IDE diagnostics

| Diagnostic family | Responsibility | What can be observed |
| --- | --- | --- |
| Compiler `CS` | Language/type checking, compiler warnings, and nullable-flow warnings when enabled | Build diagnostics; compiler options control warning treatment. |
| .NET analyzer `CA` | Reliability, performance, security, design, interoperability, and other code-quality analysis | When a compatible analyzer is available and the rule is enabled, diagnostics may appear in IDE/build with configured severity. |
| IDE analyzer `IDE` | Naming, formatting, style, and language-expression preferences | Often IDE hints or code fixes; build enforcement is separately configured and some rules remain IDE-only. |

Modern .NET SDK-style projects targeting .NET 5 or later generally receive SDK-bundled .NET analyzers by default. For earlier targets and especially **traditional non-SDK .NET Framework projects**, analyzer activation and packages may require additional, version-compatible setup. Microsoft documents a `Microsoft.CodeAnalysis.NetAnalyzers` package path and different properties for legacy non-SDK projects; do not assume SDK-only `AnalysisLevel` settings work there. Verify the actual project style, MSBuild imports, package integration, compiler, and analyzer version before claiming coverage.

The playbook does not prescribe a universally enabled CA rule list or `AnalysisMode=All`. An analyzer's availability, enabled state, severity, and verified execution are separate facts. The broader [evidence-based decision principle](standards/engineering-principles.md#evidence-based-technical-decisions) applies when selecting an analyzer policy.

## Visual Studio and command-line verification

In Visual Studio, inspect the project-applicable EditorConfig, Code Style options, Code Cleanup, and the Error List. Distinguish design-time suggestions from diagnostics emitted by an actual build. Visual Studio versions and installed analyzers can affect available settings and diagnostics.

For a compatible .NET 6 SDK or later, Microsoft's `dotnet format` documentation describes separate verification scopes. Replace `<project-or-solution>` with a real, loadable project or solution path before running the commands:

```shell
dotnet format whitespace <project-or-solution> --verify-no-changes
dotnet format style <project-or-solution> --verify-no-changes
dotnet format analyzers <project-or-solution> --verify-no-changes
```

`whitespace` addresses formatting, `style` addresses supported style fixes, and `analyzers` addresses supported non-style analyzer fixes. The default diagnostic severity threshold is `warn`; use an appropriate `--severity` value (such as `info` for included suggestions) and optional diagnostic filters when a narrower or broader check is intentional. Consult the installed tool's help for its exact accepted options.

`--verify-no-changes` exits nonzero when the formatter would change source; it is **not** a complete proof that all compiler/CA/IDE diagnostics passed. Some diagnostics are not fixable by `dotnet format`, and a project may have build or restore problems before formatting begins. Combine supported formatter checks with actual build diagnostics and other relevant verification instead of claiming all analyzers passed.

The presence of a .NET SDK alone does not prove that an older non-SDK project can be restored and loaded by `dotnet format` in that environment. Do not claim Visual Studio/CLI equivalence or cross-platform success without observed project-specific evidence. When validation is automated later, the existing [CI/local parity standard](standards/engineering-principles.md#std-002) supplies the repository-controlled-check guidance; this issue does not ship scripts or workflows.

## Applying guidance and reporting exceptions

For a new project, start with Microsoft conventions and the applicable [playbook standards](standards/csharp.md). For an existing project, inspect source, public contracts, EditorConfig, language/framework settings, and available analyzers before proposing changes. A style difference is not automatically a defect.

For example, renaming an existing public `XMLParser` type solely to change its casing could break source or binary consumers. An unchanged published identifier is outside [STD-004's](standards/csharp.md#std-004) new-or-renamed trigger; preserve the API rather than silently making a breaking rename. If a **new** interoperability-bound public identifier must instead use spelling dictated by an external contract, record a reviewed exception to STD-004 with the contract and compatibility rationale.

This documentation is guidance only. No reusable consumer EditorConfig, analyzer package, compatibility test, or executable validation asset is shipped here.
