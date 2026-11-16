# STD-016 — Vertical Slice Architecture

The playbook follows [Microsoft's .NET architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles) and its [feature-organization guidance](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/develop-asp-net-core-mvc-apps#feature-organization) by default. [Jimmy Bogard's original Vertical Slice Architecture article](https://www.jimmybogard.com/vertical-slice-architecture/) supplies primary context for organizing around requests and the axis of change. His particular CQRS-oriented approach is not a universal Microsoft mandate.

This standard establishes one distinct playbook choice: **when Vertical Slice Architecture is adopted, meaningful application behavior is organized into cohesive units of change with deliberately controlled dependencies between slices**. It does not require an interface, handler, command, query, directory, assembly, or mediator for each operation.

This document alone owns the normative STD-016 expectation. The [standards catalog](README.md) indexes it, [standards governance](../governance/standards.md) defines Recommended adoption and exceptions, and the [on-demand guide](../vertical-slice-guidance.md) provides non-normative examples and review scenarios.

## <a name="std-016"></a>Purpose, level, and applicability

**Level: Recommended (conditional).** Prefer Vertical Slice Architecture for a new or materially changed application with **distinct features or use cases** whose cohesion, independently evolving behavior, testing, or maintenance would benefit from localizing feature changes instead of scattering the implementation through unrelated horizontal technical structures. Evidence may include recurring edits across unrelated services, difficulty locating a use case, change ripple between features, or shared application services collecting unrelated operations.

An HTTP endpoint, command/query class, feature folder, or project's size alone does **not** trigger adoption. A small pure class library, cohesive utility, or straightforward CRUD application may be clearer without recognizable application slices. A library with substantial independently evolving use cases can benefit when its actual responsibilities warrant them. Adoption may cover a feature or application area rather than an entire repository.

**Conditional adoption:** An application that does not adopt this Recommended style is not noncompliant with STD-016 merely because it lacks feature folders or handlers; explain a justified simpler arrangement in the architecture decision or assessment. When an application *claims* Vertical Slice Architecture for a scope, assess that scope against the following adopted-style expectations. No omission or deviation waives independently Required SOLID, test-first development, business-policy independence, or significant external-adapter verification.

## Normative expectations when adopted

1. **Identify meaningful units of behavior and change.** Describe the material features, use cases, or request/response workflows being organized and what each owns. A slice may be one operation or a cohesive group of related operations. Choose boundaries based on business intent, responsibilities, likely independent changes, and coupling—not an endpoint count, class naming convention, or mandatory one-operation-per-handler rule. Reassess a broad feature if unrelated changes repeatedly collide in it, or a fine-grained split if it causes excessive coordination.

2. **Make feature-specific implementation cohesive and discoverable.** Keep the behavior, application orchestration, validation choices, response mapping, and contracts specific to a material slice logically near the operation they serve, as appropriate to the application's tooling. A feature can use shared domain models and infrastructure adapters without copying them into its directory. Avoid forcing each change through unrelated centralized application services, controllers, repository facades, or horizontal folders solely to satisfy an arbitrary layering ceremony. This requirement concerns *logical responsibility and change locality*, not a universal physical folder structure.

3. **Control dependencies and collaboration between slices.** Avoid unnecessarily importing or manipulating another slice's private implementation, persistence details, or mutable state. Where collaboration is genuine, expose an intentional, appropriately scoped operation, facade, application service, or contract; a direct call is valid and an explicit interface is not automatically required. Review meaningful mutual dependencies and recurring coordinated changes as signs that boundaries or ownership may be misplaced. A shared operation should represent real common behavior rather than a catch-all technical service. When [STD-015](modular-monolith.md#std-015) is also adopted, its *module-level* public-contract, implementation-cycle, and data-ownership expectations apply independently.

4. **Distinguish local work from authoritative shared business policy.** Feature-local formatting, mapping, or harmless similar technical code need not be abstracted simply because two slices resemble one another. But a business invariant or decision shared by multiple operations needs an accountable, consistently enforced policy owner; do not create conflicting independent financial, inventory, security, or other consequential rules merely to avoid sharing across slices. The exact domain-model and policy-dependency obligations remain owned by [STD-010](solid.md#std-010), [STD-011](dependency-direction.md#std-011), and, when adopted, [STD-014](ddd.md#std-014). A class called a handler or feature service is not automatically a domain service and cannot conceal forbidden policy-to-infrastructure dependencies.

5. **Choose request handling and read/write separation deliberately.** Direct invocation, cohesive feature-specific application services, standalone request handlers, framework endpoint handlers, and mediated dispatch are alternatives selected for actual clarity, testing, or cross-cutting needs. **No one-handler-per-request, one-class-per-operation, mediator, pipeline, DTO-per-method, generic repository, or third-party framework mandate** is introduced. Commands and queries as operation descriptions are distinct from CQRS with separate read/write models; CQRS, separate persistence stores, event sourcing, and asynchronous messaging are each separate decisions with their own costs and consistency requirements.

6. **Share technical cross-cutting mechanisms without moving business authority out of its owner.** Use appropriately scoped composition, focused services, decorators, middleware, filters, or pipelines for genuine common logging, telemetry, validation, authorization, transaction handling, caching, or exception behavior. Do not require a universal behavior pipeline. Ensure feature-specific authorization and business invariant checks still apply through relevant invocation paths; request-shape validation alone cannot establish domain correctness. Keep technical integration responsibilities and policy dependencies consistent with [STD-011](dependency-direction.md#std-011), adopted [STD-012](hexagonal.md#std-012) or [STD-013](clean.md#std-013), and conditional [STD-009](testing.md#std-009).

7. **Distinguish logical slices from code-access and deployment boundaries.** Slices may reside in one or several production assemblies, with feature-oriented directories and namespaces used when helpful. A C# namespace or directory offers organization, not compiler-enforced isolation; `internal` restricts accessibility across **assemblies**, not between folders within one assembly. Expose public contracts only where the intended consumers need them, and preserve existing external APIs deliberately. [STD-003](engineering-principles.md#std-003) keeps separate compiled projects **Optional**. Do not infer independent deployment, data ownership, or a microservice from a slice boundary.

8. **Verify material slice behavior and boundaries proportionately.** For created or materially changed slices, examine representative successful, rejected, and relevant failure paths, feature-specific changes and their actual dependencies, shared-policy ownership, and significant composition paths. Use independent behavioral tests where meaningful, and verify changed external adapters under [STD-009](testing.md#std-009) when its trigger applies. Combine objective dependency/project-reference checks where useful with semantic review of actual responsibilities. Record the revision, evidence, commands/results, toolchain, exceptions, and unverified properties. Neither directory names, compilation success, a green unit suite, nor a mediator registration proves slice cohesion or correct business rules.

These adopted-style expectations do not redefine the independently Required testing or policy obligations. Their distinctive subject is **feature-level cohesion, change locality, and unnecessary inter-slice coupling**.

## Relationship to existing standards and architectural approaches

| Existing authority or style | Independent responsibility and how it composes with STD-016 |
| --- | --- |
| [STD-001 — TDD](engineering-principles.md#std-001) | Required test-first practice for applicable executable changes, regardless of feature organization. |
| [STD-003 — Separate compiled projects](engineering-principles.md#std-003) | Optional physical enforcement; slices can share one production assembly. |
| [STD-009 — External-boundary verification](testing.md#std-009) | Required on its risk-based trigger; isolated feature tests do not establish actual provider behavior. |
| [STD-010 — SOLID](solid.md#std-010) | Required object-level responsibilities and sound contracts; no interface-per-class quota. |
| [STD-011 — Business-policy direction](dependency-direction.md#std-011) | Required policy independence from concrete presentation/infrastructure in any adopted or unadopted style. |
| [STD-012 — Hexagonal](hexagonal.md#std-012) | Independently Recommended application port/adapter boundaries; **when adopted**, every identified inbound and outbound port needs its explicit interface even if STD-016 otherwise permits direct feature calls. |
| [STD-013 — Clean](clean.md#std-013) | Independently Recommended protection of the entire designated Application Core; core code within a slice must follow its inward compile-time rule when adopted. |
| [STD-014 — DDD](ddd.md#std-014) | Independently Recommended domain language, models, and consistency boundaries when justified; a feature is not automatically a bounded context or aggregate. |
| [STD-015 — Modular Monolith](modular-monolith.md#std-015) | Independently Recommended business-capability module ownership and controlled collaboration in one deployment. Slices can organize **within** modules; neither style requires the other. |
| [Proportionate single-project guidance](../single-project-guidance.md) | Describes compilation/project counts, not application feature decomposition. |
| [Traditional layered/N-tier guidance](../layered-n-tier-guidance.md) | Describes logical technical responsibilities and physical tiers; slices can coexist with layers without disabling policy dependencies. |
| [STD-017 — Microservices](microservices.md#std-017) | Independently Recommended when substantial service-level autonomy is justified; it owns deployment, contract, data and operational boundaries. A slice is not a deployable service. |

Vertical Slice Architecture and Modular Monolith Architecture address **different scales of ownership**: a module owns a business capability and governs collaboration with other modules; a slice groups use-case behavior and the work needed to change it. A single module may contain many slices, and slices can exist in a non-modular-monolith application. Likewise, adopting Hexagonal or Clean Architecture is a separate decision, not a consequence of using feature folders.

## Proportionate applicability and alternatives

| Context | Assessment or reasonable alternative |
| --- | --- |
| Small pure library or utility | Cohesive types and tests often suffice; do not invent endpoints, handlers, or request DTOs. |
| Straightforward CRUD | Feature grouping may aid navigation; direct methods and a conventional service can remain simpler. |
| Business-logic-heavy application | Useful candidate for separating independently changing use cases while sharing genuinely common invariant ownership. |
| Multiple independently evolving features or teams | Favor explicit feature responsibilities and consumers; stronger projects/contracts only when coordination and enforcement justify them. |
| Existing layered application | Adopt around one affected use case when it reduces change scatter; retain appropriate shared domain or infrastructure roles. |
| Modern SDK-style .NET or traditional .NET Framework | Apply logical principles in either; use the *actual* compiler, C# language version, project format, framework, and available build/testing tools. No framework-specific endpoint or DI syntax is universal. |

Document a simpler alternative at the adoption or assessment point when feature slicing adds more ceremony than value. If a scope claims VSA but routinely uses unrelated cross-feature internals or an unrelated centralized service for every change, describe the actual deviation and consequences instead of calling its folders compliant. Preserve behavior and published contracts in incremental modernization; do not require whole-system migration, SDK conversion, or a new assembly graph.

## Proportional verification and evidence limits

1. **Trace representative scenarios to owning operations.** Identify the feature/use case, related application orchestration and contracts, shared domain rules, external capabilities, and actual source files. Explain why the boundary matches independent changes; a diagram cannot establish behavior.
2. **Inspect dependencies and ownership.** Trace changed calls, imports, public APIs, cross-feature private-type access, common services, and policy ownership. When compiled projects enforce an edge, record a real reference/build check where useful. In one assembly, supplement with source-level inspection; neither method alone proves architectural quality.
3. **Exercise meaningful feature behavior.** Use the application's suitable NUnit, xUnit, MSTest, or other supported test mechanism for important allowed/rejected paths, domain outcomes, security decisions, and relevant failure behavior. Follow STD-001 for applicable test-first development; completed green tests do not prove test-first chronology. Trivial forwarding does not demand redundant tests.
4. **Verify significant integration and composition paths.** Test meaningful host wiring and real transaction/authorization semantics where modified. Apply STD-009 for materially changed external adapters using representative dependencies or validated contracts. Fakes do not prove SQL concurrency, messaging delivery, network behavior, or production startup.
5. **Report the actual verification boundary.** Identify exact SHA, paths, commands/test results, versions/environment, manual judgments, remaining risks, and intentionally unverified properties. Do not label documentation examples as compiled, executed, or CI-validated without that evidence.

The [on-demand Vertical Slice guidance](../vertical-slice-guidance.md) illustrates proportional scenarios and alternative implementations. Those snippets and review scenarios are *examples*, not a verified test suite or mandatory project template.

## Authoritative and supplementary primary references

- [Microsoft — Architectural principles for .NET](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles): separation of concerns, encapsulation, dependency inversion, and explicit collaborators.
- [Microsoft — Developing ASP.NET Core MVC apps: Feature organization](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/develop-asp-net-core-mvc-apps#feature-organization): feature-oriented layout alongside application architecture.
- [Microsoft — CQRS pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs): logical read/write model separation, optional data-store separation, and added complexity.
- [Microsoft — Designing a DDD-oriented service](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice): domain invariants, application coordination, and infrastructure ignorance in that DDD-oriented example.
- [Microsoft — Implementing the application layer using Web API](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-application-layer-implementation-web-api): mediator/handler *example*, not a universal requirement.
- [Microsoft — Integration tests in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/testing/integration-testing): appropriate focused isolation and representative infrastructure testing.
- [Jimmy Bogard — Vertical Slice Architecture (April 19, 2018)](https://www.jimmybogard.com/vertical-slice-architecture/): original request-oriented, change-axis account; useful primary design context, not a source of universal Microsoft obligations.

Microsoft's documented guidance remains authoritative by reference. The **conditional recommendation and precise adopted-style expectation** in this document are the playbook's reviewed engineering decisions, not claims that Microsoft requires one particular feature layout, CQRS, or handler framework.
