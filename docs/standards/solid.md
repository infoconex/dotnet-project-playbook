# STD-010 — SOLID design principles

The playbook adopts Microsoft's published .NET architectural and C# design guidance as its technical default. This standard records the playbook's **stronger Required obligation to apply SOLID** and explains how to assess that obligation without prescribing a particular project graph or an interface for every class.

The [engineering-principles baseline](engineering-principles.md) establishes this obligation; the [standards catalog](README.md) provides its permanent ID and navigation. The [SOLID guidance](../solid-guidance.md) contains non-normative C# examples and optional learning levels. The [standards governance](../governance/standards.md) controls applicability and exceptions.

## <a name="std-010"></a>Purpose and applicability

**Level: Required.** Apply the five SOLID principles to new and materially changed object-oriented C# design in projects using the playbook, from a small class library to a larger application. Assess each principle in the context of the responsibilities, contracts, and change pressures actually present. Existing code is not automatically noncompliant because it predates the playbook; assess a legacy change against the behavior and boundaries it affects.

SOLID addresses maintainable object design; it does **not** require a particular architecture style, dependency-injection container, directory layout, number of compiled projects, or use of inheritance. [STD-003](engineering-principles.md#std-003) continues to make separate compiled projects Optional. The distinct Required architectural expectation that business policies remain independent of concrete infrastructure and presentation is defined by [STD-011 — Business-policy dependency direction](dependency-direction.md#std-011), which expands the [engineering-principles baseline](engineering-principles.md) without redefining SOLID.

## Normative expectation

Design the code so the five related principles hold where applicable:

| Principle | Required design expectation | Review question |
| --- | --- | --- |
| **Single Responsibility (SRP)** | Keep responsibilities cohesive and separate changes driven by unrelated actors or reasons. | Would unrelated business or technical reasons repeatedly require changing this type? |
| **Open/Closed (OCP)** | Where an actual variation or extension requirement exists, prefer a stable contract that admits the new behavior without repeatedly editing established dispatch logic. | Is a known axis of variation implemented through repeated conditionals in a central class, or would an extension point be premature? |
| **Liskov Substitution (LSP)** | Derived types and implementations must honor the behavioral promises of the contracts they claim to implement, including valid inputs, outcomes, invariants, and failure behavior. | Could a valid consumer use this implementation in place of another without an unexpected contract violation? |
| **Interface Segregation (ISP)** | Expose contracts appropriate to actual consumers, without making them depend on operations irrelevant to their responsibility. | Is a consumer forced to know about or implement capabilities it does not use? |
| **Dependency Inversion (DIP)** | At meaningful high-level/low-level boundaries, make policy depend on an appropriate abstraction rather than a concrete technical detail; place that contract according to the consuming policy. | Does a business decision directly require a replaceable infrastructure mechanism? |

These are **design obligations, not mechanical quotas**. A concrete class can satisfy SOLID. Introducing an interface with one implementation purely because a unit test can mock it, fragmenting a cohesive type into trivial classes, or inventing a plugin mechanism without a credible extension requirement can make the design worse. Existing tests and actual requirements help reveal which seams and substitutions matter.

## Applying the expectation proportionately

- **Small pure library:** Keep meaningful responsibilities and honest contracts within the library. Direct dependencies on stable, simple collaborators are fine. A library does not need Domain, Application, Infrastructure, and Presentation assemblies merely to demonstrate SOLID.
- **Application with external dependencies:** Apply SRP and DIP around real business-policy and infrastructure concerns. Where a policy needs storage, messaging, time, or a remote system, a consumer-oriented port can be appropriate; the exact project boundaries remain a separate decision.
- **Modern .NET and .NET Framework:** The principles are framework-independent. Select C# features supported by the actual compiler, language version, project format, and target; do not assume modern syntax in an older C# 7.3 toolchain or assume .NET Framework alone determines the language version.
- **Existing code:** Prefer focused, behavior-preserving improvements around the change rather than a mechanical whole-repository rewrite. Preserve published contracts unless a compatibility-conscious migration is authorized.

The [practical guidance](../solid-guidance.md#level-2-practical-c-examples) shows representative violations, improvements, and countervailing tradeoffs; its examples illustrate this standard rather than defining additional requirements. [STD-001](engineering-principles.md#std-001) governs the test-first process when executable behavior changes, while [STD-009](testing.md#std-009) governs representative external-boundary evidence when its trigger applies.

## Verification and limits

Use review evidence appropriate to the actual change:

1. Identify the relevant business responsibilities, expected variations, substitutable contracts, consumers, and concrete technical dependencies.
2. Inspect the changed classes and their callers, tests, and contract behavior. Look for multiple independent reasons to change, repeated extension conditionals, substitution failures, unused contract members, and policy coupled to concrete technology.
3. Use compiler/project-reference checks and behavioral or contract tests where they can establish a specific property. A passing build cannot establish SRP or OCP; dependency graphs cannot establish LSP's behavioral promises; a unit-test count cannot establish that the abstractions are necessary.
4. Record reviewed artifacts, the exact revision, actual checks/results, unresolved design judgments, and any unverified cases. Do not call a manual review a CI pass or infer a successful test from sample code.

No generalized SOLID analyzer or new CI gate is introduced by this documentation-only standard. Future validation automation may check specific objective constraints when it provides demonstrable value.

## Exceptions and alternatives

Required standards permit only justified, explicitly reviewed and recorded exceptions under [standards governance](../governance/standards.md#applicability-levels). An exception should identify the concrete contract or boundary affected, why compliance is not currently practical (for example, a fixed third-party API, a backward-compatible published surface, or difficult legacy coupling), the least-disruptive alternative, verification actually performed, residual risk, and follow-up when appropriate. Inconvenience or a preference for fewer files alone does not justify an actual contract violation.

Not creating an unnecessary interface, subclass, adapter, or compiled project is **not an exception**: SOLID does not demand those structures. A Recommended or Optional architecture style may be omitted according to its applicability without requiring an exception to STD-010.

## Authoritative Microsoft references

- [.NET architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles) — responsibility, encapsulation, abstraction, and dependency inversion.
- [Designing the application layer and using SOLID](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-application-layer-web-api-design) — the five principles and the distinction between dependency inversion and injection.
- [Framework Design Guidelines: interface design](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/interface) — when interfaces help and when classes are preferable.
- [C# interfaces](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/interfaces) — language contracts and interface/abstract-class distinctions.

These sources explain general Microsoft guidance; the Required applicability and exception rules above are the playbook's explicit choice. No external article or illustrative code block replaces the authoritative expectation in this document.
