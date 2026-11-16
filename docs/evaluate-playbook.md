# Manual AI-first playbook evaluation

This is a versioned, read-only **conversational evaluation procedure**, not the playbook's source of adoption instructions. The [start-here guide](../start-here.md) defines the intended developer experience, and the [assessment guide](assessment-guidance.md) defines non-normative finding/reporting behavior. The [three-case corpus](evaluation-corpus.md) identifies representative contexts and preflight evidence. Keep an evaluator's rubric separate from the participant's initial request so the evaluation does not teach an AI the behavior being assessed.

## How to run

1. Start a fresh, unpersonalized conversation so previous preferences and project history do not influence the result.
2. Open this document at a **commit-pinned GitHub URL**. Evaluate the [start-here guide](../start-here.md) and its linked standards from **the same commit**, not whichever version happens to be on `main`.
3. Give the assistant **only the relevant opening objective** below (with the repository URL or pinned revision for existing-repository cases), and ask it to follow the pinned start-here guidance. Keep the evaluator observations/rubric out of that opening request. The developer answers actual discovery questions as they arise, including whether to opt into an optional second phase if offered. Do not give an expected question list, preferred architecture, or desired phase transitions.
4. At the stopping condition, produce the **complete, self-contained evaluation report** described below in the conversation. A retained transcript may supplement the report but must not be required to interpret it after a Temporary Chat closes. Do not claim that a conversational simulation validates generated code or automated tooling.
5. **All participant scenarios are read-only.** Do not create or clone repositories, write files, execute commands, open issues or PRs, or change settings. Read-only retrieval of accessible documentation, repository files and relevant CI run/job evidence is permitted. The separate Issue #12 documentation implementation and its PR are not participant scenario actions.
6. Record the actual assistant client/model when known, the exact playbook and target revisions, whether a genuinely fresh unpersonalized conversation was possible, and all missing capabilities. **If no genuine conversation took place, label the case Not executed and keep conversational acceptance pending**; a source-inspection preflight or authored hypothetical transcript is not a run.

The [evaluation corpus](evaluation-corpus.md) includes **(1) new-project foundation, (2) SDK-style modern .NET Binary Tools, and (3) traditional non-SDK .NET Framework RecordSift**. Three cases are sufficient for the initial contract; add a targeted fourth only if a material interaction remains untested after observed results. Do not import the evaluator's expected conclusions into the assistant's prompt.

## New-project scenario

**Opening objective:** I want to start a new .NET project. I have not supplied its purpose, project type, target frameworks, architecture, or other constraints.

Evaluator observations to record **after** the interaction, not instructions to append to the participant's opening prompt:

