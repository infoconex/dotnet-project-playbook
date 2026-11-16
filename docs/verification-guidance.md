# Automated verification, code coverage, and CI/local parity

This is an **on-demand, non-normative guide** for choosing and evaluating verification in new and existing .NET repositories. It does not prescribe a universal CI pipeline, test framework, coverage percentage, script, or package. The [engineering principles](standards/engineering-principles.md), [standards governance](governance/standards.md), and [standards catalog](standards/README.md) remain authoritative. **STD-002** owns CI/local parity, **STD-001** owns test-first behavior, **STD-008** owns compiler/analyzer severity, **STD-009** owns consequential external-boundary verification, **STD-019–STD-021** own security obligations, and **STD-022** owns significant requirements-to-acceptance evidence relationships.

**Central principle:** Prefer the simplest supported verification that gives meaningful, reproducible confidence in the project's actual risks and accepted outcomes. A configured check is not evidence it ran; a green build does not prove tests or acceptance; a clean scan is not proof of security.

**References reviewed:** November 16, 2026 (America/Los_Angeles). Recheck the official documentation and installed SDK, MSBuild, NuGet, test runner, platform and service behavior before applying version-specific examples. No command or illustrative project below was executed by **this playbook repository**; it currently has no executable validator or CI workflow.

## Start with the change and its risks

For a new project, identify intended executable behavior, relevant target frameworks, consumer OS/architecture, external systems, distribution method, sensitive data and meaningful quality commitments. Choose the smallest checks that would credibly verify those claims; do not pre-install a test/coverage/security stack for hypothetical future features.

For an existing repository, inspect its actual source revision, project and solution formats, test projects, test discovery and runners, build scripts, GitHub workflows, configuration, prior decisions, security settings and recent **observed** check outcomes. Distinguish an absent check from one that cannot be accessed, one whose trigger does not apply, and one supplied by a different service. Reuse appropriate existing commands rather than forcing migration.

A verification method is useful when it answers a separate question at an acceptable cost. Examples:

- **Restore** answers whether the relevant dependencies can be resolved with the selected sources and client; it does not establish that dependencies are secure.
- **Build** establishes compilation and configured build diagnostics for the selected configuration, targets and SDK; it does not establish executable or packaging correctness.
- **Behavioral tests** show the scenarios actually discovered and executed in their specified environments; isolated tests cannot prove real-provider fidelity.
- **Formatting and analyzers** answer different questions: a formatter's ability to make changes is not a complete compiler/analyzer review.
- **Coverage** identifies instrumented code executed during the selected tests, not the correctness of assertions or requirements.
- **Security tools** provide findings within their own supported language, dependency, secret, or runtime scope; architectural and risk review remains necessary when applicable.
- **Publishing and smoke tests** provide distribution-specific evidence that ordinary build and test commands may not supply.

Avoid routinely running separate restore and build commands *in addition to* a command that already performs those operations, unless the separation gives useful failure diagnosis, caching, policy, or independent evidence. Similarly, one suite may satisfy several acceptance scenarios, and a manual review may evaluate a constraint that no available automated tool can establish.

## Applicability matrix

Interpret obligation levels using [governance](governance/standards.md): **Required** only where an existing applicable standard, principle or accepted project requirement triggers the obligation; **Recommended** means a default with a justified alternative; **Optional** is genuinely discretionary. The matrix suggests *methods*, not independent new permanent standards. Local feasibility refers to a compatible developer environment; CI feasibility refers to a properly provisioned runner or service, **not** evidence that it has been configured or executed.

