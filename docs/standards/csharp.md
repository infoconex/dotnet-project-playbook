# Playbook-specific C# engineering standards

Microsoft's published C# conventions, Framework Design Guidelines, language reference, and analyzer documentation are the primary technical authorities. The [Microsoft C# guidance map](../csharp-guidance.md) explains their scope and compatibility. This document defines **only five playbook-owned practices** that strengthen Microsoft guidance or make a necessary choice Microsoft leaves to projects. It does not duplicate Microsoft's naming tables, formatter options, or analyzer rule catalogs.

The [standards governance contract](../governance/standards.md) controls Required, Recommended, and Optional levels, conditional applicability, and exceptions. The [standards catalog](README.md) indexes each permanent ID; this document alone defines their normative expectations. Standards [STD-001 through STD-003](engineering-principles.md) retain their existing authority.

## <a name="std-004"></a>STD-004 — Microsoft-aligned public C# naming

**Level and applicability:** **Required** for newly introduced or intentionally renamed externally visible C# types, namespaces, interfaces, and members in a project using the playbook. This includes public and protected API surfaces. Do not require an existing published API to be renamed solely because it predates the convention.

**Purpose and rationale:** Predictable public API names improve discoverability and interoperation for consumers. Microsoft's [identifier naming conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names) are conventions, not compiler requirements. Making their public-facing patterns Required within this scope is the playbook's deliberate stronger obligation.

**Normative expectation:** Follow the applicable Microsoft naming guidance for new or renamed externally visible identifiers unless an explicitly reviewed and recorded exception is justified. In particular, evaluate the identifier against the guidance for types, interfaces, namespace names, and visible members; this standard does not create a competing playbook naming scheme.

**Implementation guidance:** Review proposed public API names alongside their actual consumers. For example, `IRecordReader` is an interface name consistent with Microsoft guidance, whereas introducing a new public `record_reader` type would not follow the usual C# convention. Follow Microsoft's implementation-symbol guidance for private fields and locals without assigning each convention another standard ID.

**Verification:** Review newly added or renamed public declarations against the Microsoft reference; use configured naming diagnostics such as `IDE1006` where supported. A naming preference displayed in an IDE is not automatically verified by a build. Record the actual editor, analyzer, or review evidence used.

**Exceptions and alternatives:** An unchanged published identifier such as `XMLParser` is outside the new-or-renamed trigger; do not break consumers merely to change its casing. For a **new** public symbol constrained by an external protocol, interop contract, or generated naming scheme, an explicitly reviewed and recorded Required-standard exception may justify the prescribed spelling. If future changes permit a compatible new API, apply the convention there. No consumer naming analyzer configuration is shipped by this standard.

## <a name="std-005"></a>STD-005 — Readability-first C# source organization

**Level and applicability:** **Recommended** for human-maintained C# source where file layout is an intentional design choice, for new files and substantial edits. Existing files need not be mechanically reorganized.

**Purpose and rationale:** Consistent organization makes code easier to find and review. Microsoft documents language structure and example styles but does not establish one universal ordering of every class member. This is a limited playbook preference, not a claim that other valid layouts are incorrect.

**Normative expectation:** Prefer one primary top-level type per source file, named to match that type; group related members and overloads so behavior is easy to follow. Do not prescribe a rigid visibility- or member-kind ordering when it separates related logic or adds noise.

**Implementation guidance:** A primary `RecordProcessor` type would ordinarily live in `RecordProcessor.cs`; a primary `IRecordReader` interface in `IRecordReader.cs`. Choose namespace and `using` forms compatible with the project's configured C# language version; file-scoped namespaces, for example, cannot be assumed in C# 7.3. Refer to Microsoft's [namespaces and using directives](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/program-structure/namespaces) guidance rather than inventing syntax rules.

**Verification:** Inspect representative new or changed files and ask whether the primary type is discoverable, related code remains cohesive, and the selected syntax is supported. Automated formatters generally do not prove that a member arrangement is readable; manual review is valid evidence.

**Exceptions and alternatives:** Small tightly related declarations, nested types, source generators, designer files, partial types, existing organizational conventions, and test-specific layouts may benefit from another arrangement. Under the Recommended obligation, explain an adopted alternative's tradeoff rather than creating an unnecessary exception approval.

## <a name="std-006"></a>STD-006 — Nullable reference types in new compatible projects

**Level and applicability:** **Required** for a new C# project **when** its supported target framework, compiler, language version (C# 8 or later), and build toolchain permit nullable reference types. The compatibility trigger must be evaluated for the actual project; traditional .NET Framework projects that remain on C# 7.3 do not satisfy it.

**Purpose and rationale:** Compiler-assisted null-state analysis helps express API contracts and detect potential dereferences earlier. Microsoft's recent .NET project templates already enable it in applicable contexts; the playbook makes this an explicit, conditional new-project obligation. See Microsoft's [nullable reference types](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/null-safety/nullable-reference-types) reference.

**Normative expectation:** Enable nullable annotations and warnings for new compatible project code; express nullable and nonnullable intent honestly; address the resulting nullable diagnostics instead of broadly disabling the analysis or masking unknown states with indiscriminate null-forgiving operators.

**Implementation guidance:** A genuinely optional parameter can be annotated as `string?` and checked before dereference. A new compatible SDK-style project can typically express this with `<Nullable>enable</Nullable>`, subject to the actual project toolchain. This is a documentation example, not a requirement to install a specific SDK or change an older project's language version.