- Read and follow the [start-here guide](../start-here.md) and relevant authoritative documents at the same revision. If the documents cannot be accessed, report that limitation and stop rather than guessing.
- Guide the developer through the discovery and proposal described by the playbook. Let the developer's answers determine which further information matters, including any follow-up discovery they choose.
- If the developer describes a consequential asynchronous workflow, integration, fan-out or background job, check whether the assistant compares straightforward synchronous mechanisms with conditional [STD-018](standards/event-driven.md#std-018). A small CRUD/library example with no such needs should not be prescribed a broker or event bus. This is a judgment of the conversational proposal, not a required implementation or a new universal questionnaire.
- When the proposal specifies SDK/build tools, NuGet dependency versions, shared build settings, feeds, or lock files, assess whether it follows the conditional [build and dependency configuration guidance](build-dependency-guidance.md). Do not expect all ten mechanisms or a new configuration questionnaire in a simple new project.
- When realistic secrets, sensitive data, third-party dependencies, or security-sensitive changes exist, check that the proposal applies the corresponding conditional [STD-019–STD-021](standards/security.md) and [security guidance](security-guidance.md) proportionately. A dependency-free offline utility should not be prescribed a vault, DAST, or a scanner suite without a concrete need; do not introduce a new questionnaire.
- Describe proposed actions only, without carrying them out.
- **Do not stop merely because a generator or template is absent before completing discovery and the proposed plan.** Once the proposal is complete, identify the first step that would require an unavailable playbook asset or verified capability, then stop without inventing one.
- At that point, report the foundation decisions and remaining unknowns, optional application-discovery decisions (if any), proposed files or configurations and why, applicable documented standards, intended verification, the exact implementation boundary, and any unclear or conflicting playbook guidance. Distinguish observed facts, proposals, and unverified capabilities.

## Existing-repository scenario

**Opening objective:** I want a read-only assessment of an existing .NET repository against the playbook. The evaluator must provide a specific accessible repository or its contents; do not invent one.

For the existing-repository cases, the evaluator should examine whether the assistant followed the same [start-here guide](../start-here.md), inspected actual accessible evidence, established applicability and intentional exceptions, and respected the developer's decisions about further discovery.

When the target uses event-mediated interactions, examine observed producers/consumers, transaction and published-contract evidence before assessing conditional [STD-018](standards/event-driven.md#std-018); report missing broker/deployment verification as unknown, not a proven defect. Do not mark a synchronous monolith or service as noncompliant for lacking event-driven infrastructure.

When build or dependency configuration is relevant, inspect available project/solution files, SDK/tooling constraints, NuGet package format, inherited configuration, feeds, locks, and verification workflows before suggesting changes. Apply the [build and dependency configuration guide](build-dependency-guidance.md) with its legacy compatibility and evidence limits; do not treat absence of optional central files as noncompliance.

When security or supply-chain risk is relevant, inspect the target's actual secret handling, dependency sources and formats, visible advisories, repository security settings, privileged workflows, and material changed trust boundaries. Apply [STD-019–STD-021](standards/security.md) by their triggers, using [risk-proportionate guidance](security-guidance.md). Distinguish configured scanning from scans actually run and missing coverage from a proven violation; do not call an absent optional security product a defect by itself.

Attempt to resolve the **exact target commit SHA** for the repository and branch/ref under assessment using available **read-only** repository metadata. Where possible, inspect target files at that immutable revision and distinguish such evidence from content retrieved through a moving branch. If the SHA cannot be resolved, record the supplied repository and branch/ref, the failed or unavailable retrieval method, and which findings rely on unpinned evidence. Proceed with appropriately qualified conclusions; do not invent a SHA, treat a branch name as immutable, or claim exact-revision verification.

Do not modify the target. If a missing source or capability prevents a reliable conclusion, explain the uncertainty rather than asserting compliance or a defect. Stop and report the first unsupported implementation or verification step after the assessment proposal.

## Evaluation report requirements

At the stopping condition, return the report **in the conversation**. Include the following so the evaluation can be compared with later revisions without reopening the original chat:

This is an **AI-behavior evaluation report**, distinct from the [consumer project assessment report](assessment-guidance.md#human-readable-assessment-report). The latter reports a project's standards findings; this evaluation reports what the assistant actually did and how faithfully it followed the adoption contract.

1. **Evaluation identity:** Scenario, exact playbook commit, AI client/model (if known), authorization mode, and actual sources inspected. For an existing-repository scenario, include the target repository, requested branch/ref, **resolved target commit SHA and how it was obtained**, and whether inspected evidence was pinned to that SHA. If resolution was unavailable, explicitly say so, record the attempted method and retrieval date, and distinguish unpinned evidence from immutable-revision evidence. For new-project scenarios with no target repository, mark the target SHA as not applicable.
2. **Full chronological question-and-answer log:** Include **every question asked**, not merely representative examples or totals. For each numbered question, record:
   - The phase or purpose: engineering foundation, optional application features, or a necessary clarification/transition.
   - The question's actual wording.
   - Every choice offered (or that it was free-text), the labeled recommended choice and explanation **as actually presented**, and whether interactive controls were observed. Mark absent information as *not presented*, rather than reconstructing it.
   - The developer's actual response, including their selected option or free-text answer. Clearly mark any intentionally redacted sensitive content.
   - A separate **evaluation judgment** about why the question was needed and whether it was useful, redundant, or could reasonably have been handled by a stated default. Distinguish this judgment from the observed exchange.
3. **Discovery summary:** Count questions by phase and purpose; identify where the foundation proposal was reached, whether defaults were presented together, and whether application-feature discovery was offered, accepted, declined, or unnecessary. Note the exact question or decision that marked a phase transition.
4. **Outcome and limitations:** Include the assistant's actual foundation proposal or consumer assessment report. Summarize applicable standards and exclusions, proposed files/configuration and rationale, outstanding decisions, the first missing playbook-specific asset or verification capability, checks actually performed versus configured/merely proposed, and any unclear or conflicting guidance. Identify supporting/contradictory evidence, unsupported compatibility claims, relevant authorization boundaries, and a genuine Not applicable or reviewed Required exception where observed.
5. **Recommendations for improving the playbook:** Cite the relevant question numbers or observed behavior so suggested changes can be independently evaluated.

Do not omit questions because the log is long, manufacture missing answers or recommendations, or silently turn an inference into an observation. If part of the conversation is genuinely unavailable, state the limitation and identify the missing span. This is **reporting guidance**, not a prescribed discovery questionnaire: the actual questions and phase transitions must come from the [start-here guide](../start-here.md) and developer responses.

If a scenario is **Not executed**, do not create fictional Q&A rows, phase transitions, or a "successful" evaluation report. Instead report the exact case protocol, any separately completed *read-only source inspection* (including immutable commits and sources), why the genuine conversation was unavailable, and the remaining evaluation actions. This is a documented limitation, **not** satisfaction of the chronological-interaction acceptance criterion.

## What this evaluation can establish

The transcript may provide evidence about whether an unfamiliar AI can locate the guidance, prioritize engineering foundations, present relevant defaults without excessive questioning, defer detailed application features until they are useful and chosen, apply documented standards contextually, report evidence and unknowns responsibly, respect authorization, and recognize missing assets. It cannot establish that every model/provider will behave identically, or that an installable agent, template generator, cross-platform build, or validation system works when those capabilities have not been executed.
