# STD-013 — Clean Architecture

The playbook uses [Microsoft's .NET architecture guidance](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) as its technical default. This standard records a **Recommended, context-sensitive adoption choice** and makes the distinguishing Clean Architecture property independently assessable: **the entire logical Application Core remains independent of concrete infrastructure and presentation at compile time**.

This document owns the STD-013 expectation. The [standards catalog](README.md) indexes it, [engineering principles](engineering-principles.md) identify its level, [standards governance](../governance/standards.md) governs alternatives, and [on-demand Clean Architecture guidance](../clean-guidance.md) offers non-normative C# examples and review questions.

## <a name="std-013"></a>Purpose and applicability

**Level: Recommended.** Prefer Clean Architecture for a new or materially changed application with meaningful business use cases, dependencies on external mechanisms, or architectural complexity for which a protected Application Core would improve independent testing, maintainability, or adaptability. This includes relevant web APIs, workers, CLI applications, and libraries that expose application behavior across material integration boundaries.

For small pure libraries, simple applications, or trivial technical collaborations without meaningful application boundaries, a documented simpler architecture can be more appropriate. Determine applicability from actual responsibilities and dependencies, not a repository label, application profile, framework version, or number of projects. Existing systems can adopt Clean Architecture incrementally around changed behavior without a wholesale rewrite.

**Conditional adoption:** This is a Recommended architecture *choice*. A project that does not adopt it does not violate STD-013 merely by omitting an Application Core. When a project claims Clean Architecture for a scope, assess that scope against the adopted core-wide boundary rules below. Choosing a different architecture does not waive independently [Required business-policy independence under STD-011](dependency-direction.md#std-011), [SOLID under STD-010](solid.md#std-010), TDD, or conditional external-adapter verification.

## Normative expectations when adopted

1. **Identify the logical Application Core.** Define which domain model, domain policy, application use cases, application decisions, and contracts constitute the protected core. Domain concepts must not depend on application orchestration. A library with no application use cases need not invent an Application layer.
2. **Keep all core compile-time dependencies inward.** Domain and application-core source must not require concrete database clients, provider-specific persistence types, UI frameworks, controllers, host implementations, filesystems, network clients, infrastructure adapters, or other presentation/technical implementations to compile or express their behavior. Application use cases may depend on domain concepts, stable runtime primitives, and suitable technology-neutral contracts. This protection applies to *all code designated as Application Core*, not just code recognized as business policy.
3. **Own external capability abstractions inward.** When the core requires a meaningful capability supplied by infrastructure, define an appropriately small, consumer-oriented abstraction in the core or another suitable inward, technology-neutral location. An outward implementation depends inward on that contract. Do not expose provider DTOs, configuration mechanisms, or vendor APIs through the core's contract merely to hide an implementation behind an interface. Clean Architecture alone does **not** require an explicit C# interface for every use case or internal collaborator.
4. **Keep outer responsibilities outer.** Infrastructure handles concrete integrations and translates them into core contracts. Presentation/transport accepts inputs, invokes application behavior, and translates outputs; it does not own decisions that belong to the core. Purely technical orchestration requiring direct infrastructure dependencies belongs outside the protected Application Core, even if another architectural style might call it an application service.
5. **Compose at an outer boundary.** A host, entry point, or dedicated composition root may know both core types and concrete implementations to select, configure, construct, and manage lifetimes. Its deliberate outward references are not core dependency violations. Constructor injection, manual factories, and supported DI containers can all compose the application; a particular container is not mandatory.
6. **Distinguish compile-time references from runtime calls.** At runtime, a use case can invoke a core-owned abstraction implemented by an infrastructure adapter. That outward *execution* does not create an outward *source dependency* in the core. Assess actual source/type references and responsibility placement, not call-stack direction or namespace names alone.
7. **Separate logical from physical boundaries.** Preserve these responsibilities even in a single compiled project. Introduce separate assemblies when compile-time enforcement, team boundaries, reuse, or project complexity make them valuable. [STD-003](engineering-principles.md#std-003) keeps separate compiled projects **Optional**; no prescribed four-project graph, folder hierarchy, or distributed deployment is required.

These expectations define the chosen Clean Architecture style; they are not a new universal rule that all application code must be infrastructure-free. A technical coordinator outside the protected core can legitimately depend directly on infrastructure when it does not violate independently Required policy independence.

## Responsibility map and dependency direction

These are **logical roles**, not mandatory assemblies. A single type can blur the roles in legacy code; assess what it actually does before declaring a boundary compliant.

| Role | Main responsibility | Permitted compile-time knowledge |
| --- | --- | --- |
| **Domain** | Entities, value objects, invariants, and domain decisions | Domain concepts and appropriate technology-neutral types; not application orchestration, infrastructure, or presentation |
| **Application Core** | Application use cases, coordination of domain behavior, application policy, and consumer-oriented external capability contracts | Domain and inward-owned abstractions; not concrete infrastructure or presentation |
| **Infrastructure** | Persistence, messaging, files, network/service providers, and implementation-specific integration | The core contracts it implements plus relevant technical dependencies |
| **Presentation/transport** | HTTP, CLI, UI, job trigger, or other entry-point translation | Application-facing operations and presentation mechanisms; no business policy displaced into the edge |
| **Composition root** | Select and wire implementations; configure lifetimes and host startup | Both core and infrastructure/presentation implementations, limited to composition concerns |

An illustrative multi-assembly reference arrangement is `Application -> Domain`, `Infrastructure -> Application`, and `Host -> Application + Infrastructure`. The host's reference to Infrastructure belongs in composition. In a single assembly, those exact project edges cannot be enforced by the compiler; the logical source dependencies must still be reviewed. A separate UI assembly may use application-facing contracts without directly using infrastructure types, apart from a deliberate host composition boundary.

## Relationship to existing standards

| Authority | Independent responsibility |
| --- | --- |
| [STD-010 — SOLID](solid.md#std-010) | Required object-level responsibilities, behavioral substitution, interfaces, and Dependency Inversion; no interface quota |
| [STD-011 — Business-policy dependency direction](dependency-direction.md#std-011) | Required independence of business decisions from concrete infrastructure/presentation in **every** applicable .NET design, adopted Clean Architecture or not |
| [STD-012 — Hexagonal (Ports and Adapters)](hexagonal.md#std-012) | Separately Recommended application/adapter boundary style; **if adopted**, explicit C# interfaces for every identified inbound and outbound port, even with one implementation |
| [STD-003 — Separate compiled projects](engineering-principles.md#std-003) | Optional enforcement mechanism, never a prerequisite to Clean Architecture |
| [STD-001 — TDD](engineering-principles.md#std-001) and [STD-009 — Real-boundary verification](testing.md#std-009) | Independent behavioral development and conditional significant external-adapter evidence |

Clean and Hexagonal Architecture overlap in inversion and boundary isolation, but their reviewable claims differ. Clean identifies and protects an *entire Application Core*; Hexagonal specifies explicit *inbound and outbound port interfaces* and driving/driven adapter roles. Adopting one does not automatically adopt the other. When both are adopted, satisfy both requirements without duplicating interfaces or introducing meaningless forwarding types.

## Applying the recommendation proportionately

- **Small pure library:** Cohesive domain types and tests may be enough. No artificial Application, Infrastructure, Presentation, adapter, or composition project is needed. Continue satisfying applicable Required standards.
- **Dependency-rich application:** Identify actual use cases and external capabilities, put application behavior and its capability abstractions inward, and put provider/transport details outward. Adopt only as many physical projects as provide value.
- **Modern .NET and .NET Framework:** Logical roles and the dependency rule are framework-independent; select DI mechanisms, C# syntax, project references, and analyzers supported by the *actual* compiler, framework, project format, and target environment. Built-in ASP.NET Core DI, SDK-style project files, and modern C# language features are not prerequisites.
- **Existing/legacy application:** Find affected use cases and real concrete dependencies, characterize current behavior where useful, and move the smallest meaningful core boundary inward while preserving published contracts. Do not infer that untouched legacy code must be reorganized wholesale.

See the [illustrative application, counterexample, and simpler alternatives](../clean-guidance.md#level-2-c-and-dependency-examples). Those snippets are explanations, not tested templates.

## Proportional verification and evidence limits

When Clean Architecture is adopted and meaningful boundaries are created or materially changed, gather evidence proportional to impact:

1. **Locate and trace the core.** Review use cases, domain decisions, outward contracts, concrete dependencies, and the composition root. Inspect actual code, not only assembly/namespace labels. Where separate assemblies exist and useful checks are practical, inspect project references or architecture rules for prohibited outward edges; a project graph cannot establish responsibility placement.
2. **Exercise meaningful core behavior independently.** Test application use cases with controlled substitutes for actual external capabilities and verify relevant outcomes and failures without requiring the real transport or persistence system. [STD-001](engineering-principles.md#std-001) governs TDD when behavior changes; a final green suite cannot prove test-first chronology.
3. **Verify material composition changes.** Exercise significant host registration, construction, lifetime, or startup paths when changed. A unit test of the core alone cannot demonstrate correct runtime wiring.
4. **Verify significant external adapters under STD-009.** Where its risk-based trigger applies, obtain representative real-dependency or appropriately validated contract evidence, with reviewed exceptions. Core substitutes do not establish provider correctness.
5. **Review semantic properties and report limits.** Check whether implementation details leak through ostensibly inward contracts, whether policy has drifted outward, and whether added abstractions improve isolation. Record the exact revision, actually executed commands/results, files reviewed, exceptions/alternatives, and unverified surfaces. A successful build or dependency scan does not prove architectural quality.

Do not mandate a particular analyzer, CI job, compiled project graph, or a test for every trivial forwarding method. This documentation-only standard introduces no executable validator. The [practical review guide](../clean-guidance.md#level-3-review-testing-and-migration) provides possible checks and explains their limits.

## Alternatives and reviewed deviations

Because STD-013 is **Recommended**, a project may select and document a simpler arrangement when its responsibilities, external dependencies, and change pressures do not justify Clean Architecture. Record the reason and tradeoff at the architectural decision or assessment point. That is not an exception to Required STD-011, SOLID, TDD, or conditional STD-009.

If a project *claims* Clean Architecture yet places a concrete infrastructure dependency inside its designated core, do not report that scope as conforming merely because domain business rules remain independent. Either correct the boundary, place truly technical coordination outside the core, or describe the actual alternative/deviation and its consequences. If a Required standard is also violated, follow its [explicit reviewed-exception process](../governance/standards.md#applicability-levels). Avoid inventing abstractions or changing public APIs solely to match an illustrative directory layout.

## Authoritative Microsoft references

- [Common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) — Clean Architecture Application Core, compile-time versus runtime direction, responsibilities, and composition-root exception.
- [Architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles) — separation of concerns, explicit dependencies, abstraction, and Dependency Inversion.
- [Implementing the application layer using Web API](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-application-layer-implementation-web-api) — alternative application-layer placement and DI examples; not every Microsoft sample uses Clean Architecture's protected-core boundary.
- [Dependency injection guidelines](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines) — selecting and managing composition in supported .NET applications.

Microsoft's sources describe general approaches; **Recommended adoption and the explicit adopted-core boundary** are the playbook's reviewed decisions. No external template or illustrative sample supersedes this standard.
