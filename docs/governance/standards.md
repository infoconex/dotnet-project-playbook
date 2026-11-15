# Standards governance

This page governs how standards are introduced, changed, interpreted, and traced to reusable assets. The [engineering principles](../standards/engineering-principles.md) are the current normative baseline.

## Applicability levels

| Level | Meaning | Exceptions |
| --- | --- | --- |
| Required | Must be satisfied for every project in the stated scope. | A justified, explicitly reviewed and recorded exception is necessary. |
| Recommended | Default approach unless a documented alternative better fits the project. | Explain the tradeoff at the point of adoption. |
| Optional | Adopt when the project profile or actual requirement benefits from it. | No exception required when omitted. |

Requirements may be **conditional** on context, such as Native AOT distribution, legacy MSBuild projects, or the need for physical adapter boundaries. A conditional standard must name its trigger. Do not classify unsupported projects as noncompliant merely because a standard does not apply.

## Standard content contract

Every new normative standard should state:

1. **Purpose and rationale:** the problem it addresses and relevant tradeoffs.
2. **Applicability and level:** audience, project types, and Required/Recommended/Optional status.
3. **Normative expectation:** concrete, reviewable behavior, separated from illustrative suggestions.
4. **Implementation guidance:** practical ways to comply, with profile-specific differences.
5. **Verification:** suitable local commands, automated checks, or review evidence; unsupported verification must be disclosed.
6. **Exceptions and alternatives:** conditions under which another approach is acceptable.
7. **Templates and examples:** links to implemented assets when they exist, not promises of nonexistent files.

When a standard or its implementation depends on established platform or third-party behavior, apply the [research-first technical decision principle](../standards/engineering-principles.md#evidence-based-technical-decisions). This is not an additional required research artifact for routine changes.

## Authority and change control

- Standards own normative requirements and their applicability. Architecture Decision Records capture *why* significant choices were made, not a second mutable policy catalog.
- Templates implement applicable standards; they are not independently authoritative when they disagree with an approved standard.
- Once implemented, scripts should validate executable behavior and CI workflows should orchestrate the same checks and record observed execution; skipped jobs are not passing evidence. Documentation-only review is appropriate at this foundation stage.
- Examples demonstrate how standards were applied in a particular project and are not themselves universal standards.
- Track proposed work and completion in GitHub issues and pull requests. Do not repeat live completion status across directory README files.

One issue should ordinarily have one PR. A normative change requires reviewed reasoning, impact on existing templates and tests, validation evidence, and explicit owner approval before merging. Assign meaningful decision records in [docs/decisions](../decisions/README.md) rather than silently modifying established expectations.

## Versioning and adoption

Template releases, once implemented, should carry immutable version identity and provenance. When the playbook is applied, the change proposal or review should identify the relevant playbook revision and asset versions where possible; no extra playbook-specific tracking file is required in the consumer repository.

Adoption is AI-assisted and interactive, for both new and existing projects. The consumer's actual files and existing documentation are the evidence for later on-demand assessments. An agent should respect known project decisions, ask about ambiguity, and not assume that every difference is a defect. New playbook releases must not silently overwrite consumer customizations. The detailed update and compatibility mechanism remains future work. See the [adoption decision](../decisions/0002-ai-first-adoption.md) and [planned workflow](../architecture/template-model.md#ai-first-adoption-and-assessment).
