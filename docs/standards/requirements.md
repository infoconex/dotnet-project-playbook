# Requirements and acceptance traceability standard

The [engineering principles](engineering-principles.md), [standards governance](../governance/standards.md), and [standards catalog](README.md) define authority and exception handling. The [on-demand requirements guide](../requirements-guidance.md) offers examples and choices; it is not a second normative rulebook.

## <a name="std-022"></a>STD-022 — Proportionate Requirements and Acceptance Traceability

**Level:** Recommended (conditional).

### Purpose and rationale

For consequential requirements, it should be possible to determine what was agreed, how acceptance is judged, and what evidence actually supports that judgment. Lost relationships among changing requirements, scenarios, and verification create risks that test-first implementation alone does not address. This standard establishes one reviewable playbook choice without mandating enterprise requirements management.

**Distinct ownership:** [STD-001](engineering-principles.md#std-001) owns test-driven development; [STD-009](testing.md#std-009) owns representative external-boundary verification; [evidence-based claims](engineering-principles.md#evidence-based-technical-decisions) own truthfulness about verification. [Security standards](security.md) own security obligations. STD-022 concerns **navigation between accepted requirements, observable acceptance outcomes, and evidence**, not their test technique or security implementation.

### Applicability

Assess STD-022 where a project has one or more material reasons to retain independently navigable requirements and acceptance evidence:

- Multiple independently evolving capabilities, contracts, or contributors/owners.
- Consequential quality, security, privacy, regulatory, or external-consumer acceptance constraints.
- Changes whose acceptance or regression risk is hard to assess from a small local test and its issue/PR alone.
- Maintenance across significant releases or integration boundaries where decisions and evidence might be lost.

Do not infer applicability solely from project type, size, framework, architectural style, or adoption of TDD. A cohesive library with self-explanatory tests and linked issues may need no separate requirements artifacts.

### Normative expectation when adopted

For significant **accepted requirements** in the chosen scope:

1. Keep the required outcome identifiable in the project's existing source of truth, with enough context to distinguish it from implementation design or a proposed idea.
2. Express or link to observable acceptance outcomes and relevant conditions, including meaningful quality measures where quality requirements are consequential.
3. Provide a **navigable relationship** from those requirements and outcomes to applicable verification activities and recorded evidence or an explicit evidence gap. Many-to-many links are valid.
4. Distinguish approval of the requirement, implementation of behavior, and actual verification. Do not imply a documented, compiled, or planned outcome is a passing acceptance result.
5. Assign each mutable verification status/evidence field one authoritative owner and link to it elsewhere rather than copying changing values into competing documents.

The obligation is the relationship and honest evidence, **not the document format**. Issue links, descriptive test names, PRs, a compact Markdown table, existing requirements tools, or a more detailed project-specific catalog can all satisfy it. Use stable IDs if independently locating an item warrants them; no CAP/FR/NFR/SCN convention, file-per-scenario model, universal matrix, automated traceability tool, or mandatory feature questionnaire is implied.

### Implementation and verification

- Identify the actual applicable requirements and acceptance outcomes, then follow a representative sample through to test cases, manual checks, or other appropriate verification and evidence.
- When asserting that acceptance has been verified, inspect the **observed** result and relevant revision, environment, test/run or review record, and known limits. A test name or CI configuration without execution evidence is only a planned verification path.
- Review whether important uncovered requirements and limitations are visible rather than hidden by broad claims. Document new exceptions or a justified alternative in the project's normal issue/PR decision record.
- In a documentation-only change, review the accuracy and navigability of examples without manufacturing a runtime test or claiming another repository's historical run was re-executed.

### Alternatives, exceptions, and proportionality

As a **Recommended** standard, a justified project-specific alternative can be adopted with a brief rationale. When the trigger is absent, no exception or formal assessment artifact is required. When it applies but a separate catalog or traceability table would merely duplicate working issue/test/PR links, keep those links as the implementation instead. When confidentiality, tooling access, or unavailable environments prevent verification, disclose the limitation and next appropriate check; do not convert unknown into verified.

### Illustrations and references

- [Requirements, acceptance, quality, and traceability guide](../requirements-guidance.md), including detailed and minimal examples.
- [Optional application-feature discovery](../../start-here.md#phase-2-offer-optional-application-feature-discovery).
- [ISO/IEC/IEEE 29148:2018 requirements engineering](https://www.iso.org/standard/72089.html); [ISO/IEC 25010:2023 product quality model](https://www.iso.org/standard/78176.html); [Microsoft requirements traceability](https://learn.microsoft.com/en-us/azure/devops/cross-service/end-to-end-traceability?view=azure-devops) and [testing strategy](https://learn.microsoft.com/en-us/azure/well-architected/design-guides/testing).

These external references supply established concepts; STD-022 is the playbook's **conditional choice** about navigable acceptance evidence, not an assertion that external standards are universally binding.
