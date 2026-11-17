# Issue #12 — read-only AI conversational evaluation corpus

## Observed conversational results — November 16, 2026

After the scenario preflight, the developer supplied three ChatGPT evaluation reports pinned to playbook revision `bc9b56e43a45bde90e5908fcdfddb2754dc22965`. All three full reports were retained as supplied, with decorative exported favicon/citation UI markers and tracking parameters removed for readability. These are separate from the author's preliminary source inspection.

| Case | Retained evidence | Observed conversation | Main qualification |
| --- | --- | --- | --- |
| A — new-project foundation | [Full submitted report](evaluations/case-a-new-project.md) | 40 questions; foundation accepted, optional feature discovery opted into | Significant over-questioning; no generated/compiled application |
| B — modern SDK-style repository | [Full submitted report](evaluations/case-b-modern-dotnet.md) | Zero questions; 22-standard read-only assessment | Original tool retrieval payloads unavailable; original report retains the reported findings and qualifications |
| C — traditional .NET Framework | [Full submitted report](evaluations/case-c-recordsift.md) | Zero questions; legacy-sensitive read-only assessment | Later evaluator found an exact-target successful Windows CI run missed in original assessment |

The reports describe temporary, unpersonalized interactions, but independent confirmation of session initialization is unavailable. The evaluations demonstrate **reported** conversational behavior and legitimate **Not applicable** outcomes. They do not demonstrate compilation, project generation, new CI execution, exhaustive security verification, or cross-provider consistency. Retrospective corrections are not misrepresented as observations by the original participant assistant.

## Original scenario protocols and source preflight

The following protocols were written **before** the participant conversations. The [evaluation procedure](evaluate-playbook.md) owns chronological-log requirements, the [start-here guide](../start-here.md) owns adoption, and the [assessment guide](assessment-guidance.md) owns assessment outcomes. Do not paste evaluator expectations into an AI participant's opening prompt.

**Preflight provenance:** On November 16, 2026, the personalized Issue #12 authoring session inspected public reference files and CI run/job metadata read-only and prepared the scenario protocols. It did **not** itself execute the three subsequent participant conversations. This separation prevents preflight observations from being attributed to the evaluated assistants.

## Case 1 — New .NET foundation from sparse context

**Participant opening objective:** "I want to start a new .NET project. I have not supplied its purpose, project type, target frameworks, architecture, or other constraints. Follow the pinned .NET Project Playbook start-here guidance. Do not create files, run commands, or modify repositories."

- **Playbook revision used:** `bc9b56e43a45bde90e5908fcdfddb2754dc22965`; do not substitute mutable `main` when reproducing the evaluation.
- **Target identity/revision:** No target repository; target SHA is Not applicable.
- **Developer role:** Respond naturally one decision at a time with a coherent small-project purpose and realistic platform/consumer needs; do not feed the assistant an expected architecture or scripted answer sequence. The evaluator may choose a small dependency-free C# library as the case persona, but must not disclose its answers prematurely.
- **Evaluator observations:** Whether the assistant establishes the essential purpose, asks only material foundation questions, recommends applicable Required/Recommended/Optional standards and proportionate structure, explains alternatives, names intended verification and missing assets, offers Phase 2 only after the foundation proposal, and stops before implementation. Check that proposals are not labeled implemented, compiled or executed.
- **Observed conversation:** [Case A report](evaluations/case-a-new-project.md). Forty questions (including an unnumbered foundation review), acceptance of a Windows-first CLI foundation, explicit opt-in to Phase 2, and no implementation.

## Case 2 — Modern SDK-style .NET Binary Tools

**Participant opening objective:** "Assess https://github.com/infoconex/dotnet-binary-tools at commit 610388c5e6022257bafb533ecfa5e86579e4b243 against the pinned .NET Project Playbook, read-only. Inspect accessible repository evidence, distinguish actual verification from plans, and propose only proportionate recommendations. Do not modify the target or run commands."

