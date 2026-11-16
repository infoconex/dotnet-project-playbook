# Traditional layered and N-tier architecture: on-demand .NET guidance

Logical layering can make responsibilities easier to understand and change. Physical N-tier deployment can address different scaling, availability, or security needs. **Neither is an automatic consequence of creating several C# projects**, and neither permits business policies to depend on concrete presentation or infrastructure mechanisms.

This is **illustrative guidance, not a new normative standard, executable template, or verified application**. The authoritative obligations remain [Required STD-010 — SOLID](standards/solid.md#std-010), [Required STD-011 — Business-policy dependency direction](standards/dependency-direction.md#std-011), [Optional STD-003 — Separate compiled projects](standards/engineering-principles.md#std-003), [STD-001 — TDD](standards/engineering-principles.md#std-001), and [conditional STD-009 — External-boundary verification](standards/testing.md#std-009). [STD-012 — Hexagonal](standards/hexagonal.md#std-012), [STD-013 — Clean](standards/clean.md#std-013), and [STD-014 — DDD](standards/ddd.md#std-014) remain independently Recommended choices with their own obligations **if adopted**. Issue #24 introduced no layered/N-tier-specific standard because Microsoft's guidance and existing standards cover those independently assessable expectations. Separately, [STD-015 — Modular Monolith Architecture](standards/modular-monolith.md#std-015) conditionally governs adopted **business-capability module** boundaries, and [STD-016 — Vertical Slice Architecture](standards/vertical-slice.md#std-016) conditionally governs **feature/use-case cohesion**; neither dictates technical layers, physical tiers, or compiled-project count.

The levels below offer explanations on demand, not a mandatory architecture questionnaire or automated assessment. Start with the project's actual responsibilities and constraints; do not adopt layers simply because a framework sample uses them.

## Level 1 — Understand the choice

### Logical responsibilities, not a mandatory stack

| Logical responsibility | Typical work | Important boundary |
| --- | --- | --- |
| Presentation / transport | Translate HTTP, UI, CLI, or other actor requests and format responses | Avoid placing business decisions in controllers, views, or protocol models |
| Application / use-case coordination | Coordinate workflows, invoke domain behavior, handle application-level decisions and appropriate transaction orchestration | Any *business-policy* decisions must obey STD-011, even inside a technical-looking handler |
| Domain / business policy | Express business concepts, rules, invariants, and state transitions | Evaluate policy without concrete persistence, UI, transport, or host mechanisms |
| Data access / infrastructure | Implement storage, messaging, network, file, external-service, and provider-specific behavior | Contain vendor APIs, persistence models, and technical translation |
| Contracts / abstractions | Express capabilities needed by a policy or other consumer, in a suitable inward-owned contract | Avoid a universal shared project or abstractions that leak provider details |
| Composition root | Select, configure, construct, and connect implementations in an outer host | Composition may know both inward contracts and concrete adapters without creating a forbidden policy dependency |

A project may omit a role that has no work, combine cohesive roles in a class or assembly, or use different names. A pure library need not invent Presentation or Application layers. An application service may contain business policy or only technical orchestration; its name does not decide which dependencies it may use. [Microsoft's application-layer guidance](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-application-layer-implementation-web-api) illustrates technical coordination with infrastructure, while STD-011 independently protects any business decisions within it.

### Layers, compiled projects, deployments, and tiers are different

| Term | What it means | What it does not establish |
| --- | --- | --- |
| Logical layer | A responsibility and its permitted collaborators | A required folder, namespace, assembly, or server |
| Namespace or folder | Source organization | Compiler-enforced dependency isolation |
| Compiled project / assembly | A build/reference boundary, possibly used to enforce source dependencies | A distinct runtime service, application tier, or independently deployable feature |
| Application deployment unit | Artifacts deployed and released together | One assembly, one logical layer, or necessarily one physical machine |
| Physical deployment tier | A distinct runtime placement/boundary, such as separately hosted web, application, or database infrastructure | A one-to-one mapping to source layers, compiled projects, or business capabilities |

For example, `OrderApi`, `OrderApplication`, and `OrderInfrastructure` may be three compiled projects but one deployed web application. Conversely, one web application containing multiple logical layers can access a separately hosted database tier. Several instances of the same web tier for scale-out do not, by themselves, create new kinds of architectural tiers. [Microsoft's common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) and [Azure N-tier guidance](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/n-tier) make the logical/physical distinction explicitly.

### Preserve policy independence before choosing a layering style

Traditional downward compile-time coupling, such as `UI -> BusinessLogic -> ConcreteSqlDataAccess`, can make the business-logic layer depend on a specific database implementation. A replaceable DAL class does not solve this if the policy must compile against concrete DAL types or provider-specific data contracts.

When **business policy** needs an external capability, define an appropriately technology-neutral, consumer-oriented contract with that policy or a suitable inward boundary. A concrete adapter implements it; the host composes them. A runtime call may reach SQL even though the policy's **source dependency** does not point to SQL. The Required rule belongs to [STD-011](standards/dependency-direction.md#std-011), not to a newly invented layered-architecture obligation.

This does not ban all outward source dependencies: a coordinator that only performs technical work may call infrastructure directly, and an outer composition root may reference contracts and implementations. If Clean Architecture is also adopted, its *entire designated Application Core* has stronger inward dependency conditions under STD-013. If Hexagonal is adopted, its identified inbound and outbound ports require explicit interfaces under STD-012. A layered application does not automatically claim either style.

## Level 2 — Compare practical shapes and tradeoffs

### Example A — Layered behavior without infrastructure-coupled policy

Suppose a use case must decide whether to approve an order based on the customer's unpaid invoice count. The snippets below are **C# 7.3-compatible illustrative excerpts**, not a compiled solution, tested database adapter, or prescribed class-per-layer arrangement. An actual project would normally place primary types in their own files and use its supported toolchain.

**Business policy: independent decision over business facts**

```csharp
public sealed class OrderApprovalPolicy
{
    public bool CanApprove(int unpaidInvoiceCount)
    {
        return unpaidInvoiceCount < 3;
    }
}
```

**Application capability contract and coordinating use case:**

```csharp
using System;

public interface IUnpaidInvoiceCount
{
    int ForCustomer(Guid customerId);
}

public sealed class CheckOrderApproval
{
    private readonly IUnpaidInvoiceCount _invoiceCount;
    private readonly OrderApprovalPolicy _policy;

    public CheckOrderApproval(
        IUnpaidInvoiceCount invoiceCount,
        OrderApprovalPolicy policy)
    {
        _invoiceCount = invoiceCount ?? throw new ArgumentNullException(nameof(invoiceCount));
        _policy = policy ?? throw new ArgumentNullException(nameof(policy));
    }

    public bool IsAllowed(Guid customerId)
    {
        return _policy.CanApprove(_invoiceCount.ForCustomer(customerId));
    }
}
```

A concrete SQL adapter can implement `IUnpaidInvoiceCount`, translating database results into the business-relevant count; a presentation entry point can call `CheckOrderApproval`. The outer host can construct the SQL adapter and use case manually or with an appropriate supported DI container. Neither the rule nor use case needs SQL client, controller, or database-specific model types. A real SQL integration must be verified separately when [STD-009](standards/testing.md#std-009) applies.

For a project choosing separate compiled boundaries, one possible graph is:

| Project / role | Example source references |
| --- | --- |
| `OrderDomain` | No reference to application host or SQL infrastructure |
| `OrderApplication` | `OrderDomain` and its own `IUnpaidInvoiceCount` contract |
| `OrderInfrastructure` | `OrderApplication` to implement its contract; SQL/provider dependencies |
| `OrderHost` | `OrderApplication` and `OrderInfrastructure` to compose the application |

These are **optional assemblies** under STD-003. The exact same roles could live in one production project, with source-level discipline and semantic review instead of compiler-enforced project references. The graph resembles one Clean Architecture arrangement, but resemblance alone does **not** declare that STD-013 or STD-012 was adopted. Where those styles *are* adopted, assess all their independent requirements.

**Counterexample:** If `OrderApprovalPolicy` constructs a SQL connection, queries unpaid invoices, and then decides approval, the business decision depends on a concrete infrastructure mechanism. Calling that class a business layer does not make it STD-011-compliant.

**Different legitimate case:** A CSV-export coordinator with no business rules can write through a stable concrete file API directly. Introducing an artificial repository, port, or DAL solely to preserve a three-layer diagram may add no value. Always inspect what the coordinator actually decides.

### Example B — Strict versus relaxed logical layering

| Choice | Useful when | Costs and risks |
| --- | --- | --- |
| Strict / closed | Adjacent boundaries enforce real policy, security, validation, or change isolation | Pass-through code, excess dependencies, and—when tiers are remote—extra hops and latency |
| Relaxed / open | A direct call safely avoids meaningless intermediaries and respects actual ownership | Extra coupling, opportunities to bypass authorization or invariant enforcement |
| Selective | Some boundaries are meaningful and others merely forward requests | Requires review of each permitted bypass and its consequence |

Do not use a blanket rule that presentation must always call every intermediate layer. Nor should presentation bypass an application authorization or domain-invariant boundary merely because a direct data path is faster. A read-oriented shortcut may be appropriate when its access control, data ownership, policy semantics, and consistency are deliberately addressed. Microsoft's [N-tier guidance](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/n-tier) distinguishes closed/open layers and strict/relaxed tier communication. The *source dependency graph* and the *network request path* should be reviewed separately.

### Example C — A physically distributed N-tier system

A web frontend, a separately hosted application service, and a remote database can be separate tiers. The exact topology, tier count, and grouping of logical responsibilities depend on the deployment; one tier may host several logical layers. A database hosted remotely from an otherwise single-deployment web application is already a physical boundary, but does not require a separate application-service tier.

Before adding an application tier, identify the specific requirement: distinct resource scaling, security isolation, reliability boundary, deployment constraint, regional/hybrid placement, or operational ownership. Compare a single application deployment (possibly with a separate database) against distributed application tiers.

| Concern | Single application deployment | Separately hosted application tier |
| --- | --- | --- |
| Communication | Mostly in-process application calls, though storage can still be remote | Additional network contracts, serialization, latency, timeouts, and partial failures |
| Scaling | Scale the application unit together; often sufficient | Potentially scale web and application workloads differently, if design actually permits it |
| Security | Fewer application trust boundaries; still secure database and external connections | Service identity, authentication/authorization at boundaries, encryption, network restrictions, secrets, and audit responsibility |
| Reliability | Fewer intermediate application dependencies; shared failures remain possible | Fault isolation opportunities alongside new failure modes, recovery and retry/idempotency considerations |
| Operations | Simpler deployment, diagnostics, and version coordination | More environments, deployments, compatibility coordination, distributed tracing/monitoring, and operational costs |

Use well-defined contracts at genuine network boundaries and verify failure behavior, access controls, and compatibility relevant to the system. Not every application needs messaging, circuit breakers, independent deployment, or distributed transactions. Network-tier separation does not guarantee independent feature releases: tightly coupled tiers may still need coordinated deployments. Nor does a traditional N-tier design automatically become microservices, whose [Microsoft definition](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices) includes autonomous business-capability services with independent deployment. [STD-017](standards/microservices.md#std-017) separately governs that conditional service-level choice, with [practical guidance](microservices-guidance.md). Avoid adding a middle tier that only forwards CRUD requests without delivering architectural value.

## Level 3 — Apply, review, and modernize proportionately

### Choose from the problem, not an architecture label

| Context | Practical starting choice | Reconsider when |
| --- | --- | --- |
| Small pure class library | Cohesive domain or utility types, independently tested; no presentation or network tier | Real technical collaborators, reuse, or enforcement boundaries emerge |
| Straightforward CRUD app | Simple use-case/transaction coordination and presentation, keeping any actual business decisions independent of persistence | Rules, external systems, or change coupling become material |
| Complex business application | Identify distinct policies, use cases, and adapters; apply relevant architecture styles by their own triggers | Source dependencies undermine testing, evolution, or integrity |
| Modular monolith | Organize meaningful business-capability modules under [STD-015](standards/modular-monolith.md#std-015), with appropriate responsibilities *within* each module | Global cross-module DALs or shared models create coupling; consider stronger module enforcement |
| Vertical slices | Group meaningful feature/use-case changes under [STD-016](standards/vertical-slice.md#std-016) while retaining legitimate shared domain and infrastructure responsibilities | Feature folders alone do not establish cohesion or override STD-011; see the [Vertical Slice guide](vertical-slice-guidance.md) |
| Modern SDK-style .NET | Use the project's actual SDK, C# version, DI facilities when helpful, and project-reference checks where valuable | Runtime and deployment requirements justify stronger physical boundaries |
| Traditional .NET Framework | Preserve old `.csproj`, language constraints, API contracts, and supported Windows/MSBuild/test tooling; isolate affected policy incrementally | Focused extraction gives demonstrable testing, compatibility, or ownership benefit |
| Distributed N-tier | Document actual runtime topology and network contracts; test relevant failures and trust boundaries | Operational costs outweigh the intended scalability, isolation, or migration benefit |

**Incremental modernization:** Characterize affected legacy behavior when practical. Locate the business decision in an ASP.NET/Web Forms/MVC controller, service, DAL, or stored-procedure call path. Extract the smallest meaningful policy operation away from concrete UI/database mechanisms while preserving published contracts; then decide whether a new project reference, adapter, or tier provides measurable value. Do not rewrite a .NET Framework application into multiple layers or SDK projects merely to conform to a diagram. C# syntax compatibility by itself does not establish target framework, package, compiler, operating-system, or runtime compatibility; use the actual toolchain. See the [single-project guide](single-project-guidance.md) for one-project versus multi-project decisions.

### Review actual evidence and its limits

For a meaningful new or changed boundary, use the smallest suitable evidence:

1. **Identify policy and responsibilities.** Trace business rules, use cases, request translation, concrete adapters, contracts, and composition. Do not infer role or compliance from a filename, namespace, folder, or layer label.
2. **Inspect source/reference direction.** Review actual type uses and `ProjectReference`/traditional assembly references when present. A project graph can flag objective forbidden edges but cannot prove the policy is in the right place. Single-project designs need source-level and semantic review.
3. **Exercise meaningful policy independently.** Test decisions, permitted and rejected outcomes, and relevant failure behavior without requiring a real UI, SQL server, or unrelated adapter. Follow [STD-001](standards/engineering-principles.md#std-001) for new executable behavior; no mandatory test for a trivial pass-through.
4. **Check significant adapter and composition behavior.** Apply [STD-009](standards/testing.md#std-009) to materially significant external-adapter changes; where significant host registration or composition changes, verify the relevant wiring/lifetime path. Fakes alone do not establish provider behavior.
5. **If tiers are remote, verify the real contract risks.** Choose representative tests for service authentication/authorization, serialization/contract compatibility, timeout, transient failure and recovery, data access restrictions, and operational visibility according to the actual topology and threat model. State which environments and conditions were exercised.
6. **Record revision, results, and gaps.** Distinguish documented Microsoft behavior, reviewed design, actually executed tests, and unresolved judgments. A build, namespace scan, diagram, or documentation review alone cannot prove production security, performance, tier resilience, or architecture quality.

No universal analyzer, extra assembly, CI gate, per-layer test suite, deployment topology, or new standard is introduced. For documentation-only playbook changes, review claims, links, examples, and consistency; do **not** claim that illustrated C# or network scenarios compiled, ran, or passed tests.

## Microsoft guidance and neighboring playbook material

- [Common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) — traditional N-layer coupling, Clean Architecture's inversion, and single-deployment layering.
- [Architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles) — separation of concerns, abstraction, and Dependency Inversion.
- [Azure N-tier architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/n-tier) — physical tiers, closed/open layers, strict/relaxed communication, migration, benefits, and costs.
- [Application layer implementation using Web API](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-application-layer-implementation-web-api) — technical coordination that can use infrastructure without making domain rules.
- [Azure microservices architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices) — when independent services are a *different* deployment/ownership choice.
- [Business-policy dependency direction guide](dependency-direction-guidance.md), [Clean Architecture guide](clean-guidance.md), [Hexagonal guide](hexagonal-guidance.md), [DDD guide](ddd-guidance.md), [Vertical Slice guide](vertical-slice-guidance.md), and [single-project guide](single-project-guidance.md) — optional deeper explanations without redefining their standards.

Microsoft's sources are **documented architectural guidance**, not proof that a particular .NET or .NET Framework repository has implemented it. Requirements and exceptions continue to be governed by the linked [standards catalog](standards/README.md) and [standards governance](governance/standards.md).
