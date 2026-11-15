# Engineering principles

This is the authoritative baseline for engineering principles applied to projects using the playbook. [Standards governance](../governance/standards.md) defines what each obligation level means and how exceptions are approved. The [standards catalog](README.md) indexes approved, independently assessable practices by permanent ID and category. More detailed implementation standards will be introduced by future issues.

| Principle | Level | Application |
| --- | --- | --- |
| SOLID | Required | Design maintainable responsibilities, substitutions, interfaces, and dependency boundaries appropriate to the code. |
| <a name="std-001"></a>Test-driven development (`STD-001`) | Required | For new executable behavior and defect fixes, write a meaningful failing test, implement minimally, then refactor. Explain justified exceptions when behavioral TDD is applicable. Documentation-only edits do not require a behavioral test or an exception. |
| Dependency direction | Required | Keep business policies independent of concrete infrastructure and presentation mechanisms. |
| Automated verification | Required | For meaningful executable behavior, check important outcomes and applicable structural constraints with locally reproducible evidence where practical. Document gaps; documentation-only review does not require an artificial automated check. |
| <a name="std-002"></a>CI/local parity (`STD-002`) | Recommended | When CI is introduced, keep underlying validation in repository-controlled scripts; let CI provision tools, select environments, and publish results. |
| Hexagonal (Ports and Adapters) architecture | Recommended | When external adapters or meaningful dependency boundaries exist, define ports where they are consumed, keep adapters outside business logic, and use the pattern where it clarifies real dependencies. |
| <a name="std-003"></a>Separate compiled projects (`STD-003`) | Optional | Separate Domain, Application, Infrastructure, and presentation into compiled projects when responsibility and dependency boundaries justify the additional projects. |
| Evidence-based claims | Required | Distinguish designed, implemented, and observed/verified behavior. Record exact revisions and real test results. |
| Research-first technical decisions | Required | When decisions depend on external platform, framework, or tooling behavior, consult applicable authoritative guidance before inventing a solution or discovery experiment; verify its applicability to the actual project. |

## Applying STD-001 — Test-driven development

The Required TDD expectation in the table above is authoritative. It applies to **new executable behavior and defect corrections**, whether the behavior belongs to a pure library, an application component, or an infrastructure adapter. Select the [smallest meaningful behavioral boundary](../testing-guidance.md#choosing-the-first-test-and-broader-evidence) that can express the desired outcome; a unit test is not automatically the right first test for every change.

1. **Red:** Express the next observable behavior or regression in a test, run it, and establish that it fails for the intended behavioral reason—not merely because the project fails to build, a fixture is broken, or the test environment is unavailable.
2. **Green:** Make the smallest production change that satisfies that behavior and run the relevant test. Do not add speculative implementation or tests whose only purpose is to mirror private methods.
3. **Refactor:** Improve names, responsibilities, duplication, and boundaries while retaining the passing behavioral tests. Repeat in small increments for additional behavior.

For a defect, first reproduce the incorrect behavior with a regression test when feasible. For difficult existing code, a characterization test can establish what currently happens before changing it; distinguish that observation from the desired new behavior. TDD does not require every implementation line to have a separate test or mandate a single test framework, project graph, or level of test. [STD-009](testing.md#std-009) adds conditional real-boundary evidence when significant external-adapter behavior is involved; it does not replace the TDD cycle.

**Justified exceptions:** If a meaningful failing test cannot reasonably be established first—for example, because a necessary external environment is unavailable, an emergency correction cannot wait for a test harness, or legacy coupling prevents a useful observation—keep the departure narrow. Explain the concrete obstacle, any characterization attempt, alternative verification actually performed, residual uncertainty, and appropriate follow-up in the issue or PR. Obtain the explicit review required for an exception to a Required standard. Difficulty or inconvenience alone is not an automatic exception. Documentation-only edits do not trigger behavioral TDD and need no exception.

**Verification:** Review the behavioral tests and their outcomes, the scope of the change, and available evidence of the red-green-refactor sequence. A final passing test suite alone does not prove that tests were written first. Record what was observed rather than inferring TDD chronology or compatibility from source files. The [practical testing guide](../testing-guidance.md) supplies examples and Microsoft references without redefining STD-001.

## Architectural interpretation

SOLID and independence from infrastructure apply even to small class libraries. Hexagonal architecture is the preferred way to express boundaries when there are external adapters. It does **not** mandate four physical projects for every application. A complex service may need multiple independently compiled layers; a small pure library may need only the library and its tests.

New abstractions should serve an actual dependency, extension requirement, or testing seam. Avoid speculative project layers and wrappers. Test selection and architecture checks must match the concrete project rather than blindly reusing another repository's project graph.

## Evidence-based technical decisions

For a decision that depends on established .NET, NuGet, operating-system, framework, library, or tooling behavior, first ask **what is already known and what remains uncertain for this project?** Use the following research order, considering the source's authority for the specific behavior, version, platform, and context:

1. **Authoritative guidance:** Official platform/vendor documentation and applicable published technical specifications or standards. Neither always takes precedence over the other; establish which actually governs the behavior.
2. **Implementation evidence:** Relevant framework/library source code, release notes, and upstream tests. Distinguish observed implementation details from stable public contracts.
3. **Focused experimentation:** When material uncertainty remains, design a controlled, reproducible investigation that answers that question and records its limits.
4. **Supporting context:** Community guidance and independent findings when authoritative evidence is incomplete or conflicting; corroborate claims before relying on them.

Once an established approach is applicable, implement it and verify it using the repository's own dependencies, toolchain, operating systems, and tests. Do not perform an additional *discovery* experiment simply to rediscover behavior already settled by applicable authoritative guidance. A targeted compatibility or regression test may still be necessary.

Classify the evidence accurately:

| Classification | What the evidence means |
| --- | --- |
| **Documented** | An authoritative source describes expected behavior within an identified version, platform, and contractual scope. It does not prove this repository implements the behavior correctly. |
| **Verified** | Observed execution confirms relevant behavior in a specified repository environment, with commands, results, and revision evidence. It does not establish untested environments. |
| **Experimental** | A controlled investigation addresses material uncertainty left by other sources; record the question, method, outcome, and limitations. Its results may also constitute Verified evidence when reproducibly established. |

For significant technical decisions, record the applicable sources, the uncertainty that justified investigation, the actual verification evidence, and any intentional departure from authoritative guidance with rationale and tradeoffs. Keep changing implementation/CI status in the issue or PR, not duplicated across permanent standards. This is proportional guidance: routine application work and straightforward TDD changes do **not** require a research report or a mandatory literature search.

The [.NET Binary Tools multi-RID and lock-file example](../../examples/dotnet-binary-tools.md#documented-guidance-and-repository-specific-verification) illustrates how published guidance and focused application-specific tests complement one another.

## Verification and applicability

Relevant unit/component/integration tests, dependency-direction checks, and peer or owner review provide complementary evidence. No one static gate proves SOLID or full hexagonal correctness. A passing build does not establish scenario acceptance, security, release readiness, or cross-platform behavior that was not exercised.

Project-type implementation guidance belongs to future standards and templates. Refer to the [template model](../architecture/template-model.md) for the planned profiles rather than treating future deliverables as present features.
