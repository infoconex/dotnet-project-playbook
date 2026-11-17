# AI-guided standards assessment and recommendations

This is **non-normative guidance** for applying the [registered standards](standards/README.md) through the canonical [start-here workflow](../start-here.md). It does not create a new engineering obligation or a permanent standard. Each linked standard defines its own scope and expectation; [standards governance](governance/standards.md) owns Required, Recommended, Optional, conditional applicability, and exceptions. External platform behavior is governed by the relevant Microsoft, GitHub, or other authoritative technical documentation.

**Principle: Simple by default, rigorous when necessary.** Assess actual engineering risks and evidence without turning a small project into a compliance-management exercise. This document describes how a general-purpose AI assistant should assess and explain; it is **not** an installed assessor, compliance engine, project generator, or executable validator.

## Choose the mode and evidence before a conclusion

1. **New-project foundation:** Learn a short purpose, intended consumers, project type, target frameworks and platforms, and material architecture, dependency, security, distribution or verification constraints. Identify applicable standards and proposed foundations; do not treat as-yet-uncreated files or unexecuted checks as satisfied or failed. Present the reviewable foundation before offering optional application-feature discovery.
2. **Existing-repository assessment:** Obtain read-only authorization, inspect source, project/solution files, framework/toolchain configuration, dependencies, tests, workflows, relevant history and documented decisions **before asking for facts those sources already supply**. Identify the requested ref and resolve an immutable commit where possible. Read-only means no target-repository files, settings, branches, issues, PRs, checks or other state are changed; if access is unavailable, state exactly what is unknown.
3. **Authorized improvement or later reassessment:** Use the preceding assessment as a proposal, not permission to implement. Confirm actual authority and target governance before editing. For later reassessment inspect the current target afresh; no playbook adoption manifest or automatic synchronization is required.

Screen the full [catalog of STD-001–STD-022](standards/README.md), starting with each authoritative standard's level, scope, and trigger. The screening may be summarized for untriggered or unselected practices; report each materially applicable obligation, genuine gap, exception, and consequential unknown individually. Do not copy the catalog's normative text into a separate checklist. An unchanged legacy project is not automatically subject to standards scoped to **new projects** or **new/changed behavior**.

Consider real boundaries rather than matching filenames or architecture labels. A pure library need not adopt distributed services, messaging, Clean Architecture, or additional compiled projects without actual justification. A traditional non-SDK .NET Framework project can be appropriate with its compatible Windows, MSBuild, NuGet and test runner choices. Conversely, the presence of a tool, configuration, test name or folder is not proof that its expected behavior was executed or verified.

## Apply six assessment outcomes

First identify **applicable**, **not applicable**, or **undetermined trigger**, and note the Required/Recommended/Optional level. Then assign one outcome to the precisely scoped assessed claim. Do not silently combine multiple independently assessable claims under a misleading result.

| Outcome | Meaning | Minimum support for the conclusion |
| --- | --- | --- |
| **Satisfied** | An applicable obligation is met within the stated scope. | Relevant source, decision/review, and/or actual executed evidence appropriate to the obligation; identify revision, scope and material limitations. |
| **Gap** | The obligation applies and credible evidence establishes a material unmet condition. | State the actual trigger, unmet expectation and concrete contradictory source or observed failure. No mere inference from uninspected files or absent access. |
| **Partially satisfied** | Multiple **separable** conditions are involved; some are supported, while meaningful others are proven unmet or still unverified. | Name supported portions and distinguish proven gaps from unknown portions. Do not use Partial to disguise failure of an indivisible obligation. |
| **Approved exception** | An applicable **Required** obligation has a justified, explicitly reviewed and recorded departure consistent with [governance](governance/standards.md). | Link the actual scope, rationale, review/approval and remaining risk or follow-up. This is not ordinary satisfaction; an alleged but unverified approval is Unknown. |
| **Not applicable** | The triggering conditions do not apply to the assessed project or change. | Identify the relevant standard scope and known project/change facts disproving the trigger. It is not a defect and needs no remediation. |
| **Unknown** | Accessible evidence does not support a defensible determination, or the trigger itself is unresolved. | Identify inaccessible, missing, contradictory, stale or unexecuted evidence and what could resolve the uncertainty. Do not infer compliance or a gap. |

For an indivisible obligation, direct evidence of violation means **Gap** even if unrelated practices are good; insufficient evidence means **Unknown**. For a composite obligation, **Partially satisfied** does not hide a proven constituent gap or an unknown portion. Break down large claims when doing so makes the report clearer.

**Recommended alternatives and Optional omissions:** A Recommended default is not universally mandatory. Where a documented alternative better fits, record the decision and tradeoff explicitly; if the obligation is a considered design choice, distinguish a *governance-consistent alternative* from actually adopting its named pattern. An Optional practice not selected for a justified project profile needs no exception. Do not claim the architecture was implemented just because a reasonable alternative was selected. When a genuine condition applies but its satisfaction is unclear, use Unknown rather than convenient Not applicable.

