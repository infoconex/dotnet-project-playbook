# Engineering principles

This is the authoritative baseline for engineering principles applied to projects using the playbook. [Standards governance](../governance/standards.md) defines what each obligation level means and how exceptions are approved. More detailed implementation standards will be introduced by future issues.

| Principle | Level | Application |
| --- | --- | --- |
| SOLID | Required | Design maintainable responsibilities, substitutions, interfaces, and dependency boundaries appropriate to the code. |
| Test-driven development | Required | For new executable behavior and defect fixes, write a meaningful failing test, implement minimally, then refactor. Explain justified exceptions when behavioral TDD is applicable. Documentation-only edits do not require a behavioral test or an exception. |
| Dependency direction | Required | Keep business policies independent of concrete infrastructure and presentation mechanisms. |
| Automated verification | Required | For meaningful executable behavior, check important outcomes and applicable structural constraints with locally reproducible evidence where practical. Document gaps; documentation-only review does not require an artificial automated check. |
| CI/local parity | Recommended | When CI is introduced, keep underlying validation in repository-controlled scripts; let CI provision tools, select environments, and publish results. |
| Hexagonal (Ports and Adapters) architecture | Recommended | When external adapters or meaningful dependency boundaries exist, define ports where they are consumed, keep adapters outside business logic, and use the pattern where it clarifies real dependencies. |
| Separate compiled projects | Optional | Separate Domain, Application, Infrastructure, and presentation into compiled projects when responsibility and dependency boundaries justify the additional projects. |
| Evidence-based claims | Required | Distinguish designed, implemented, and observed/verified behavior. Record exact revisions and real test results. |
| Research-first technical decisions | Required | When decisions depend on external platform, framework, or tooling behavior, consult applicable authoritative guidance before inventing a solution or discovery experiment; verify its applicability to the actual project. |

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