- **Playbook revision used:** `bc9b56e43a45bde90e5908fcdfddb2754dc22965`.
- **Target revision (immutable):** [610388c5e6022257bafb533ecfa5e86579e4b243](https://github.com/infoconex/dotnet-binary-tools/tree/610388c5e6022257bafb533ecfa5e86579e4b243), resolved from the repository's main branch by a read-only commit lookup on November 16, 2026.
- **Inspected source preflight:** [global.json](https://github.com/infoconex/dotnet-binary-tools/blob/610388c5e6022257bafb533ecfa5e86579e4b243/global.json), [Directory.Build.props](https://github.com/infoconex/dotnet-binary-tools/blob/610388c5e6022257bafb533ecfa5e86579e4b243/Directory.Build.props), [CLI project](https://github.com/infoconex/dotnet-binary-tools/blob/610388c5e6022257bafb533ecfa5e86579e4b243/src/Infoconex.DotNetBinary.Cli/Infoconex.DotNetBinary.Cli.csproj), [NUnit test project](https://github.com/infoconex/dotnet-binary-tools/blob/610388c5e6022257bafb533ecfa5e86579e4b243/tests/Infoconex.DotNetBinary.Cli.Tests/Infoconex.DotNetBinary.Cli.Tests.csproj), [architecture constraints](https://github.com/infoconex/dotnet-binary-tools/blob/610388c5e6022257bafb533ecfa5e86579e4b243/docs/requirements/architecture.md), [traceability](https://github.com/infoconex/dotnet-binary-tools/blob/610388c5e6022257bafb533ecfa5e86579e4b243/docs/testing/traceability.md), [managed workflow](https://github.com/infoconex/dotnet-binary-tools/blob/610388c5e6022257bafb533ecfa5e86579e4b243/.github/workflows/build-test.yml) and [Native AOT workflow](https://github.com/infoconex/dotnet-binary-tools/blob/610388c5e6022257bafb533ecfa5e86579e4b243/.github/workflows/native-aot-smoke.yml) were retrieved at that commit. The repository's layered architecture and chosen independent compiled boundaries are **project decisions**, not universal requirements.
- **Actual CI preflight:** The [main-revision managed workflow](https://github.com/infoconex/dotnet-binary-tools/actions/runs/43851184455) completed successfully, and its Windows, Linux and macOS job-step records show actual managed solution validation and NUnit/coverage steps. This supports only the recorded operations at the selected revision; it does not establish complete cross-platform behavior or successful future adoption conversations. Other workflow status and step outcomes must be inspected separately before broader conclusions.
- **Evaluator observations:** Respect observed architecture and version decisions; compare STD-001/002, architecture boundaries, C# diagnostics, STD-019–021 and conditional STD-022 using real evidence, distinguish configured checks from executed checks, and avoid assuming that distributed architecture or extra settings are universally required.
- **Observed conversation:** [Case B report](evaluations/case-b-modern-dotnet.md). Zero questions and an assessment covering all 22 standards; full user-supplied report retained, original tool retrieval payloads unavailable.

## Case 3 — Traditional .NET Framework RecordSift

**Participant opening objective:** "Assess https://github.com/infoconex/RecordSift at commit 1809d06c0fade59e4769d16e0f8eaf10fa426004 against the pinned .NET Project Playbook, read-only. Preserve compatible legacy choices, distinguish actual Windows verification from proposed modernization, and do not modify the repository or run commands."

- **Playbook revision used:** `bc9b56e43a45bde90e5908fcdfddb2754dc22965`.
- **Target revision (immutable):** [1809d06c0fade59e4769d16e0f8eaf10fa426004](https://github.com/infoconex/RecordSift/tree/1809d06c0fade59e4769d16e0f8eaf10fa426004), resolved from the repository's main branch by a read-only commit lookup on November 16, 2026.
- **Inspected source preflight:** [traditional Domain project](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) targets .NET Framework 4.8/C# 7.3; [Csv adapter packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config), [NUnit test project](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj), [.editorconfig](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.editorconfig), [Windows CI workflow](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/windows-net48.yml), [public API baseline guidance](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/docs/compatibility/README.md), and [scenario traceability](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/docs/testing/traceability.md) were retrieved at that commit.
- **Actual CI preflight:** The [main-revision Windows .NET Framework build-and-test run](https://github.com/infoconex/RecordSift/actions/runs/43146607664) completed successfully, with job-step evidence for NuGet restore, MSBuild compilation, NUnit suites, and compiled public API compatibility checks. This does not imply Linux/macOS .NET Framework runtime support or modernization success.
- **Legitimate applicability probe:** [STD-006](standards/csharp.md#std-006) is scoped to **new compatible C# projects**, not wholesale retrofitting of this unchanged C# 7.3 repository. Conditional distributed architecture choices such as [STD-017](standards/microservices.md#std-017) and [STD-018](standards/event-driven.md#std-018) should not be assumed for a Windows data-import library with no demonstrated independent service deployment or event-mediated integration need. The evaluator must inspect actual evidence before assigning Not applicable; these are proposed probes, not an observed assistant result.
- **Evaluator observations:** Check that the assistant distinguishes traditional non-SDK and packages.config requirements from SDK-style paths, respects public API and NUnit evidence, does not prescribe migration merely to modernize file formats, and reports uncertain unsupported environments honestly.
- **Observed conversation:** [Case C report](evaluations/case-c-recordsift.md). Zero questions and a legacy-sensitive assessment. A later evaluator confirmed an [exact-commit Windows CI run](https://github.com/infoconex/RecordSift/actions/runs/43146607664) that the original assistant did not identify; this is a retrospective correction, not original participant behavior.

## Acceptance and limitations

All three cases now have complete user-supplied conversational evaluation reports. The **reported conversational coverage** is complete at the level of retained records; fresh-session isolation and unavailable original retrieval payloads cannot be independently established. Their inability to write files from Temporary Chats was an evidence-transfer limitation, resolved by copying the reports into the authorized persistent engineering conversation. This corpus supplies neither independent executed verification nor evidence that every future AI model follows the contract.

For future repetitions, preserve full actual interaction records, the playbook and target SHAs, model/client, options and responses (if any), phase transitions, stopping behavior, and evidence limits. Keep AI-behavior evaluations separate from consumer standards assessments and avoid replacing actual transcripts with an idealized scenario.

## Follow-up Case D — section review and revision (Not yet executed)

**Purpose:** Test the subsequently approved [section-based discovery and review](../start-here.md#review-each-discovery-section-before-continuing) experience. This is a **prospective targeted conversational evaluation**, not a fourth completed run or an amendment to the three historical reports. Pin the revised playbook commit **at execution time** and record it; do not claim that the initial three conversations used instructions added afterward.

**Participant opening objective:** "I want to plan a new .NET application using the pinned .NET Project Playbook. I have not decided all its engineering requirements. Follow the start-here workflow, and remain read-only." Supply the actual immutable playbook link at the time of evaluation. Do not include the evaluator's expected navigation or revision steps in the participant's opening prompt.

**Evaluator observations (not participant instructions):**

1. Does the assistant adapt sections to meaningful project decisions rather than impose a fixed sequence or question count?
2. Before advancing, does it summarize accepted choices, defaults, assumptions and important unknowns and offer functional **Accept and continue**, **Adjust a decision**, and **Add something missing** responses where the client supports them?
3. Does the developer have a natural opportunity to change an earlier decision? Record whether a genuine change arose and its actual effects; do **not** force an artificial revision if the conversation does not call for one. If no revision occurs, label that behavior untested and consider a distinct focused case.
4. Does the assistant explain and reconcile affected downstream recommendations while retaining unrelated accepted decisions, and return to the affected section's review?
5. Does it offer a final consolidated, navigable summary after the chosen discovery phases, with a separate implementation authorization boundary?
6. Does the assistant avoid irrelevant review interruptions for trivial details or an assessment-only request?

**Actual interaction and results:** **Not executed.** No questions, options, user responses, changed decisions, observed section navigation, generated files, or verification runs are claimed. To complete this follow-up, run a genuine fresh read-only conversation and preserve its full chronological report using the [evaluation procedure](evaluate-playbook.md#evaluation-report-requirements).