**Example of a justified Not applicable outcome:** In an unchanged traditional .NET Framework repository, [STD-006](standards/csharp.md#std-006) (nullable reference types in *new compatible C# projects*) does not retroactively require rewriting an existing C# 7.3 project. Record the actual project format, language version, revision, and scope of the assessment; new projects or material future changes can have different triggers. This is an example of assessment logic, not a completed consumer assessment.

## Match evidence strength to the claim

| Evidence | What it can establish | What it cannot establish alone |
| --- | --- | --- |
| Authoritative documentation | Supported platform/tooling behavior for stated versions and conditions | That a consumer implements, builds or runs correctly |
| Source/configuration inspection | Presence, structure or declared settings at an identified revision | Successful execution, a historical test-first sequence or runtime compatibility |
| Manual engineering review | A reviewer's inspected scope, method, findings and decision | Unexecuted tests or unsupported deployment environments |
| Executed test/build/check | The actual operation and result for its revision and environment | Untested behavior, other OS/RIDs, security, or all requirements |
| Scenario conversation | Observed AI questions, recommendations, decisions, transitions and stops | Behavior of all AI providers, a generated application, or automation that was not run |
| Experimental evidence | A scoped reproducible answer to a material technical uncertainty | Generalization beyond the experiment's scope |

Use the [verification guide](verification-guidance.md) to distinguish **Passed, Failed, Skipped, Unavailable, Manually reviewed, and Not executed** for checks. Those are *verification execution* outcomes, not the six *standards assessment* outcomes above. In particular a skipped GitHub job's check conclusion or a successful workflow container cannot substitute for inspecting which material steps actually ran. A clean scanner result is not proof of overall security. Do not claim that documentation review compiles, validates, or generates a project.

For each material finding, record **supporting evidence** separately from **contradictory evidence** and **limitations**. Prefer links to files at immutable revisions, issues, review decisions, test cases, and CI runs over copied mutable status. If a target SHA cannot be resolved, identify the moving ref, retrieval date, method attempted, and conclusions relying on unpinned material. Cite only observations actually inspected; missing access is not a failed check.

**Execution provenance:** When a check matters to an assessment, distinguish the requested repository revision, the revision of inspected source, the SHA attached to any CI run, the particular jobs or steps recorded as successful, and unavailable logs. Look for existing commit-linked run/job results before concluding that exact-revision execution is unknown. A historical PR-candidate run does not automatically establish execution of its later squash commit; equally, an available exact-commit CI result should not be overlooked. Source, configured workflow, historical executed check, independently reproduced execution, and administrator-only setting are useful *evidence descriptions*, not extra assessment outcomes.

**Composite findings:** Use one of the six canonical outcomes for each reported obligation, then qualify its scope. If a standard covers separable protections, identify which were observed and which remain unknown or unmet. Avoid vague mixtures such as “partially evidenced, broader coverage unknown” as a substitute for a defined outcome. An absent configuration or unavailable audit is a limitation, not automatically contradictory evidence.

## Human-readable assessment report

Start with a compact report; expand fields when consequences or conflicting evidence warrant it. This is a **shape**, not a mandatory machine-readable schema or universal table of every standard.

### Identity and context

- **Objective and mode:** new-project foundation, read-only existing-repository assessment, or authorized reassessment.
- **Identity:** project purpose and consumers, repository URL/ref if any, project type, relevant framework, language, OS, architecture, dependencies and material constraints.
- **Provenance:** exact playbook commit; for a target repository exact target commit and resolution method if available, or explicit unpinned limitation; assessment date.
- **Sources and scope:** inspected paths, decisions, tool/CI records and inaccessible sources. For a new proposal, no target SHA exists and source files are proposed rather than implemented.

### Findings

For each material standard, record: **STD ID/title and authoritative link; level and applicability trigger; outcome; supporting evidence; contradictory evidence if any; evidence limitations and exceptions if applicable; action/decision if useful.** Group straightforward justified Not applicable entries or omit optional fields that add no useful context, but be able to show that the full catalog was considered. A proposition about future files may be an *intended way to satisfy a standard*, not an observed Satisfied outcome.

### Recommendations and boundaries

For each meaningful action, identify the problem/opportunity, relevant standard or official guidance, actual evidence, expected benefit, material drawbacks and alternatives, practical priority, prerequisites, verification required, and **explicit authorization needed**. Distinguish immediate correctness/security/compatibility risk from valuable but deferrable maintainability and productivity work. Use human terms such as **Now**, **Next**, and **Consider** if helpful; never calculate a universal compliance score or create issues automatically.

Finish with unresolved questions, checks actually executed versus configured/planned/skipped/unavailable, exceptional decisions, Phase 2 offered/accepted/declined/unnecessary, and the next authorized step. In read-only mode, **stop before implementation**.

## Prioritize by risk and engineering value

1. Investigate demonstrable correctness and acceptance failures, material security and sensitive-data exposure, unsupported compatibility or release claims, and applicable Required obligations **in their actual risk context**.
2. Evaluate unverified material acceptance commitments, maintainability and architecture boundaries, developer experience, and worthwhile Recommended alternatives against observed change pressure.
3. Account for existing decisions, remediation cost, prerequisites, maintenance/operational burden and opportunity cost. Explain why an action belongs now or later; do not impose a technical pattern for its own sake.
4. Do not prescribe remediation for legitimate Not applicable results, unselected Optional practices or supported alternatives. Where evidence is Unknown, prioritize obtaining the smallest decisive evidence before prescribing substantial change.

No assessment or discovery question authorizes a branch, issue, PR, source edit, new configuration, workflow, package, test run, or deployment. A later change requires the developer's permission and the target's own governance.

## Evaluation is a different activity

An **assessment report** evaluates the consumer project. A separate [AI conversational evaluation report](evaluate-playbook.md#evaluation-report-requirements) evaluates what an assistant actually asked, recommended and concluded. The [three-case evaluation corpus](evaluation-corpus.md) defines representative read-only cases; a protocol, sample output, source inspection or manually authored ideal transcript does **not** establish observed conversational behavior. If a fresh run cannot be performed, disclose **Not executed** and leave the corresponding evaluation acceptance pending.
