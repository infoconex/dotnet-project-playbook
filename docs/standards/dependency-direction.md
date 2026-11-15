# STD-011 — Business-policy dependency direction

The playbook follows Microsoft's published .NET architectural guidance by default. This standard makes the existing [Required engineering principle](engineering-principles.md) independently assessable: **business policy must remain independent of concrete infrastructure and presentation mechanisms**. Its scope is based on *responsibility*, not on a prescribed assembly or architectural pattern.

The [standards catalog](README.md) indexes this permanent ID. [Practical dependency-direction guidance](../dependency-direction-guidance.md) illustrates the standard without creating additional requirements. [Standards governance](../governance/standards.md) defines Required obligations and exceptions.

## <a name="std-011"></a>Purpose and applicability

**Level: Required.** Apply this expectation when creating or materially changing business-policy code in a .NET class library, application, service, command-line tool, or other project using the playbook. Domain policy and business decisions performed by application use cases are in scope wherever they reside, even when mixed with infrastructure in a single compiled assembly. The absence of an external dependency does not require introducing an artificial port.

The principle applies to modern .NET and .NET Framework projects, including existing systems being changed incrementally. It does **not** require Clean Architecture, Hexagonal Architecture, Domain-Driven Design, a particular folder or namespace scheme, a dependency-injection container, or separate projects. [STD-003](engineering-principles.md#std-003) continues to make separate compiled projects **Optional**; [STD-010](solid.md#std-010) governs object-level SOLID design.

## Normative expectation

Business-policy code must not **depend on concrete infrastructure or presentation mechanisms to express or decide business rules**. In particular:

1. **Keep policy independent.** Domain rules, invariants, and application-level business decisions must not require concrete database clients, file/network transports, persistence models tied to a provider, UI controls, controllers, or hosting APIs to evaluate or enforce those decisions. Stable language/runtime primitives and appropriately abstract, technology-neutral collaborators are not prohibited.
2. **Direct source dependencies deliberately.** When a business decision needs a result or capability supplied by an external mechanism, use a suitable contract defined with the consuming policy or in another appropriately inward, technology-neutral location. An outer adapter can implement that contract. A policy must not instantiate, select, or configure a particular replaceable technical implementation to make its decision.
3. **Separate policy from technical orchestration.** Code that merely coordinates technical work without making or encoding business decisions may depend directly on infrastructure, including in an application-level component. A type or method is not exempt merely because it is called a command handler, application service, adapter, or coordinator: inspect the actual decisions it contains. If orchestration starts making business decisions, isolate that policy from the concrete mechanism.
4. **Permit composition to know implementations.** A composition root or other outer application assembly may reference both contracts/policy and concrete adapters to construct and connect them. At runtime, policy can call a contract whose implementation executes infrastructure code; this does not create a forbidden compile-time dependency from policy to the implementation.
5. **Use boundaries proportionately.** Preserve logical responsibilities even inside one project. Introduce interfaces, ports, wrappers, assemblies, or framework-specific dependency injection only where actual responsibilities, replaceability, tests, or enforcement justify them. A direct dependency on a stable concrete collaborator with no policy-to-infrastructure coupling is not automatically a violation.

These are **policy-independence obligations**, not rules forbidding all outward calls, enforcing a universal inward layer graph, or requiring that every application component be infrastructure-free.

## Responsibility and dependency interpretation

The names below identify *logical roles*; a project need not contain all five, use these names, or compile each into a separate assembly.

| Logical role | Boundary interpretation |
| --- | --- |
| **Domain policy** | Owns relevant business concepts, invariants, and decisions; does not require a concrete UI, database, transport, or host to exercise its rules. |
| **Application policy** | Coordinates or makes business decisions across domain operations. The portions containing policy observe the same independence rule, even if the containing application assembly also includes technical orchestration. |
| **Infrastructure adapter** | Implements concrete persistence, messaging, file, or external-service access; may depend on technology-neutral contracts and domain models needed to fulfill them. |
| **Presentation/transport** | Translates user or protocol requests to application operations and formats results. Business policy should not depend on its controllers, view types, or transport-specific models. |
| **Composition root** | Selects and wires concrete implementations at an outer boundary; may legitimately reference policy contracts and infrastructure together. |

**Allowed example:** A policy depends on `IOutstandingInvoiceCount`; a SQL adapter implements it; a host constructs the adapter and passes it to the policy. **Disallowed example:** The policy directly constructs a `SqlConnection` to determine whether a customer qualifies. **Context-sensitive example:** A CSV-export coordinator with no business rules writes to a file directly; the mere lack of an interface is not a violation. See the [C# and project-reference examples](../dependency-direction-guidance.md#level-2-c-and-project-reference-examples).

**Compile-time versus runtime:** Source and project references establish what a component must know to compile; runtime control flow establishes what executes. At runtime a policy call may reach a database-backed adapter through a contract even though the policy's compile-time reference remains toward that contract. The host/composition root may depend on both. A physical project reference can prevent some forbidden source dependencies; a namespace name or passing build alone cannot prove that policy has been isolated.

## Applying the standard proportionately

- **Small pure library:** Keep business rules independent of any concrete technical mechanism they do not need. No artificial infrastructure project, adapter, DI framework, or interface is demanded.
- **Application or service:** Identify business decisions before deciding which code needs contracts. Keep thin technical coordination flexible while preventing domain or application business rules from becoming bound to persistence, presentation, or hosting details.
- **Traditional .NET Framework and modern .NET:** Use the project's actual compiler, C# language version, target framework, and project format. Neither SDK-style projects nor built-in dependency injection are prerequisites. This guidance does not imply that a .NET Framework runtime supports modern-only APIs or syntax.
- **Existing code:** Assess the affected rule and boundary. Prefer focused, behavior-preserving separation supported by relevant tests over sweeping project or public-API changes. Unchanged legacy code is not automatically assessed as if it were newly written.

The [SOLID standard](solid.md#std-010) covers Dependency Inversion as one of five object-design principles; this standard owns the **distinct Required policy-versus-technical boundary**. The [testing standard](testing.md#std-009) adds conditional representative real-boundary evidence for materially significant adapter behavior; it does not mandate an adapter for every policy. The [engineering-principles baseline](engineering-principles.md) remains the source for other existing obligation levels.

## Verification and limits

For a material change, use evidence proportionate to the project and risk:

1. **Identify the policy.** Name which decisions, invariants, and use cases constitute business policy, including policy inside otherwise technical-looking application code. Record relevant concrete dependencies and justify any direct references.
2. **Check objective boundaries where valuable.** Inspect assembly/project references, dependency graphs, and source imports or namespaces. Where project boundaries exist and a local check is practical, use the project's existing build/inspection mechanisms to detect a concrete forbidden dependency; record the actual command, target, and result. There is no universal required analyzer, project graph, or new CI gate.
3. **Review semantic boundaries.** Inspect relevant implementations, data types, call sites, and tests to determine whether business decisions depend on a technology detail, whether an apparent port is meaningful, and whether technical orchestration conceals business policy. These judgments are not established by a project-reference check.
4. **Record actual evidence and limitations.** Identify the revision, files, checks, findings, exceptions, and any unverified paths. A successful build, a clean namespace scan, or a passing architecture test is not proof of policy independence. Do not represent documentation review as executable verification.

Applicable functional and adapter tests remain governed by [STD-001](engineering-principles.md#std-001) and [STD-009](testing.md#std-009), respectively. The [practical guide](../dependency-direction-guidance.md#level-3-review-and-verification) contains illustrative review questions and inspection examples, not an additional verification mandate.

## Exceptions and alternatives

A genuine departure from business-policy independence requires a **justified, explicitly reviewed and recorded exception** under [standards governance](../governance/standards.md#applicability-levels). State the affected rule or dependency, the concrete constraint (such as a fixed third-party surface, a published compatibility contract, or legacy coupling), the viable alternatives, the least-disruptive mitigation, observed verification, residual risk, and follow-up when appropriate. Neither convenience nor the mere existence of old coupling automatically justifies new policy-to-infrastructure dependencies.

Using a concrete type for **non-policy orchestration**, keeping a small library in one assembly, or declining a speculative interface is **not an exception**, because the normative rule does not prohibit those designs.

## Authoritative Microsoft references

- [.NET architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles) — separation of concerns, abstraction, and dependency inversion.
- [Common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) — Clean Architecture compile-time dependencies, runtime composition, and project organization.
- [Designing a DDD-oriented microservice](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice) — domain-model independence and layered responsibilities.
- [Implementing the microservice application layer using Web API](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-application-layer-implementation-web-api) — command-handler and infrastructure coordination in a real application layer.

These sources provide the general Microsoft architectural guidance. The specific **Required responsibility-based independence**, its proportional application, and the reviewable-exception rule are the playbook's approved standard; illustrative code cannot override that requirement.
