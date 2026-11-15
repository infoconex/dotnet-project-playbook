# STD-012 — Hexagonal (Ports and Adapters) architecture

The playbook follows Microsoft's published .NET architecture guidance by default. This standard makes the existing **Recommended** Hexagonal Architecture principle independently assessable, with a deliberate playbook choice: **every identified inbound and outbound port has an explicit interface when the pattern is adopted**, including ports with one implementation. It does not require every project to adopt the pattern or every collaborator to become a port.

The [standards catalog](README.md) indexes this permanent ID. [On-demand C# guidance](../hexagonal-guidance.md) illustrates the roles, tests, and alternatives without creating another normative definition. [Standards governance](../governance/standards.md) explains how Recommended practices and alternatives are assessed.

## <a name="std-012"></a>Purpose and applicability

**Level: Recommended.** Prefer Hexagonal Architecture when a new or materially changed .NET application or library has **meaningful external-adapter or dependency boundaries**: persistence, remote services, messaging, presentation/transport, device or file I/O, testable application policy, or credible implementation substitution. The decision should account for independent testing and isolation of business policy, not just the current number of implementations. The pattern can be useful in a single compiled project.

For a small pure library or trivial technical collaboration with no meaningful boundary, a documented, simpler design is appropriate. A technical component does not become a hexagon merely because it has an interface. This Recommended style is not a compulsory architecture for every repository; once a project **chooses to adopt** it for a boundary, the port expectations below define what that adoption means.

The guidance applies to both modern .NET and .NET Framework using their actual language versions, project formats, and runtime capabilities. [STD-003](engineering-principles.md#std-003) continues to make separate compiled projects **Optional**; no dependency-injection framework or universal layer count is mandated.

## Port, adapter, and dependency expectations when adopted

1. **Identify real application boundaries.** Name the application behavior exposed to outside actors and the external capabilities that behavior consumes. Define a port only for an identified interaction across a meaningful boundary. Do not wrap every internal function, value type, calculation, or stable technical collaborator.
2. **Declare an explicit interface for every inbound port.** An inbound (driving/primary) port describes an application operation available to a driving actor such as a controller, CLI, scheduled job, or test. The port is an explicit C# interface with an application-oriented contract. A driving adapter depends on that interface instead of the concrete use-case implementation. This holds even when one driving adapter or one use-case implementation exists.
3. **Declare an explicit interface for every outbound port.** An outbound (driven/secondary) port describes an external capability the application needs. Put its explicit C# interface with the consuming application or policy boundary (or another appropriately inward, technology-neutral location); an outer adapter implements it. Application policy depends on the port, not a database client, network library, file system, or provider implementation. This holds with one adapter implementation.
4. **Keep adapters focused on translation and technical integration.** Driving adapters translate transport/user/host inputs into inbound-port calls and responses into appropriate outputs. Driven adapters implement outbound ports using concrete technologies. Keep business decisions in the relevant domain/application policy; do not hide them in adapters or provider-specific DTOs. Port contracts should describe consumer needs and stable business concepts, not leak an adapter's vendor API.
5. **Compose at an outer boundary.** A composition root may construct concrete use cases and adapters, register them in a DI container, and connect interfaces to implementations. Constructor injection and manual wiring are both valid. Composition's reference to concrete infrastructure is not an inversion violation.
6. **Distinguish source dependencies from execution.** At compile time, application policy knows its ports and domain types; the driven implementation knows the port it implements. At runtime a call can travel from a driving adapter through an inbound port and use case to a driven adapter through an outbound port. The runtime call direction does not require an inward compile-time reference to the implementation.

An interface is a **port** only if it expresses an identified external application interaction. The explicit-interface rule above is **conditional on adopting Hexagonal Architecture**; it does not override the [SOLID standard](solid.md#std-010) for ordinary internal collaborators or make speculative interfaces universally necessary. Port interfaces should be cohesive, honest, and behaviorally substitutable. A single implementation is not, by itself, a reason to omit an identified port's interface after adopting the pattern.

## Responsibilities and physical layout

| Logical role | Owns | Source dependency direction |
| --- | --- | --- |
| Domain/application policy | Business rules and use cases; applicable port contracts | Domain concepts and technology-neutral ports, not concrete adapter implementations |
| Inbound port | Application-facing use-case interface | Contracts and business types understood by the application |
| Driving adapter | HTTP endpoint, CLI command, UI presenter, background trigger, or other caller | Inbound port, not a specific use-case class |
| Outbound port | Application-owned requirement for persistence, time, messaging, external service, etc. | Technology-neutral consumer contract |
| Driven adapter | Concrete implementation of an outbound port | The port it fulfills plus its technical dependencies |
| Composition root | Concrete instantiation, configuration, and lifetime ownership | Both application ports/implementations and concrete adapters as needed |

These are **roles**, not six required assemblies, directories, namespaces, or separately packaged artifacts. One assembly can maintain meaningful logical boundaries; several projects may enforce valuable compile-time edges. [STD-011](dependency-direction.md#std-011) independently requires business-policy independence from concrete infrastructure and presentation **whether or not Hexagonal Architecture is chosen**. Thin purely technical orchestration may depend on infrastructure directly under STD-011 if it contains no business policy; a project claiming a particular interaction as a hexagonal port still uses an explicit interface for that port.

## Proportional boundary verification

For materially changed hexagonal behavior, select tests that establish meaningful independent properties rather than merely counting interfaces or test doubles:

1. **Application through inbound port:** Exercise significant use-case behavior through the inbound interface while replacing outbound adapters with controlled substitutes. Verify business outcomes, decisions, and relevant failure behavior independently of the real external system.
2. **Significant driving adapter:** Exercise its translation, request/response mapping, or failure-handling behavior against a substituted inbound port. This tests how the actor reaches the application without entangling use-case behavior.
3. **Significant driven adapter:** Verify its actual integration with a representative real external dependency or appropriately provider-validated contract **when the risk-based trigger of [STD-009](testing.md#std-009) applies**. A fake outbound port cannot establish that the real provider behaves as expected. Where the trigger does not apply, select appropriate tests based on risk.
4. **Assess the boundary, not just mechanics:** Review port ownership and interfaces, concrete dependency references, policy isolation, adapter responsibilities, and the composition root. Use objective project-reference or architecture checks where they provide useful evidence, combined with semantic review. No universal analyzer, new CI tool, or mandatory per-port test for trivial forwarding is required.

[STD-001](engineering-principles.md#std-001) still governs TDD for new behavior and defect fixes. [STD-009](testing.md#std-009) owns real-dependency evidence and reviewed exceptions where it applies. Record the actual commands, versions, tests and outcomes, reviewed paths, unverified surfaces, and justified omissions. A compiling graph or passing isolated tests does **not** prove the runtime adapter works or that business policy is isolated. See the [illustrative test strategy](../hexagonal-guidance.md#level-3-testing-review-and-adoption).

## Adoption, alternatives, and exceptions

- **Adopt with meaningful boundaries:** A service with an external database and transport layer, or a library needing independent application-level tests and swappable integrations, commonly benefits from both types of ports even with one adapter implementation.
- **Use a simpler design where justified:** For a trivial technical operation without meaningful application-policy, external-adapter, or substitution boundaries, direct collaboration can be clearer. Record the decision and its context when assessing or changing architecture; omitting a Recommended style is not an exception to a Required standard.
- **Adopt incrementally:** In legacy systems, define the first useful inbound/outbound boundaries around the affected behavior. Preserve public contracts and characterize existing behavior where practical; there is no required whole-system rewrite or physical reorganization.
- **Handle genuine deviations honestly:** If a project describes a boundary as hexagonal but omits its explicit port interface, identify the reason, alternative, impact on substitution/testing, and appropriate follow-up. Do not silently label direct concrete coupling a port. Under the [standards governance](../governance/standards.md#applicability-levels), Recommended practices allow justified alternatives; any departure from independently Required [STD-010](solid.md#std-010), [STD-011](dependency-direction.md#std-011), or conditional [STD-009](testing.md#std-009) must follow their own applicable exception rules.

## Authoritative Microsoft references

- [.NET common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) — relates Hexagonal/Ports-and-Adapters, Onion, and Clean Architecture, and explains compile-time dependency inversion and runtime composition.
- [.NET architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles) — separation of concerns, explicit dependencies, and abstraction.
- [.NET dependency injection guidelines](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines) — context for composition and lifetime choices when a container is used.

Microsoft guidance is the technical default. The **Recommendation's applicability** and the **explicit interface for every adopted inbound and outbound port** are the playbook's approved choices, not claims that Microsoft universally mandates one interface for every application class.