| Expectation / level | Conditions that justify it | Suitable mechanism | Prerequisites / local and CI feasibility | Evidence produced and important limits | Valid omission or alternative |
| --- | --- | --- | --- | --- | --- |
| Dependency restore — supporting Required executable verification | Package inputs must be resolved for meaningful compilation/test/distribution | Supported dotnet, MSBuild, or NuGet restore; optionally locked mode where already chosen | Actual feeds, credentials, tool/client and project format; **local:** usually yes if reachable; **CI:** yes when provisioned | Restored graph and errors at this revision; not full reproducibility or vulnerability freedom | No restore required for genuinely dependency-free/documentation-only changes; a combined native command may restore |
| Compilation/build — Required principle for meaningful executable changes | C# or build behavior is new or materially modified | dotnet build or compatible MSBuild, configuration and TFM | SDK/Build Tools, workloads and targeting packs; **local:** compatible host; **CI:** compatible runner | Compiler/build success, outputs and enabled diagnostics for selected configuration; no runtime acceptance | Pure documentation-only changes; reused build inside a verified test/publish operation when sufficient |
| Unit tests — STD-001 Required where applicable | Test-first new executable behavior/defect correction at a useful isolated boundary | Compatible framework, adapter and test platform | Test host/runtime, dependencies; **local/CI:** usually yes when compatible | Executed behavioral assertions; not external integration or proof of red-first chronology from a final green run | Different smallest meaningful test boundary; reviewed STD-001 exception when justified |
| Component tests — Recommended when useful | Multiple collaborators/use cases need controlled in-process verification | Run controlled component fixture through public boundary | Host and test doubles; **local/CI:** normally yes | Behavior of the composed component; substitutes do not prove real dependencies | A pure cohesive unit or adequate existing tests already provide confidence |
| Integration tests — STD-009 Required when triggered; otherwise risk-based | Significant new/changed external-adapter correctness, compatibility, integrity, security or reliability risk | Execute real dependency and representative success/failure cases | Database, filesystem, network, service, version and isolated test data; **local:** sometimes; **CI:** if environment available | Actual exercised provider/configuration behavior; not all production settings | Validated provider contract or reviewed exception with residual risk under STD-009 |
| Contract tests — conditional route under STD-009; otherwise Recommended when useful | Independently evolving producer/consumer schema or protocol | Consumer/provider agreement validated against the provider | Compatible contract fixture/service; **local/CI:** depends on provider access | Contract compatibility for validated scope; fake-only contract does not prove real provider | Shared in-process code with no independently evolving contract |
| Acceptance and quality-scenario verification — based on accepted commitments | Stakeholder-visible behavior or measurable reliability/performance/compatibility requirement | Executable acceptance test, benchmark, representative manual evaluation | Agreed workload, environment, oracle, thresholds; **local/CI:** as context allows | Evidence for explicitly exercised outcomes; an acceptance document alone is not execution | No separate ceremony for a small issue/test/PR; STD-022 governs significant traceability |
| Formatting — Recommended when enforceable and valuable | Tracked style policy and compatible formatter, particularly new/revised source | dotnet format whitespace/style/analyzers --verify-no-changes as supported | Loadable project/tool, effective EditorConfig, compatible SDK; **local/CI:** when supported | Fixable differences at selected severity; not all analyzer or IDE-only diagnostics | Legacy incompatible tool; IDE/manual review or project-specific formatter |
| Compiler diagnostics — build errors block; warnings under STD-008 | Compile or configured diagnostic policy applies | Actual compiler/MSBuild output at specified severity | Effective language version/configuration/analyzers; **local/CI:** compatible toolchain | Emitted errors/warnings only; no evidence about disabled or IDE-only rules | No separate warnings-as-errors gate without justified project policy |
| Static analyzers — STD-008 Recommended | Compatible rules could catch significant correctness, maintainability or API problems | SDK analyzers or version-compatible Roslyn/IDE analyzers | Analyzer availability and effective settings; **local/CI:** varies for legacy IDE rules | Findings for enabled IDs/severity; scan silence not proof of design correctness | Unsupported legacy tooling or review of selected rules without blanket packages |
| Code coverage — Optional unless a specific quality policy requires it | Uncovered critical paths, refactoring risk or useful comparable trends | Microsoft Code Coverage, dotnet-coverage, compatible Coverlet/reporting | Matching collector/test runner, symbols, instrumentation; **local/CI:** platform/tool-dependent | Executed lines/branches/methods where supported; not assertion or requirements quality | No actionable coverage need, incompatible collector, unjustified overhead |
| Dependency vulnerability analysis — STD-020 Required conditionally | Third-party packages/tools/components are present | NuGet Audit, GitHub Dependabot alerts, other supported ecosystem review | Package graph, advisory access and supported client; **local:** NuGet if compatible; **CI/service:** configured capability | Recognized known vulnerabilities at scan time; not a clean bill of health | No third-party dependencies; unsupported audit client requires alternative risk review, not silent exemption |
| SAST / secret scanning / DAST — risk-selected supporting methods | Relevant language, credentials, reachable app, threats, compliance or security-sensitive change | GitHub CodeQL/secret scanning, suitable static or dynamic checks | Repository/service setup or safe running target; **local:** tool-dependent; **CI/service:** available if configured | Pattern/advisory/dynamic findings limited to scan scope; no proof of overall security | No runnable service for DAST; unsupported language; proportionate other evidence |
| Platform-specific behavior — required to support material platform claims | OS APIs, native dependencies, TFM/RID, architecture or compatibility requirement matters | Select OS/architecture/TFM tests and real runtime/consumer execution | Appropriate host/runner, target runtime and native dependencies; **local:** sometimes; **CI:** OS matrix when provisioned | Only the exercised environment/operation; build on one host is not universal portability | No cross-platform contract; document excluded unsupported environments |
| Package, publish, install and launch — context-dependent Required verification | Distributed binary, NuGet package, Native AOT, deployed app, signing or release artifact | Native pack/publish followed by artifact/installation/smoke verification | Chosen RID/OS/workloads, packaging and consumer host; **local/CI:** according to distribution | Actual artifact or launch behavior for selected target; build success alone insufficient | A pure library change not producing or changing a distribution artifact |
| Manual engineering/security review — contextual, STD-021 Required where triggered | Design/requirements constraints beyond automated checks; material security-sensitive changes | Recorded peer/owner review, risk/boundary analysis and disposition | Competent reviewer and accessible evidence; **local:** human; **CI:** cannot automatically substitute | Reviewed scope and findings, not an executed runtime test | No separate security review for changes outside STD-021 trigger; normal code review may suffice |

