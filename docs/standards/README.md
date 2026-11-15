# Engineering standards catalog

This index identifies engineering practices that the .NET Project Playbook can use when proposing a new project's foundation or assessing an existing repository. The linked standard, not its index entry, owns the normative expectation. The [standards governance](../governance/standards.md) defines obligation levels, conditional applicability, exceptions, and identifier rules.

The catalog is **an initial subset**, not a complete set of .NET engineering standards or an automated compliance checker. Subsequent issues will add detailed guidance and further standards without changing the identities already assigned.

## Registered standards

| ID | Category | Standard | Level | Applicability at a glance |
| --- | --- | --- | --- | --- |
| `STD-001` | Testing | [Test-driven development](engineering-principles.md) | Required | New executable behavior and defect corrections; justified exceptions remain possible. |
| `STD-002` | Verification | [CI/local parity](engineering-principles.md) | Recommended | When CI exists, prefer repository-controlled checks runnable locally and called by CI. |
| `STD-003` | Architecture | [Separate compiled projects](engineering-principles.md) | Optional | Add physical boundaries when responsibilities and dependencies justify them. |

These rows provide navigation and short applicability summaries. Consult the [authoritative engineering-principles table](engineering-principles.md) and [governance](../governance/standards.md) for the actual expectations, exceptions, and meanings of Required, Recommended, and Optional. A catalog entry does not establish that a target repository complies.

## Applying the catalog to a project

Determine the project's purpose, project type, target framework, supported operating systems, and known constraints. Inspect an existing repository's actual files and decisions before reaching a conclusion. The project's type alone does not establish compliance or justify adding extra projects and configuration files.

| Project context | How to interpret the initial standards |
| --- | --- |
| Class library | Apply TDD to applicable new behavior and fixes; project separation remains optional rather than a mandatory layered solution. |
| Command-line application | Assess the same practices against its actual dependencies and test surfaces; introduce CI/local parity guidance when CI is present. |
| Web API | Assess the same foundation practices while recognizing that hosting, infrastructure, and security details require further applicable standards. |
| Worker | Assess applicable engineering practices without assuming the application needs web presentation or a prescribed project graph. |
| Modern SDK-style .NET | Use the project's actual SDK and target framework to select meaningful verification; do not infer untested OS support from the project format. |
| Traditional .NET Framework | Retain applicable engineering principles while accounting for legacy project/tooling constraints and Windows-only runtime behavior. |

These are **applicability notes**, not an exhaustive or profile-specific standards matrix. A Recommended standard may have a justified alternative, an Optional standard need not be adopted, and a conditional standard cannot be treated as a failure when its trigger is absent. If evidence is missing, report the assessment as unknown rather than assuming compliance or a defect.

## Where additional standards belong

Group related standards in topic-oriented Markdown documents as those standards are approved. Each independently assessable practice receives one permanent global identifier. Categories can change, but identifiers cannot; individual EditorConfig keys and other low-level configuration settings ordinarily remain implementation details of a practice.

Future topic guidance will address C# conventions, testing, design and architecture, build and dependency management, security, compatibility, requirements, and verification. Do not create placeholder files merely to reserve these topics or IDs.

For interactive project setup and read-only existing-repository assessment, follow the single [start-here guide](../../start-here.md). Reusable consumer templates, executable checks, and comprehensive domain guidance are not yet available through this catalog.