**Verification:** Inspect the effective compiler language/nullable settings and an actual build's nullable diagnostics in the target project. A project-file setting alone does not prove a clean analysis; do not claim a check passed without running it. The [C# guidance map](../csharp-guidance.md#nullability-and-language-features) illustrates compatible and legacy code paths.

**Exceptions and alternatives:** When an otherwise new project has a genuinely unsupported target or toolchain, this conditional standard does not apply; use language-compatible null validation instead. A justified temporary interop or generated-code boundary can require a reviewed, localized exception. For **existing** compatible applications, Microsoft's [staged nullable migration guidance](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/update-applications/nullable-migration-strategies) is the recommendation; migrating every legacy file is not required by this new-project standard.

## <a name="std-007"></a>STD-007 — Repository-controlled EditorConfig in new C# projects

**Level and applicability:** **Required** for a newly established C# project adopting the playbook. An applicable checked-in `.editorconfig` in the repository hierarchy satisfies the requirement; a duplicate file in every project directory is unnecessary.

**Purpose and rationale:** Shared configuration helps keep editor choices and supported diagnostics reproducible across contributors. Microsoft documents EditorConfig configuration and Visual Studio support, but does not universally require every project to commit one. That requirement is the playbook's additional decision.

**Normative expectation:** Version-control an `.editorconfig` whose scope includes the new project's C# source and expresses selected applicable coding conventions. Do not treat all possible EditorConfig keys as mandatory, or presume that a configured preference is automatically enforced by the build.

**Implementation guidance:** Inspect inherited EditorConfig files and deliberately choose the scope, indentation, line-ending, naming, and relevant analyzer preferences; coordinate text normalization with Git attributes when present. Microsoft's [Visual Studio EditorConfig documentation](https://learn.microsoft.com/en-us/visualstudio/ide/create-portable-custom-editor-options?view=visualstudio) explains generation and editing. The playbook's own root `.editorconfig` governs this documentation repository and is **not** a consumer template.

**Verification:** Review the tracked file and its scope relative to C# source, then inspect effective editor settings with a compatible editor. Where supported, selectively use `dotnet format` or actual diagnostics to check configured behavior; never infer CI enforcement solely from an EditorConfig entry.

**Exceptions and alternatives:** A nested or monorepo project can inherit one applicable tracked file; generated files and established project sections may legitimately use overrides. A new project that cannot use the configuration mechanism requires a reviewed and recorded Required-standard exception identifying its replacement approach. For an **existing** project, review and improve the established configuration incrementally rather than introducing churn; this existing-project adoption is Recommended guidance, not another mandatory standard.

## <a name="std-008"></a>STD-008 — Risk-based compiler and analyzer enforcement

**Level and applicability:** **Recommended** where compiler diagnostics or compatible .NET/IDE analyzers can be reviewed or configured. The available rules, defaults, and enforcement mechanisms depend on the actual toolchain and project type.

**Purpose and rationale:** Compiler errors, compiler warnings, CA quality analyzers, and IDE style analyzers identify different issues. Microsoft provides rule lists and configuration mechanisms, but teams must choose an appropriate enforcement policy. The playbook prefers useful, supportable checks over blanket severity escalation. See Microsoft's [code analysis overview](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview) and [configuration options](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/configuration-options).

**Normative expectation:** Begin with applicable compiler and Microsoft CA analyzer defaults, review newly introduced compiler warnings, and elevate selected high-value CA or IDE diagnostics when their benefit and toolchain support justify the maintenance cost. Prefer IDE suggestions for purely stylistic choices. Avoid a universal warnings-as-errors requirement or blanket `AnalysisMode=All` policy; document material project-specific severity choices and known warning baselines.

**Implementation guidance:** Classify each proposed gate as compiler `CS`, .NET `CA`, or IDE `IDE`; identify the enabled rule set, effective severity, build versus IDE behavior, and tool versions. SDK-provided analyzers are often appropriate for compatible modern SDK-style projects, while traditional non-SDK .NET Framework projects can require version-compatible analyzer packages and different setup. Use rule-specific settings to justify targeted promotion rather than assuming category-level configuration activates every rule. The [Microsoft guidance map](../csharp-guidance.md#compiler-ca-and-ide-diagnostics) explains these distinctions and verification commands.

**Verification:** Examine the actual compiler/analyzer build output and, when available, an IDE or `dotnet format` run for the selected diagnostics. A `dotnet format --verify-no-changes` result measures fixable changes, not all analyzer violations; a green build does not prove IDE-only suggestions were checked. Record tool versions, commands, results, and unverified gaps for the actual project. When CI exists, cross-reference the existing [CI/local parity standard](engineering-principles.md#std-002).

**Exceptions and alternatives:** A well-supported project may deliberately treat selected warnings as errors or use a broader analysis mode; an existing legacy project may maintain a reviewed warning baseline during incremental remediation. Under the Recommended obligation, document the reasons and tradeoffs. Do not mandate an analyzer package, diagnostic ID, or setting incompatible with the consumer's toolchain.

## Scope of this issue

These standards are documentation-only. The [Microsoft guidance map](../csharp-guidance.md) contains reference examples and tool prerequisites, not a consumer-ready `.editorconfig`. Reusable configuration, analyzer dependencies, automation scripts, CI workflows, migration changes, and compatibility experiments are deferred. No compliance or automated verification result is implied by the existence of this documentation.
