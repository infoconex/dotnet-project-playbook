# Modular Monolith Architecture: on-demand .NET guidance

A **modular monolith** packages an application as a unified deployment while organizing meaningful business capabilities behind controlled internal boundaries. The goal is independent understanding and change within one application, **not** mandatory microservices readiness. A module should own meaningful behavior and provide deliberate collaboration contracts; folders or assemblies alone cannot establish that ownership.

This is **illustrative guidance, not another standard, a distributable template, or a verified .NET application**. The authoritative adopted-style obligation is [Recommended STD-015 — Modular Monolith Architecture](standards/modular-monolith.md#std-015). Independently [Required STD-010 — SOLID](standards/solid.md#std-010), [Required STD-011 — Business-policy dependency direction](standards/dependency-direction.md#std-011), [Required STD-001 — TDD](standards/engineering-principles.md#std-001), and [conditional STD-009 — External-boundary verification](standards/testing.md#std-009) retain their scopes. [Hexagonal (STD-012)](standards/hexagonal.md#std-012), [Clean (STD-013)](standards/clean.md#std-013), and [DDD (STD-014)](standards/ddd.md#std-014) remain independently Recommended; [compiled project separation (STD-003)](standards/engineering-principles.md#std-003) remains Optional.

The following levels are optional explanations for a specific design question or repository assessment, **not a mandatory discovery questionnaire, generator, architecture analyzer, or universal implementation checklist**.

## Level 1 — Decide whether modules help

### Begin with business capabilities and change pressure

| Actual project situation | Practical starting point | What would change the decision |
| --- | --- | --- |
| Small pure class library | Cohesive types and tests; no application modules required | Distinct, independently evolving business capabilities appear |
| Straightforward CRUD application | Simple responsibilities with policy independence | Separate business policies, data ownership, or repeated cross-feature change ripple appears |
| Complex domain application | Identify business capabilities, decision ownership, significant data, and collaboration boundaries | If several nominal modules repeatedly share their rules, reconsider module boundaries |
| Enterprise monolith with distinct ownership | Introduce or strengthen modules around stable responsibilities | Separate compiled assemblies may help if source-only boundaries erode |
| Application operated by multiple teams | Clarify who changes each business decision, who approves contracts, and who owns data | Team boundaries alone need not define modules or require separate repositories |
| Existing .NET Framework application | Extract the smallest valuable logical module behind compatible contracts | Use additional projects only when build, visibility, testability, or compatibility needs justify them |
| Possible future independent deployment | Keep clear contracts and data ownership if useful **today** | Independently deployed services require a separate operational justification |

An application can be large yet cohesive enough for straightforward layering. A compact application may have two genuinely independent business capabilities. Use concrete responsibilities, integration needs, test evidence, and change history rather than a fixed file-count or module-count threshold.

**Business-oriented decomposition** commonly uses Orders, Inventory, Billing, or Fulfillment as examples. Each name should correspond to decisions and information it owns. A `DataAccess`, `Utilities`, or `Services` directory normally describes a technical category, not an independent business capability. A module can contain presentation, use-case, policy, and infrastructure responsibilities as appropriate, while still observing independently Required policy independence.

### Separate four different boundaries

| Boundary | Governs | Does not imply |
| --- | --- | --- |
| Business capability/module | Ownership, public collaboration contracts, and allowed dependencies | One bounded context, one team, one assembly, or one database |
| DDD bounded context | Meaning and consistency of a particular domain model | Automatic adoption of DDD everywhere, or a one-to-one physical module |
| Project/assembly | Build-time references and assembly-level visibility | One runtime process or an independently deployable service |
| Deployment | What ships and runs together | One source project or one domain model |

Microsoft describes a monolith as a single-deployment application even when its code uses multiple responsibilities and projects. Its bounded-context guidance discusses separate conceptual models without requiring that every conceptual boundary be deployed remotely. A modular monolith can be the appropriate **long-term** architecture rather than a staging step toward microservices.

### Neighboring styles: independent choices

| Style | Its main question | How it can coexist with modules |
| --- | --- | --- |
| [Proportionate single-project](single-project-guidance.md) | How many production projects are justified? | Many logical modules can live in one assembly, with weaker compiler-enforced privacy |
| [Traditional layered/N-tier](layered-n-tier-guidance.md) | What responsibilities and runtime tiers are separate? | Individual modules may have logical layers; no extra remote tier is implied |
| [Hexagonal](standards/hexagonal.md#std-012) | What are application ports and external adapters? | A module may adopt Hexagonal; every identified inbound and outbound **port** then needs an explicit interface |
| [Clean](standards/clean.md#std-013) | What is the protected Application Core? | A module may adopt its inward core rule without requiring all modules to do so |
| [DDD](standards/ddd.md#std-014) | What models express business meaning and invariants? | Bounded contexts often inform modules, but neither requires the other or a one-to-one mapping |
| [Vertical Slice — STD-016](standards/vertical-slice.md#std-016) | How should feature/use-case changes be organized? | Feature slices can be organized **within** a module; neither style automatically requires the other |
| [Microservices — Issue #27](https://github.com/infoconex/dotnet-project-playbook/issues/27) | Which capabilities need independent service deployment and autonomy? | A separate decision about network contracts, operations, security, and distributed consistency |

Combining styles means adopting **each selected style's** applicable obligations; a similar-looking directory does not automatically adopt it. For example, using `Orders/Domain` and `Orders/Infrastructure` does not by itself establish Clean or Hexagonal Architecture. Nor does preferring in-process calls excuse an actual violation of STD-011.

## Level 2 — C# module boundaries, contracts, and data

### Example A — One production project, meaningful logical modules

Illustrative layout, **not an existing compiled application**:

```text
Shop/
  Shop.csproj                     # One production assembly and one application deployment
  Orders/
    OrderApproval.cs              # Orders-owned business decision
  Inventory/
    InventoryAvailability.cs      # Inventory-owned public read capability
    StockDataAccess.cs            # Inventory implementation; not consumed directly by Orders
  Host/
    Composition.cs                # Connects module capabilities and implementations
Shop.Tests/
  Shop.Tests.csproj
```

This is source organization only. Even if `StockDataAccess` were declared `internal`, it would remain accessible to **all code in the same assembly**, including code placed in `Orders/`. The module privacy rule therefore requires careful source/type usage review or a meaningful focused check, rather than assuming folders or namespaces provide compiler-enforced protection. For stronger assembly enforcement, consider Example B.

An intentional public module-facing capability can be a **concrete facade**. When Modular Monolith Architecture is selected without separately adopting Hexagonal Architecture, STD-015 does not demand an interface for every collaboration. In these **illustrative, uncompiled C# 7.3-compatible excerpts**, Inventory exposes only the operation Orders needs:

```csharp
// Inventory/InventoryAvailability.cs — illustrative, not compiled or executed.
using System;

namespace Shop.Inventory
{
    public sealed class InventoryAvailability
    {
        private readonly Func<string, int> _onHand;

        public InventoryAvailability(Func<string, int> onHand)
        {
            _onHand = onHand ?? throw new ArgumentNullException(nameof(onHand));
        }

        public bool CanFulfill(string sku, int quantity)
        {
            if (string.IsNullOrWhiteSpace(sku))
                throw new ArgumentException("A product identifier is required.", nameof(sku));
            if (quantity <= 0)
                throw new ArgumentOutOfRangeException(nameof(quantity));

            return _onHand(sku) >= quantity;
        }
    }
}
```

Orders consumes the **public Inventory capability**, not Inventory's repository, database client, or persistence representation:

```csharp
// Orders/OrderApproval.cs — illustrative, not compiled or executed.
using System;
using Shop.Inventory;

namespace Shop.Orders
{
    public sealed class OrderApproval
    {
        private readonly InventoryAvailability _inventory;

        public OrderApproval(InventoryAvailability inventory)
        {
            _inventory = inventory ?? throw new ArgumentNullException(nameof(inventory));
        }

        public bool CanApprove(string sku, int quantity, bool paymentAuthorized)
        {
            return paymentAuthorized && _inventory.CanFulfill(sku, quantity);
        }
    }
}
```

The host can supply the technology-neutral `Func<string, int>` capability using an implementation appropriate to its real environment. The facade does not expose a SQL client or require Orders to know how stock was read. A stable, cohesive concrete business collaborator is not automatically a violation of SOLID or policy independence. A dedicated `IInventoryAvailability` interface may become worthwhile if consumers need independent substitution, versioned contracts, or a clearer assembly boundary. **If this interaction is explicitly identified as an inbound or outbound port of an adopted Hexagonal design, STD-012's interface rule applies independently.**

This tiny example illustrates one **read-only availability decision**, not a reservation protocol, durable stock decrement, authorization rule, or concurrency guarantee. A real reservation must be owned and protected by Inventory, and availability alone does not establish that stock cannot change before an order commits. Separate tests and real persistence behavior would be needed for those claims.

### Example B — Multiple compiled projects, one deployment

A possible structure when module-level compilation boundaries add useful enforcement:

```text
Shop/
  Shop.Host/                      # One application host and deployment composition
  Orders.Module/                  # Orders implementation and private behavior
  Inventory.Contracts/            # Public Inventory collaboration types
  Inventory.Module/               # Inventory behavior and persistence implementation
  Shop.Tests/                     # Focused module/interaction tests
```

Orders may reference `Inventory.Contracts` without referencing `Inventory.Module`; the host may reference contracts and both implementations for composition. This arrangement can prevent some direct cross-module implementation imports, but it is **one illustrative shape**, not a standard layout. Other modules might expose their approved public API directly from an implementation assembly. A single `Shop.csproj` can also remain valid.

**Compiler caveat:** Contract-only project dependencies do not prove semantic decoupling. Two modules can reference each other's contract projects without a project graph cycle, while their runtime operations still depend reciprocally or coordinate every change. Verify the **actual implementation dependency and call ownership**, not only the compiler graph.

Physical project boundaries add project files, public API/version maintenance, build references, and possible test-access decisions. Keep [STD-003](standards/engineering-principles.md#std-003) Optional and use the arrangement only when the enforcement benefit outweighs that cost. Neither multiple libraries nor one contracts project per module turns the application into microservices.

### Example C — Shared database, module-owned writes

Suppose Orders and Inventory use the **same SQL database**, possibly even the same database schema:

| Behavior | Boundary interpretation |
| --- | --- |
| Orders requests `Inventory.Reserve(sku, quantity)` through an approved capability | Appropriate if Inventory owns stock invariants and implements the mutation safely |
| Orders uses its own SQL repository to update `Inventory.Stock` directly | Bypasses Inventory ownership; inconsistent with adopted STD-015 |
| A reporting query joins Orders and Inventory tables without modifying them | Potentially acceptable if its security, consistency, schema coupling, and stewardship are explicitly managed |
| Orders and Inventory coordinate a local atomic transaction | Potentially appropriate if the persistence model actually supports it, module-owned operations are preserved, and failure/concurrency semantics are verified |
| Every module gets a separate database and event bus automatically | Unnecessary physical and operational complexity without a demonstrated requirement |

An important distinction is **one logical authority for each business mutation**, not a universal prohibition on a common SQL server, physical schema, selected foreign key, or report query. Cross-module foreign keys can create schema-evolution coupling, so evaluate them deliberately. Shared DTOs or persistence entities should not silently collapse distinct business models or allow arbitrary writes. Ownership belongs to the actual rules and operations, not merely to an EF Core `DbContext` name or a table prefix.

If a business requirement spans modules, decide whether one module should own the full invariant or an application-level coordinator should manage a process across legitimate module-owned operations. Explicitly consider local transaction capabilities, isolation, concurrency, retries, and partial changes. A transaction spanning several modules in one process is **not inherently distributed**; a successful in-memory unit test cannot establish its database behavior.

### Example D — Choose the smallest sufficient communication mechanism

| Mechanism | Useful for | Primary tradeoff |
| --- | --- | --- |
| Direct in-process call to published facade/interface | Immediate result, validation, synchronous work, local transaction participation | Direct business contract coupling; errors/timeouts must be handled at the actual boundary |
| Mediated command/query dispatch | Multiple callers with a real dispatch or cross-cutting policy requirement | More indirection; may hide who owns behavior; no mandatory mediator library |
| Synchronous in-process application event | Several reactions that need explicit synchronous handling | Handler order, exceptions, and transaction membership need definition |
| Post-commit application/integration event | Consumers need to react after a successful state change | Publication ordering, delivery guarantees, duplicates, and restart behavior need definition |
| Durable asynchronous messaging | Actual temporal independence, workload buffering, or separate processing reliability | Broker/queue operations, idempotency, observability, retries, consistency, versioning |

The names **domain event** and **application/integration event** describe different business meanings and boundaries; they do not automatically select an infrastructure mechanism. When a handler is inside a transaction, define failure and rollback semantics; when it runs after commit, define what happens if the handler or publication fails. A fire-and-forget callback does not become a reliable event bus because it runs in process. Avoid building an internal distributed system to connect methods that could call one another directly.

### Example E — Module composition and lifetime ownership

A host may call a small, publicly documented module registration method or manually construct the dependencies of an application. Module initialization can establish registrations and technical integrations without turning each module into an independently hosted process. The host remains accountable for application startup/shutdown and compatible service lifetimes. A module can own an internal scheduler or resource only when its lifecycle is made explicit to the host.

For supported modern .NET hosts, Microsoft's dependency-injection guidelines help with scope and disposal choices. For older .NET Framework projects, a compatible DI library or manual factories may be more appropriate; **do not copy ASP.NET Core registration syntax into an environment without that API**. Keep business policy independent of the concrete composition mechanism under STD-011. Avoid hidden process-global mutable registries or service locators as shortcuts across module boundaries.

## Level 3 — Review, verify, and modernize

### Scenario-based architecture review

| Scenario | Assessment question | Expected interpretation |
| --- | --- | --- |
| Small pure library | Are there actually independent business capabilities and owners? | Often no modular monolith adoption needed |
| Straightforward CRUD app | Would modules protect material business behavior or merely add wrappers? | Simple design may be a documented alternative |
| Large app with `Modules/` folders | Can one module change without calling another's private types or writing its records? | Directory labels alone prove nothing |
| Orders calls Inventory's approved API | Is Inventory's implementation and stock policy still owned by Inventory? | Suitable module collaboration |
| Orders imports Inventory's internal repository | Does the call bypass the approved capability? | Adopted boundary violation even if the solution builds |
| Orders updates Inventory tables | Can Inventory's invariants be bypassed? | Adopted data-ownership violation |
| Shared database, distinct mutation owners | Are direct reads and cross-module queries deliberate and controlled? | Acceptable with documented coupling and safety |
| A and B depend on each other's internals | Is there an implementation cycle or mislocated shared responsibility? | Reassess module decomposition; avoid cyclic coupling |
| A and B reference each other's contracts | Do runtime interactions create semantic cycles or shared ownership? | Compiler graph alone is insufficient evidence |
| One business transaction spans modules | Is local atomicity feasible, do owner-controlled operations preserve invariants, and are failure paths tested? | Allowed with evidence, not presumed correct |
| Event handler runs after commit | What if the handler fails or the host stops? | State delivery, retry, and consistency limits explicitly |
| Significant module startup change | Were registrations and disposal/lifetimes actually exercised? | Verify meaningful composition path |
| Traditional .NET Framework monolith | Can one capability be isolated without breaking current API/build constraints? | Prefer incremental, compatibility-conscious adoption |
| Module claims Hexagonal or Clean | Are all applicable adopted-style port/core expectations satisfied? | Evaluate each style independently |
| Team contemplates extracting a service | Is independent deployment actually needed, and what are the data/transaction costs? | Separate Issue #27 decision; extraction is not the goal |

### Practical evidence strategy

1. **Locate ownership.** Trace a real use case across entry point, public module-facing contract, owner implementation, business invariant, and persistent mutations. Check who must change when business meaning evolves.
2. **Inspect implementation dependencies.** Review actual source usage, injected types, calls and event chains. Where multiple projects exist, inspect `ProjectReference` or traditional assembly references and exported types. In one assembly, inspect imports and call sites; `internal` provides no per-namespace firewall. Avoid declaring modules independent merely because no project-reference cycle exists.
3. **Exercise significant behavior through the boundary.** Test representative successful and rejected operations, owner-controlled state transitions, and caller-visible failures. Use controlled substitutes only at meaningful integration seams; a facade might be testable directly without inventing an interface solely to mock it. Apply STD-001 to new executable behavior.
4. **Check real data and composition behavior as applicable.** Validate material cross-module transaction isolation, concurrency, persistence access, event timing, and DI/manual wiring with representative integration/component tests. Apply STD-009 to materially significant external adapters. Substitute-based tests do not establish SQL rollback, event durability, or host lifetime correctness.
5. **Record the exact limits.** Identify the reviewed commit, paths, available toolchain/target, actual executed checks/results, scenario coverage, alternatives and remaining uncertainty. A diagram, green build, namespace scan, or conceptual code snippet cannot establish all semantic properties. There is **no universal modularity analyzer** or new mandatory CI gate in STD-015.

For **documentation-only playbook changes**, review terminology, source support, examples, hyperlinks, and standards consistency. Do not claim a C# fragment compiles or a target framework supports a package without a real compatible toolchain execution.

### Evolving an existing monolith without a rewrite

1. Start with recurring change pain, a business capability boundary, or a risky direct data mutation, not a desired number of assemblies.
2. Characterize existing business behavior when practical, including persistence-visible effects and public compatibility constraints.
3. Give one affected capability an intentional public module-facing operation. Redirect its significant callers before hiding its private implementation.
4. Move write ownership and invariant enforcement behind the owning module progressively. Preserve valid read/reporting needs, and assess their schema coupling explicitly.
5. Decide whether separate assemblies or focused automated dependency checks are worth introducing **after** the logical boundary has value.
6. Exercise behavior, important transactions, and composition with the actual supported tools; record remaining coupled paths honestly.

Modern SDK-style .NET can use supported `dotnet` tooling and modern hosting facilities where applicable. Traditional non-SDK .NET Framework projects may require Visual Studio/MSBuild and legacy test runners on Windows; use the real compiler and language level (for example C# 7.3) rather than assuming all current framework APIs or C# syntax exist. A working source example in one target does not prove another target's compilation, runtime, or operating-system compatibility.

You may deliberately stop at a well-structured modular monolith. Independent deployment, network contracts, service autonomy, distributed consistency, and scaling characteristics belong to a separate microservices evaluation and are **not** eventual acceptance criteria for modularity.

## Primary references and guidance boundary

- [Microsoft .NET architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles) — encapsulation, separation, abstraction, and bounded contexts.
- [Microsoft common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) — one- versus multiple-project monoliths and dependency patterns.
- [Microsoft domain analysis](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis) and [data sovereignty discussion](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/architect-microservice-container-applications/data-sovereignty-per-microservice) — model, data, and ownership considerations; database isolation rules specific to distributed microservices are **not adopted unchanged**.
- [Microsoft C# `internal`](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/internal) — assembly, not folder, accessibility.
- [Microsoft domain events guidance](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation) and [DI guidance](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines) — consistency, composition, and lifecycle tradeoffs.
- [Microsoft incremental modernization pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig) — phased risk reduction without requiring service extraction.
- [Kamil Grzybek's original modular-monolith implementation](https://github.com/kgrzybek/modular-monolith-with-ddd) — a stricter, valid illustrative design using events and schema boundaries, **not a set of mandatory .NET conventions**.
- [Martin Fowler's Monolith First](https://martinfowler.com/bliki/MonolithFirst.html) — first-party analysis and caveats on decomposing monoliths into separate services.
- [Jimmy Bogard's Vertical Slice Architecture](https://www.jimmybogard.com/vertical-slice-architecture/) — first-party feature/use-case organization distinction; [STD-016](standards/vertical-slice.md#std-016) separately owns adopted feature-level cohesion, not module ownership.

These are documented design principles and examples, not experimental verification of this guide's snippets. [STD-015](standards/modular-monolith.md#std-015) remains the sole authority for the adopted module-level obligation.
