# Engineering principles

This is the authoritative baseline for engineering principles applied to projects using the playbook. [Standards governance](../governance/standards.md) defines what each obligation level means and how exceptions are approved. More detailed implementation standards will be introduced by future issues.

| Principle | Level | Application |
| --- | --- | --- |
| SOLID | Required | Design maintainable responsibilities, substitutions, interfaces, and dependency boundaries appropriate to the code. |
| Test-driven development | Required default practice | For new behavior and defect fixes, write a meaningful failing test, implement minimally, then refactor. Explain a justified verification-only or documentation exception. |
| Dependency direction | Required | Keep business policies independent of concrete infrastructure and presentation mechanisms. |
| Automated verification | Required where practical | Check important behavior and applicable structural constraints with locally reproducible evidence. Document gaps. |
| CI/local parity | Recommended implementation pattern | Keep underlying validation in repository-controlled scripts; let CI provision tools, select environments, and publish results. |
| Hexagonal (Ports and Adapters) architecture | Preferred | Define ports where they are consumed, keep adapters outside business logic, and use the pattern where it clarifies real dependencies. |
| Separate compiled projects | Conditional | Separate Domain, Application, Infrastructure, and presentation when responsibility and dependency boundaries justify the additional projects. |
| Evidence-based claims | Required | Distinguish designed, implemented, and observed/verified behavior. Record exact revisions and real test results. |

## Architectural interpretation

SOLID and independence from infrastructure apply even to small class libraries. Hexagonal architecture is the preferred way to express boundaries when there are external adapters. It does **not** mandate four physical projects for every application. A complex service may need multiple independently compiled layers; a small pure library may need only the library and its tests.

New abstractions should serve an actual dependency, extension requirement, or testing seam. Avoid speculative project layers and wrappers. Test selection and architecture checks must match the concrete project rather than blindly reusing another repository's project graph.

## Verification and applicability

Relevant unit/component/integration tests, dependency-direction checks, and peer or owner review provide complementary evidence. No one static gate proves SOLID or full hexagonal correctness. A passing build does not establish scenario acceptance, security, release readiness, or cross-platform behavior that was not exercised.

Project-type implementation guidance belongs to future standards and templates. Refer to the [template model](../architecture/template-model.md) for the planned profiles rather than treating future deliverables as present features.
