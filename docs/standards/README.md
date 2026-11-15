# Engineering standards catalog

This index identifies engineering practices that the .NET Project Playbook can use when proposing a new project's foundation or assessing an existing repository. The linked standard, not its index entry, owns the normative expectation. The [standards governance](../governance/standards.md) defines obligation levels, conditional applicability, exceptions, and identifier rules.

The catalog is **an initial subset**, not a complete set of .NET engineering standards or an automated compliance checker. Subsequent issues will add detailed guidance and further standards without changing the identities already assigned. For C# conventions already established by Microsoft, consult the [Microsoft C# guidance map](../csharp-guidance.md) directly; the C# standards below capture only deliberate playbook obligations or choices.

## Registered standards

| ID | Category | Standard | Level | Applicability at a glance |
| --- | --- | --- | --- | --- |
| `STD-001` | Testing | [Test-driven development](engineering-principles.md#std-001) | Required | New executable behavior and defect corrections; justified exceptions remain possible. |
| `STD-002` | Verification | [CI/local parity](engineering-principles.md#std-002) | Recommended | When CI exists, prefer repository-controlled checks runnable locally and called by CI. |
| `STD-003` | Architecture | [Separate compiled projects](engineering-principles.md#std-003) | Optional | Add physical boundaries when responsibilities and dependencies justify them. |
| `STD-004` | C# naming | [Microsoft-aligned public C# naming](csharp.md#std-004) | Required | New or intentionally renamed externally visible C# identifiers, subject to reviewed exceptions. |
| `STD-005` | C# organization | [Readability-first C# source organization](csharp.md#std-005) | Recommended | Human-maintained C# files where a readable layout choice is meaningful. |
| `STD-006` | C# nullability | [Nullable reference types in new compatible projects](csharp.md#std-006) | Required | New C# projects with a supported language, target framework, and toolchain combination. |
| `STD-007` | C# configuration | [Repository-controlled EditorConfig in new C# projects](csharp.md#std-007) | Required | Newly established C# projects, satisfied by an applicable tracked EditorConfig. |
| `STD-008` | C# diagnostics | [Risk-based compiler and analyzer enforcement](csharp.md#std-008) | Recommended | Where compiler and supported analyzer diagnostics can be meaningfully reviewed. |
| `STD-009` | Testing | [Representative external-boundary verification](testing.md#std-009) | Required (conditional) | Materially significant new or changed external-adapter behavior; use representative real dependencies or appropriately validated contracts. |
| `STD-010` | Design | [SOLID design principles](solid.md#std-010) | Required | New or materially changed object-oriented C# design; apply all five principles in context without mandatory speculative abstractions. |
| `STD-011` | Architecture | [Business-policy dependency direction](dependency-direction.md#std-011) | Required | Business-policy code in new or materially changed .NET code; independence by responsibility, without mandatory compiled layers. |
| `STD-012` | Architecture | [Hexagonal (Ports and Adapters) architecture](hexagonal.md#std-012) | Recommended | Meaningful application/adapter boundaries; when adopted, explicit interfaces for every inbound and outbound port, including single-implementation ports. |

These rows provide navigation and short applicability summaries. Consult the [authoritative engineering principles](engineering-principles.md), [playbook-specific C# standards](csharp.md), [external-boundary testing standard](testing.md), [SOLID standard](solid.md#std-010), [business-policy dependency standard](dependency-direction.md#std-011), [Hexagonal Architecture standard](hexagonal.md#std-012), and [governance](../governance/standards.md) for actual expectations, exceptions, and meanings of Required, Recommended, and Optional. A catalog entry does not establish that a target repository complies.

## Applying the catalog to a project

Determine the project's purpose, project type, target framework, supported operating systems, and known constraints. Inspect an existing repository's actual files and decisions before reaching a conclusion. The project's type alone does not establish compliance or justify adding extra projects and configuration files.

| Project context | How to interpret the initial standards |
| --- | --- |
| Class library | Apply SOLID, business-policy independence, and TDD to applicable new behavior and fixes; a pure library need not adopt Hexagonal Architecture or physical layers. STD-009 does not apply without a significant external-adapter boundary. |
| Command-line application | Assess the same practices against its actual dependencies and test surfaces; introduce CI/local parity guidance when CI is present. |
| Web API | Assess the same foundation practices while recognizing that hosting, infrastructure, and security details require further applicable standards. |
| Worker | Assess applicable engineering practices without assuming the application needs web presentation or a prescribed project graph. |
| Modern SDK-style .NET | Use the project's actual SDK and target framework to select meaningful verification; do not infer untested OS support from the project format. |
| Traditional .NET Framework | Retain applicable engineering principles while accounting for legacy project/tooling constraints and Windows-only runtime behavior. |

These are **applicability notes**, not an exhaustive or profile-specific standards matrix. A Recommended standard may have a justified alternative, an Optional standard need not be adopted, and a conditional standard cannot be treated as a failure when its trigger is absent. If evidence is missing, report the assessment as unknown rather than assuming compliance or a defect. For C# projects, use the [Microsoft C# guidance map](../csharp-guidance.md) to identify the applicable official recommendations before applying the additional playbook obligations.

## Where additional standards belong

Group related standards in topic-oriented Markdown documents as those standards are approved. Each independently assessable practice receives one permanent global identifier. Categories can change, but identifiers cannot; individual EditorConfig keys and other low-level configuration settings ordinarily remain implementation details of a practice.

The [testing guide](../testing-guidance.md) expands practical test selection without creating an ID for every technique. The [dependency-direction guide](../dependency-direction-guidance.md) illustrates practical policy boundaries without creating a second Required definition. The [Hexagonal guide](../hexagonal-guidance.md) offers optional C# examples and boundary-test explanations without redefining STD-012. Future topic guidance will further address design and architecture, build and dependency management, security, compatibility, requirements, and verification. Do not create placeholder files merely to reserve these topics or IDs. Existing Microsoft guidance should be linked rather than redefined in new playbook standards unless a deliberate deviation or stronger obligation is approved.

For interactive project setup and read-only existing-repository assessment, follow the single [start-here guide](../../start-here.md). Reusable consumer templates, executable checks, and comprehensive domain guidance are not yet available through this catalog.
