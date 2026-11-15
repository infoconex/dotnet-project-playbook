# Manual AI-first playbook evaluation

This is a versioned, read-only **evaluation scenario**, not the playbook's source of adoption instructions. The [start-here guide](../start-here.md) defines the intended developer experience. This file supplies only the test scenario, operational boundaries, and stopping condition so the evaluation does not teach an AI the behavior being assessed.

## How to run

1. Start a fresh, unpersonalized conversation so previous preferences and project history do not influence the result.
2. Open this document at a **commit-pinned GitHub URL**. Evaluate the [start-here guide](../start-here.md) and its linked standards from **the same commit**, not whichever version happens to be on `main`.
3. Ask the assistant to run one scenario below. The developer answers discovery questions as they arise, including whether to opt into an optional second phase if offered. Do not provide an expected question list, a preferred architecture, or the desired phase transitions in the opening prompt.
4. Preserve the transcript or final report for review. Record the playbook commit and AI client/model, the number and purpose of foundation versus application-feature questions, whether defaults were presented together, and whether any optional second phase was offered and explicitly chosen. Do not claim that a conversational simulation validates generated code or automated tooling.
5. **All scenarios are read-only.** Do not create or clone repositories, write files, execute commands, open issues or PRs, or change settings. Read-only retrieval of accessible documentation and repository content is permitted.

## New-project scenario

**Opening objective:** I want to start a new .NET project. I have not supplied its purpose, project type, target frameworks, architecture, or other constraints.

As the AI assistant:

- Read and follow the [start-here guide](../start-here.md) and relevant authoritative documents at the same revision. If the documents cannot be accessed, report that limitation and stop rather than guessing.
- Guide the developer through the discovery and proposal described by the playbook. Let the developer's answers determine which further information matters, including any follow-up discovery they choose.
- Describe proposed actions only, without carrying them out.
- **Do not stop merely because a generator or template is absent before completing discovery and the proposed plan.** Once the proposal is complete, identify the first step that would require an unavailable playbook asset or verified capability, then stop without inventing one.
- At that point, report the foundation decisions and remaining unknowns, optional application-discovery decisions (if any), proposed files or configurations and why, applicable documented standards, intended verification, the exact implementation boundary, and any unclear or conflicting playbook guidance. Distinguish observed facts, proposals, and unverified capabilities.

## Existing-repository scenario

**Opening objective:** I want a read-only assessment of an existing .NET repository against the playbook. The evaluator must provide a specific accessible repository or its contents; do not invent one.

As the AI assistant, follow the same [start-here guide](../start-here.md), inspect actual evidence where accessible, and establish applicability and intentional exceptions before proposing improvements. Follow the developer's decision about any further discovery. Do not modify the target. If a missing source or capability prevents a reliable conclusion, explain the uncertainty rather than asserting compliance or a defect. Stop and report the first unsupported implementation or verification step after the assessment proposal.

## What this evaluation can establish

The transcript may provide evidence about whether an unfamiliar AI can locate the guidance, prioritize engineering foundations, present relevant defaults without excessive questioning, defer detailed application features until they are useful and chosen, apply documented standards contextually, respect authorization, and recognize missing assets. It cannot establish that an installable agent, template generator, cross-platform build, or validation system works when those capabilities have not been executed.