Do not impose a universal per-commit pipeline. A project may use fast PR checks and additional scheduled, manual, release-only, or environment-specific checks. When a required outcome lacks its necessary verification, record the gap or reviewed exception rather than calling an absent conditional check a defect by default.

## CI/local parity and orchestration

[STD-002](standards/engineering-principles.md#std-002) recommends reusing the same verification operations locally and in CI when CI exists. Direct native commands are often sufficient; a repository-controlled script can improve reproducibility for complex, multi-step, argument-sensitive checks. No shell, wrapper, programming language, or CI engine is a universal prerequisite.

**Repository-owned operations:** select the projects/targets, restore and build, execute chosen tests, run formatting/analyzer checks, collect justified coverage, and validate project-specific constraints.

**CI orchestration:** provision supported tools and OS/architecture; invoke the repository's operations; apply explicit selection/triggers and permissions; capture stdout, test/coverage reports and exit results; publish artifacts; enforce adopted quality gates.

The underlying operation can be equivalent even when the environments differ. A Windows-only Framework test command can be reproducible on a Windows developer machine and hosted Windows runner without requiring Linux equivalence. Record differences in SDK, working directory, environment variables, package feeds, secrets, configuration, runtime and architecture. Never treat a script existing in a repository as proof it was executed by CI.

**GitHub-managed exceptions:** hosted CodeQL analysis, Dependabot advisories/security update PRs, secret scanning and similar services cannot always be captured in one local command. Inspect their enablement, actual latest/commit-specific run or alert status, supported analysis scope, and permissions separately. The presence of a workflow file, branch rule or security settings page is configuration evidence, not an observed pass.

**GitHub required-check nuance:** A conditionally **skipped job** can report success for branch protection while executing no underlying verification. A **workflow skipped** because of path, branch or commit-message filtering can leave a required check pending. Required-check evaluation therefore does not replace review of relevant steps and their actual conclusions. If using merge queues, required workflows need appropriate merge-group triggers; none is introduced by this guide. See [GitHub status checks](https://docs.github.com/en/pull-requests/reference/status-checks), [conditional jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions) and [required-check troubleshooting](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

## Selecting .NET test platforms and commands

A test **framework** defines tests (such as NUnit, MSTest, xUnit); a test **platform** discovers, executes and reports them. Microsoft documents VSTest and Microsoft.Testing.Platform (MTP) as distinct choices. Match framework adapters, test host, SDK, project format and reporting extensions. Do not mix VSTest-only and MTP-only test projects in the same invocation/configuration.

For compatible SDK-style projects, VSTest is the default dotnet test mode. Native MTP mode is supported starting with .NET 10 SDK and requires a compatible MTP version (at least 1.7 for that integration). Select the runner intentionally where useful; options, coverage extensions and result reporting are runner-specific. Installing the newest SDK does not convert an existing traditional Framework project into an MTP test application. See [test-platform comparison](https://learn.microsoft.com/en-us/dotnet/core/testing/test-platforms-overview), [dotnet test](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test), [VSTest mode](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test-vstest) and [MTP mode](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test-mtp).

For **modern SDK-style VSTest** projects, representative operations (substitute actual paths; none run here):

~~~shell
dotnet restore MySolution.sln
dotnet build MySolution.sln --no-restore
dotnet test MySolution.sln --no-build --logger trx
~~~

For a **compatible MTP configuration**, command options and reporting extensions differ; e.g. dotnet test may forward MTP-specific options after the separator. Do not paste VSTest switches into MTP mode unexamined.

For a **traditional non-SDK .NET Framework** repository, begin with the actual legacy build and test setup, not a presumed modern CLI invocation. On an appropriate Windows developer/build-tools machine:

~~~powershell
nuget restore Legacy.sln
msbuild Legacy.sln /p:Configuration=Release
vstest.console.exe .\Tests\bin\Release\Legacy.Tests.dll /Logger:trx
~~~

The above assumes packages.config restoration and a VSTest-compatible adapter/test assembly. Traditional PackageReference projects ordinarily use MSBuild restore. MSBuild 16.5+ documents a packages.config restore option, but its availability does not imply the rest of a legacy solution is portable. Framework developer/targeting packs, tool imports, bitness, COM/WindowsDesktop tasks, installed runtime and adapters must be checked; use the existing [build guide](build-dependency-guidance.md) and [platform guide](platform-compatibility-guidance.md). See [NuGet restore](https://learn.microsoft.com/en-us/nuget/consume-packages/package-restore), [Framework reference assemblies](https://learn.microsoft.com/en-us/dotnet/framework/migration-guide/reference-assemblies), and [VSTest.Console](https://learn.microsoft.com/en-us/visualstudio/test/vstest-console-options?view=vs-2022).

SDK-style .NET Framework code may be compilable on a supported non-Windows environment with appropriate references, but Microsoft's .NET Framework runtime executes on Windows. In mixed solutions, a successful build/test of one modern project does not certify the traditional projects, solution-wide imports or Windows-only components.

Always check test discovery and execution counts. A successful command with zero discovered tests, unintentionally filtered tests or an absent test host can leave the intended behavior unverified. Distinguish skipped test cases from passing cases and record unexpected discovery reductions.

## Code coverage as diagnostic evidence

Coverage measures which selected, instrumented code executed during specific tests. It does **not** prove correct assertions, acceptance requirements, failure handling, SOLID design, security or cross-platform behavior. Microsoft's [coverage overview](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-code-coverage) and [unit-test best practices](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices) support that distinction.

| Metric | What it can reveal | What it cannot establish |
| --- | --- | --- |
| Line | Whether countable instrumented source lines executed | Every expression or condition on that line was meaningfully tested |
| Branch | Whether measured decision outcomes/branches executed | Every business scenario, state, assertion, or path combination was correct |
| Method/function | Whether an instrumented method was entered, when the collector/report supports the metric | Meaningful method assertions, all internal branches or correct public behavior |

First evaluate the collection/reporting capabilities already supplied or supported by the selected Microsoft runner/toolchain:

1. **VSTest Code Coverage collector / Microsoft.CodeCoverage:** For compatible installations, the collector named "Code Coverage" can collect .coverage and supported XML/Cobertura outputs, with runsettings where needed.
2. **dotnet-coverage:** A .NET global/local tool for supported collection, merging and format conversion. Check tool version, instrumentation modes and platform compatibility before choosing it.
3. **MTP extension:** Microsoft.Testing.Extensions.CodeCoverage supports MTP-specific --coverage options, output selection and collector registration with the appropriate package/version.
4. **Visual Studio coverage:** Available measurements and UI/reporting depend on the actual Visual Studio edition/version. Do not assume features from a newer Visual Studio version exist in an older installation.
5. **Alternatives:** Coverlet (including VSTest's "XPlat Code Coverage") and ReportGenerator can be useful, including HTML rendering, but are not mandated. Validate editions/licensing, supported metrics, format imports and maintenance before depending on advanced or paid features.

See [dotnet-coverage](https://learn.microsoft.com/en-us/dotnet/core/additional-tools/dotnet-coverage), [MTP coverage](https://learn.microsoft.com/en-us/dotnet/core/testing/microsoft-testing-platform-code-coverage), [Visual Studio coverage](https://learn.microsoft.com/en-us/visualstudio/test/using-code-coverage-to-determine-how-much-code-is-being-tested) and [customizing code coverage](https://learn.microsoft.com/en-us/visualstudio/test/customizing-code-coverage-analysis).

For a compatible VSTest collector, one illustrative command is:

~~~shell
dotnet test MyTests.csproj --collect:"Code Coverage"
~~~

For a compatible **MTP** setup with the Microsoft coverage extension, an illustrative invocation is:

~~~shell
dotnet test -- --coverage --coverage-output-format cobertura
~~~

These examples are **alternatives**, not compatible synonyms. The required packages, options, test selection and output paths must be checked before use. For multiple MTP test modules, an explicit common output filename can overwrite coverage reports even when the command succeeds; preserve distinct per-module outputs before any merge.

Coverage comparisons need a stable denominator: same relevant source revision or a well-explained changed-code comparison, consistent test selection/configuration, symbols, instrumentation, exclusions and tool versions. Include/exclude test assemblies, third-party libraries and generated code deliberately. Source generators and synthesized methods, optimization, missing PDBs, inlining, native instrumentation and report conversion may alter which lines, branches or functions are countable. Record method/function support only after inspecting the actual collector's output, not by assuming every coverage format or free report UI supports it.

**Native AOT:** Ordinary managed tests run under the development runtime; publishing with Native AOT creates a native executable with different verification and instrumentation boundaries. Use relevant publish, install, launch and smoke tests for the AOT distribution, and report managed-code coverage only for the process it measured. Native binary coverage requires its own compatible collector/instrumentation and environment; do not infer that it exists because managed unit coverage succeeded. See [Native AOT diagnostics](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/diagnostics).

**Thresholds:** No universal numerical coverage minimum exists in this playbook. Examine uncovered consequential behavior, negative paths and change-associated regressions first. If a project adopts a numeric gate, record its accepted risk/quality rationale, reliable baseline, comparable metric and exclusions, failure action, and owner. Do not optimize percentages by suppressing meaningful untested code or adding assertion-free tests.

## Failure policies, skip handling and exceptions

Assign each selected check a policy independently of its operational result:

| Policy | Appropriate behavior |
| --- | --- |
| **Required and applicable** | Resolve execution failures and verification gaps before accepting the change, or obtain the existing standard's scoped reviewed exception |
| **Advisory** | Expose actionable findings and rationale; do not silently transform them into build failures |
| **Informational** | Measure and retain evidence for discussion without a default blocking threshold |
| **Experimental** | State the hypothesis, limited confidence and temporary non-blocking status; promote only after the check becomes reliable and valuable |
| **Environment-dependent** | Assign designated OS/provider/runtime verification; show which other environments cannot execute it |
| **Known exception** | Retain scope, approver/owner, reason, alternative evidence, residual risk and follow-up; do not generalize to unrelated changes |
| **Unavailable** | Preserve failure-to-execute diagnostics and decide whether applicable Required evidence can be supplied elsewhere or needs reviewed exception |

Compilation errors, actual failing Required tests and failures of selected material quality gates normally block. Compiler warnings, CA/IDE severities and formatter policies are governed by [STD-008](standards/csharp.md#std-008). Vulnerability remediation/disposition is governed by [STD-020](standards/security.md#std-020). Material security review is governed by [STD-021](standards/security.md#std-021). A fixed warnings-as-errors switch, every CodeQL warning or any coverage delta must not automatically become a universal merge blocker.

Treat flaky tests as unreliable evidence needing diagnosis, isolation and ownership. A rerun's green result does not make the initial failure disappear; record both, any root cause, quarantine scope and follow-up. Report deliberately skipped tests and unsupported environments without calling them passing or globally defective. For missing access, misconfigured runners, rate limits or infrastructure failures, distinguish inability to verify from an actual product failure and from an authorized exception. The need for environment-specific verification can be material even when it cannot reasonably execute on every commit.

## Verification results and provenance

For consequential claims, record these fields **in the project's authoritative PR, CI run/artifact, test results or review record**, not synchronized copies across permanent documentation indexes:

| Field | Record |
| --- | --- |
| Identity | Repository, exact candidate commit SHA, relevant project/TFM/configuration |
| Expectation | Purpose, acceptance claim or standard trigger, selected check and applicable policy |
| Toolchain | SDK, MSBuild/NuGet/runner/collector versions when relevant |
| Environment | OS/version, architecture/RID, runtime, CI runner or local host, material external dependency versions |
| Operation | Actual command/test selection or manual procedure, with configuration and meaningful inputs |
| Observed result | Execution status, exit/result, discovered/executed/passed/failed/skipped counts when available |
| Provenance | Immutable or revision-specific CI run, log, TRX, coverage artifact, review or local transcript reference |
| Boundary | What did not execute, unsupported environments, exclusions, advisory findings, unavailable infrastructure and follow-up |

Six reporting outcomes must remain distinct:

| Outcome | Interpretation |
| --- | --- |
| **Passed** | Selected relevant verification genuinely executed and met its criteria in the recorded environment |
| **Failed** | Verification executed but its required criteria were not met; separately investigate product versus infrastructure cause |
| **Skipped** | A known check/case was intentionally not executed; record the reason and applicability; not a behavioral pass |
| **Unavailable** | Execution was attempted but blocked by infrastructure, dependency access or missing tools; behavior remains unverified |
| **Manually reviewed** | An identified reviewer inspected a defined scope; record findings and approval/deferral, not merely this status |
| **Not executed** | No run or review attempt occurred; planned/configured/absent checks cannot supply observed evidence |

For manual reviews, the review **method** and reviewer's conclusion are separate concepts: a manually reviewed change may reveal a defect or unresolved risk. A GitHub check conclusion of success, skipped or neutral is a platform merge-management signal, not a substitute for underlying execution evidence. CI artifacts can expire; retain the necessary evidence reference and material conclusion with appropriate provenance, and avoid claiming unavailable details later.

Example report skeleton (all placeholders; **not an observed run**):

| Field | Illustrative entry |
| --- | --- |
| Repository/revision | example/portable-library @ [exact 40-character SHA needed] |
| Environment/tool | Windows x64; SDK and NUnit adapter versions [to be recorded] |
| Operation | dotnet test Example.Tests.csproj --no-build |
| Intended scenario | Clamp request below first page returns first page |
| Result | **Not executed** — demonstration only; no test was run |
| Evidence | No CI run, TRX or local transcript |
| Boundary | No compilation, runtime, Framework consumer, Linux/macOS, security or acceptance evidence |

When a check genuinely executes, replace the placeholders with actual values; never retain an example's unobserved "passed" result. A green build does not demonstrate acceptance tests; a test pass on one OS is not a universal cross-platform pass; a coverage report is not a correctness certificate. For accepted requirements and significant scenarios, keep the [STD-022 relationship](standards/requirements.md#std-022) to the actual evidence or explicit gap.

## Two contrasting project profiles

### A. Small pure C# library — hypothetical

Assume a cohesive SDK-style C# library with no external dependency, network service, native assets, deployment host or promised multi-platform runtime behavior. Its meaningful next change corrects a paging boundary. Suitable verification might be:

- Under [STD-001](standards/engineering-principles.md#std-001), record the failing regression example, correct implementation, and observed tests; the pre-fix red result is not inferable from the final passing suite.
- Use a compatible dotnet build/test operation and record SDK, NUnit or other selected runner, target framework, discovered/executed results and revision.
- Apply configured formatting/diagnostics when supported, with [STD-008](standards/csharp.md#std-008) determining useful severities.
- Add coverage **only** if uncovered branches or historical changes help choose tests; do not create a blanket threshold or report-generator dependency.
- Do not invent database integration tests, DAST, publishing smoke, multi-RID AOT, secrets vault or OS matrix when the relevant triggers/requirements are absent.

The [testing guide's pure-library example](testing-guidance.md#example-a--a-pure-c-library) supplies illustrative NUnit-style behavior. Its code was not compiled by this playbook.

### B. Multi-platform inspection CLI — inspected historical reference

The [.NET Binary Tools reference](../examples/dotnet-binary-tools.md) demonstrates justified expansion: multiple project responsibilities, untrusted file parsing, cross-platform x64 distribution, Native AOT and .NET Tool packaging, security-relevant file/resource limits and a historical coverage report.

For **CAP-005 PR #21**, I inspected the merged PR record, its final head **07fe6ddb41236774e04829cbff2a94f26fad64b1**, repository workflow definitions, and [recorded managed build/NUnit job steps](https://github.com/infoconex/dotnet-binary-tools/actions/runs/43826359144) and [Native AOT job steps](https://github.com/infoconex/dotnet-binary-tools/actions/runs/43826359218) for that final candidate. The recorded managed validation, NUnit/coverage and reporting steps succeeded on Windows, Linux and macOS. The recorded AOT publication/smoke steps also succeeded on all three; SDK-free Linux consumer and lock-drift steps executed successfully on Linux, while those Linux-specific steps were **skipped** on other runners.

These are **historical GitHub Actions observations linked to one exact candidate**, not checks run during Issue #11, not new live CI assertions, and not general claims about future CAP-006 or other commits. Some steps are intentionally skipped while a job is successful; the pass scope is the operations actually executed in the named environments. The reference project's specific scripts, matrix, custom reporting and coverage counts are engineering choices, not minimum requirements for a new .NET project. Do not copy their mutable CI status into the standards catalog.

## Security, workflow and release boundaries

Treat dependency advisories (SCA), source-based SAST/CodeQL, secret scanning, DAST of a safely reachable application, real-boundary behavior tests, human security review, and artifact-provenance checks as different questions. Choose those applicable to the project; never equate no scanner findings with an absence of vulnerabilities. [STD-019–STD-021](standards/security.md) own material controls, vulnerability disposition and security-sensitive reviews; the [security guide](security-guidance.md) describes tool tradeoffs.

CI workflows themselves are a trust boundary. Evaluate least-privileged GITHUB_TOKEN permissions, explicit secret access, untrusted PR content, dependency/action provenance, publishing credentials and separation between untrusted validation and privileged release operations. In particular, do not run untrusted PR code with credential-bearing pull_request_target permissions; see [GitHub's security guidance](https://docs.github.com/en/actions/reference/security/secure-use) and [pull_request_target precautions](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target). No security settings or workflows are changed by this guide.

A packaging or publication check must describe the *actual* artifact and consumer environment it exercised. Successful test, pack or publish operations are different evidence: a Native AOT executable must be published before its native runtime behavior can be verified; package structure, installation, launch, signing and provenance require their own checks when material to the distribution contract. Never describe a pending release or planned workflow as executed.

## Applying the guide through AI-assisted adoption

Use [start-here](../start-here.md) as the only authoritative conversational process. For a new-project foundation, propose a compact verification strategy covering actual known technology and risk; defer unrelated feature tests until meaningful requirements emerge. For an existing repository, inventory what is truly configured and observed before suggesting amendments. Distinguish **satisfied, gap, partial, approved exception, not applicable and unknown** when producing an assessment under the planned [Issue #12 contract](https://github.com/infoconex/dotnet-project-playbook/issues/12); do not claim that contract is already implemented.

Present an actionable next check or a risk-qualified omission when evidence is missing. Never require a fixed questionnaire, a specific CI vendor, a mandatory test framework, a coverage percentage or optional checks whose triggers do not apply. Require explicit authorization before changing a consumer repository.

## Official reference map and document boundary

- [.NET testing fundamentals](https://learn.microsoft.com/en-us/dotnet/core/testing/); [dotnet test](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test); [VSTest and MTP comparison](https://learn.microsoft.com/en-us/dotnet/core/testing/test-platforms-overview).
- [Unit testing best practices](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices); [VSTest.Console](https://learn.microsoft.com/en-us/visualstudio/test/vstest-console-options?view=vs-2022).
- [Code coverage for testing](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-code-coverage); [MTP coverage](https://learn.microsoft.com/en-us/dotnet/core/testing/microsoft-testing-platform-code-coverage); [dotnet-coverage](https://learn.microsoft.com/en-us/dotnet/core/additional-tools/dotnet-coverage).
- [dotnet format](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format); [.NET analyzers](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview); [NuGet auditing](https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages).
- [NuGet restore](https://learn.microsoft.com/en-us/nuget/consume-packages/package-restore); [MSBuild](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild); [.NET releases and support](https://learn.microsoft.com/en-us/dotnet/core/releases-and-support).
- [GitHub Actions](https://docs.github.com/en/actions); [GitHub status checks](https://docs.github.com/en/pull-requests/reference/status-checks); [GitHub CodeQL](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning); [Dependabot alerts](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts).

This Issue #11 change delivers **documentation only**. It adds no test projects, executable validator, CI workflow, coverage tooling, automation, package or consumer template. Any later claim of successful compilation, test, coverage, release or cross-platform execution requires target-specific observed evidence.
