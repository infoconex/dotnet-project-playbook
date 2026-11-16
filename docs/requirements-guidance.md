# Requirements, acceptance scenarios, and traceability

This is an **on-demand, non-normative guide** for new-project creation and existing-repository assessment. [STD-022 — Proportionate Requirements and Acceptance Traceability](standards/requirements.md#std-022) owns the conditional Recommended obligation. [Standards governance](governance/standards.md) explains applicability and alternatives. Do not turn these examples into a universal requirements structure.

**Central principle:** Record only enough intent, acceptance conditions, and evidence links to make important behavior and quality commitments understandable and reviewable. A small library can use an issue, tests, and PR; a product with independently evolving capabilities may benefit from a separate catalog.

## When requirements discovery belongs in the workflow

| Context | Proportional approach |
| --- | --- |
| **Phase 1 — new-project foundation** | Learn a brief purpose, project kind, target platform, and material technical constraints. Do **not** demand a full feature catalog before proposing foundation defaults. |
| **Phase 1 — existing-repository assessment** | First inspect source, tests, issues, project files, CI, and decisions. Preserve intentional conventions and distinguish missing access from missing requirements. |
| **Phase 2 — optional feature discovery** | If the developer opts in or a material feature gap warrants it, explore capabilities, behavior, quality, and acceptance **one question at a time**, reusing what is already known. |
| **Implementing an agreed change** | Clarify the outcome and tests needed for that change. [STD-001](standards/engineering-principles.md#std-001) governs behavioral TDD even without a formal requirements phase. |

See [start-here.md](../start-here.md#phase-2-offer-optional-application-feature-discovery). Deferring or declining Phase 2 is valid; neither phase itself authorizes implementation.

## Choose useful concepts, not a universal taxonomy

| Concept | Question answered | Example of when to record separately |
| --- | --- | --- |
| **Capability** | What useful outcome does the product enable? | A cohesive area with several independently changing requirements or owners. |
| **Functional requirement** | What observable behavior or contract must hold? | A distinct input, output, validation, or failure rule accepted by consumers. |
| **Business rule** | What invariant, decision, or policy must hold independently of an interface? | A policy reused by more than one use case; it can be embedded in the requirement rather than assigned its own file or ID. |
| **Quality / nonfunctional requirement** | Under which conditions and to what measurable degree must the system perform? | Significant reliability, performance, security, accessibility, compatibility, or other quality commitment. |
| **Acceptance scenario** | Given which context and action, what observable result would demonstrate the requirement? | Boundary, failure, or integration behavior whose outcome needs separate discussion or traceability. |
| **Verification evidence** | What actually ran or was reviewed, in which revision/environment, and what did it establish? | A test result, manual acceptance record, representative environment run, or explicit gap. |

A requirement should normally be clear enough to discuss, implement, and verify without relying on its eventual internal architecture. Avoid mixing agreed behavior with speculative implementation or presenting a proposed requirement as approved. Requirements may belong in issues, a living contract, code-level tests, or capability pages; do not create every artifact by default.

### Stable identifiers and relationships

Use stable IDs such as `CAP-005`, `FR-INV-001`, or `SC-INV-001` **when people or tools need to refer to items independently**. They are not mandated prefixes or a universal parent-child hierarchy. Retain accepted IDs during edits; record meaningful changes without silently reusing an ID for a different contract.

Requirements can have multiple scenarios; one scenario may validate multiple requirements; one test may cover more than one scenario, and a significant scenario may need multiple evidence types. Links or compact tables are sufficient when navigable. A full requirements traceability matrix is one **optional** implementation, not the standard itself.

## Write observable acceptance scenarios

A scenario needs enough **context**, **event or stimulus**, and **expected observable result** that another person can judge acceptance. Given/When/Then is often readable but is not required syntax, a mandate to store Gherkin files, or an obligation to adopt Cucumber.

Illustrative scenario for a hypothetical paging library:

> **Given** a request for page zero and ten available pages, **when** the page number is clamped, **then** page one is returned.

Also consider invalid inputs, limits, failures, and meaningful changes of state. Prefer outcomes visible through a public contract over assertions about private methods or internal call counts. Some acceptance cases are naturally unit-level; others require a real filesystem, database, network provider, host OS, or production-like workflow. Apply the existing [testing guide](testing-guidance.md), [STD-001](standards/engineering-principles.md#std-001), and [STD-009](standards/testing.md#std-009), rather than duplicating their test-selection obligations.

Cucumber's [Gherkin reference](https://cucumber.io/docs/gherkin/reference/) explains the Given/context, When/action, Then/observable-result idiom. It is a language option, not a required .NET testing stack.

## Quality requirements and acceptance conditions

Use a relevant quality attribute when a stakeholder commitment or material risk makes it necessary, not as a checklist exercise. [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) is a useful product-quality reference model; selecting an attribute does **not** establish its required target. Have the appropriate project decision-maker set the actual target.

A meaningful quality scenario identifies:

1. The relevant operating condition, workload, platform, architecture, and dependencies.
2. The stimulus or failure condition.
3. The observable response and measure.
4. The agreed acceptance threshold and measurement method.
5. Evidence, if collected, or what environment/measurement remains unavailable.

**Hypothetical proposal — not an approved or executed benchmark:** For a proposed report-export feature, after an agreed representative 10,000-record dataset and fixed benchmark host are specified, measure thirty warmed exports; the illustrative acceptance target is a p95 duration no greater than **2.0 seconds**. A test name, an unspecified host, or a passing build would not prove this target. The team must approve the real workload, host, repetitions and threshold; until execution is observed the result is **unverified**. This number is not a playbook default or Microsoft recommendation.

For consequential security or privacy requirements, refer to [STD-019–STD-021](standards/security.md); do not create weaker parallel security acceptance rules. For OS/framework/distribution claims, use the [platform compatibility evidence guidance](platform-compatibility-guidance.md). Quality measurement complements, but does not replace, behavioral and boundary testing.

## Detailed, real reference — .NET Binary Tools

The following is **a record inspected in the reference repository**, not a requirement that other projects copy its structure:

| Relationship | Reference |
| --- | --- |
| Capability | [CAP-005 — Inspection Inventory](https://github.com/infoconex/dotnet-binary-tools/blob/main/docs/capabilities/CAP-005.md) |
| Approved functional requirement | `FR-INV-001`, owned by CAP-005's requirement coverage table |
| Acceptance scenario | [SC-INV-001 — Inventory an individual inspection](https://github.com/infoconex/dotnet-binary-tools/blob/main/docs/scenarios/functional/inspection-inventory/FR-INV-001.md) |
| Concrete mapped test | `InspectionInventoryServiceTests.SingleFileInspectionHasOneCandidateAndSharedCompletion` |
| Recorded execution evidence | [Three-OS NUnit CI run 43818418554](https://github.com/infoconex/dotnet-binary-tools/actions/runs/43818418554), code revision `4e1c1626a6ee78cfd3d2fd31e370293f0378a0c6` |

The repository's [scenario-to-test traceability index](https://github.com/infoconex/dotnet-binary-tools/blob/main/docs/testing/traceability.md) records status and evidence centrally; requirement wording resides in capability documentation, and navigation indexes do not duplicate mutable scenario status. Its [nonfunctional requirements](https://github.com/infoconex/dotnet-binary-tools/blob/main/docs/requirements/non-functional.md) are explicitly **proposed, not approved**. Do not silently promote proposed quality scenarios into accepted requirements.

**Evidence limit:** This guide inspected the repository's recorded mapping and historical CI link; Issue #10 did **not** run the referenced project's NUnit tests or independently certify all supported hosts, artifacts, or later revisions. The mapped CI result applies only to its recorded revision and operations.

## Lightweight example — small pure C# library

For a cohesive hypothetical `PageRange.Clamp` library, a single issue could say: “Requests below the first page return page one; requests above the final page return the final page.” Its acceptance cases can be named directly in NUnit tests:

- `Clamp_RequestBelowFirstPage_ReturnsFirstPage`
- `Clamp_RequestAboveLastPage_ReturnsLastPage`
- `Clamp_NoAvailablePages_ThrowsArgumentOutOfRangeException`

The PR links the issue, identifies the tests and exact passing command/run/revision, and discloses any skipped environment. That gives a navigable **requirement → test → evidence** chain. A separate capability page, requirement ID, scenario file, and matrix would add little value. These names and outcomes are **illustrative**, not tests executed for Issue #10.

If the library later gains independent consumers, public compatibility guarantees, significant quality targets, or complex business policy, reassess its traceability rather than imposing the larger structure retroactively without need.

## Evidence, status authority, and honest claims

| Available record | Justified claim | Not established |
| --- | --- | --- |
| Agreed issue / accepted scenario | Intended and approved behavior within its stated scope | Implemented or verified behavior |
| Source diff / passing compilation | Code exists and compiles in the tested toolchain | Accepted behavior, runtime performance, or all consumers |
| Named automated test but no run | An identifiable intended check | A passing check |
| Passing test with run, SHA and environment | Specified outcomes observed in that revision/environment | Universal acceptance on untested platforms or dependencies |
| Representative manual review or test | The recorded observations in the reviewed environment | Automated coverage or unobserved behavior |
| Missing host, unavailable dependency, skipped CI | Explicit unverified gap | Pass or compliance |

Keep mutable acceptance status/evidence in **one** authoritative location chosen by the project (for example, GitHub issue/PR, test-management system, or a traceability table); link to it from stable requirement and index pages. Distinguish `Proposed`, `Approved`, `Implemented`, `Verified`, `Blocked`, and `Unknown` where those concepts matter, but do not require this vocabulary or replicate all six fields across artifacts. A test outcome may change without altering the approved requirement's wording.

A real test result should identify an appropriate run/command, result, revision, and relevant environment, alongside material limitations. Manual checks may be adequate for some observations; unavailable environments must remain stated gaps. Do not count planned checks, build-only smoke tests, coverage percentages, or historical tests on another SHA as acceptance proof for unexecuted scenarios.

## AI-assisted application to a repository

1. Establish whether the request is a foundation proposal, feature discovery, change implementation, or retrospective assessment. Follow authorized scope.
2. For existing projects, **inspect actual** issues, tests, source, CI, requirements and decisions before proposing new artifacts. Do not interpret a missing `docs/requirements` folder as a defect.
3. Determine whether STD-022's conditional triggers apply. Where existing links already provide enough traceability, retain them; where material relationships are lost, propose the smallest correction.
4. Ask a targeted question only when an unknown materially changes requirement ownership, acceptance threshold, or verification plan. Reuse answered questions; do not administer a fixed questionnaire.
5. When a new feature emerges, define the next meaningful outcome and evidence boundary with TDD. Return to foundation decisions only when a discovered requirement materially affects them.
6. Report what was approved, implemented, actually verified, skipped, or unknown. Propose changes for review; do not infer implementation authorization from discovery alone.

## Technical references

- [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html)
- [ISO/IEC 25010:2023 — Product quality model](https://www.iso.org/standard/78176.html)
- [Microsoft — Testing strategy and traceability for Azure workloads](https://learn.microsoft.com/en-us/azure/well-architected/design-guides/testing)
- [Microsoft — End-to-end requirements traceability](https://learn.microsoft.com/en-us/azure/devops/cross-service/end-to-end-traceability?view=azure-devops)
- [Microsoft — .NET unit-testing best practices](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices)
- [Cucumber — Gherkin reference](https://cucumber.io/docs/gherkin/reference/)

These references provide established vocabulary and behavior; the playbook's only new normative choice for this topic is [STD-022](standards/requirements.md#std-022).
