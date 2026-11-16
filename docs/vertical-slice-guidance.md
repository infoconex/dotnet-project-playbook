# Vertical Slice Architecture: on-demand .NET guidance

Vertical Slice Architecture organizes meaningful application behavior around **features and use cases** so that changing a capability usually involves a cohesive area of code. It emphasizes locality of change and low *unnecessary* coupling between features. It does not eliminate legitimate shared domain policy, architectural boundaries, or infrastructure integrations.

This document is **illustrative guidance, not a separate standard, executable template, installed feature generator, or verified application**. The authoritative adopted-style decision is [conditional Recommended STD-016](standards/vertical-slice.md#std-016). Independently Required [SOLID (STD-010)](standards/solid.md#std-010), [business-policy dependency direction (STD-011)](standards/dependency-direction.md#std-011), [TDD (STD-001)](standards/engineering-principles.md#std-001), and [conditional real-boundary verification (STD-009)](standards/testing.md#std-009) retain their own scopes. [Hexagonal (STD-012)](standards/hexagonal.md#std-012), [Clean (STD-013)](standards/clean.md#std-013), [DDD (STD-014)](standards/ddd.md#std-014), and [Modular Monolith (STD-015)](standards/modular-monolith.md#std-015) remain independently Recommended choices. Separate compiled projects remain [Optional (STD-003)](standards/engineering-principles.md#std-003).

These three levels answer increasingly detailed questions on demand. They are **not** a mandatory discovery questionnaire, automatic compliance checker, or prescribed layout.

## Level 1 — Decide whether slices improve the work

### Think in changes and use cases

A slice groups the application work required to fulfill a meaningful request, operation, or workflow. It might include entry-point translation, application orchestration, feature-specific validation, output mapping, and appropriate calls into domain policy and infrastructure contracts. It need not own a private copy of every technical mechanism it uses.

| Unit | Meaning | Common mistake |
| --- | --- | --- |
| Business capability or module | Broad responsibility such as Orders or Inventory, possibly containing many features | Assuming each feature is independently deployed or owns a complete bounded context |
| Feature | Cohesive behavior such as Order Cancellation or Stock Reservation | Creating an enormous `OrdersService` for unrelated operations |
| Use case or request | Specific meaningful operation, such as Cancel Order | Requiring one handler/interface/DTO/project for every method, even if trivial |
| Command or query | Operation intended to change state or retrieve information | Equating a name or HTTP verb with complete CQRS adoption |
| Shared domain policy | Business meaning or invariant used in several operations | Duplicating critical policy per handler to keep every file isolated |
| Infrastructure adapter | Concrete database, HTTP, file, or messaging integration | Copying persistence code into feature folders or importing concrete provider details into policy |

**Granularity heuristic:** If two operations routinely change together for one business reason, grouping can be cohesive. If a feature requires unrelated edits or many different consumers, divide it. If single-operation directories create mostly forwarding code and repeated contract translation, a larger feature grouping may be clearer. Use actual change pressure, not a fixed number of classes.

### Decide from context

| Context | Reasonable starting point | When to reconsider |
| --- | --- | --- |
| Small pure class library | Cohesive public types and tests; no fake request pipeline | Independently evolving business use cases emerge |
| Simple CRUD | Direct application methods or feature grouping as needed | Shared service classes become hard to navigate or tightly coupled |
| Business-logic-heavy API | Use-case-oriented responsibilities with explicit policy ownership | Feature boundaries cannot protect important shared invariants |
| Multiple feature teams | Discoverable feature contracts and selective compiler enforcement | Changes repeatedly cross unrelated feature internals |
| Modular monolith | Business-capability modules containing one or more slices | Slices accidentally bypass module-owned operations or data |
| Existing layered/.NET Framework application | Extract one meaningful changed use case with behavior-preserving tests | A broad refactor would break supported toolchains, public contracts, or deployment assumptions |

Using command and query classes does not by itself mean a system adopted Vertical Slice Architecture. Likewise, replacing `Controllers/Services/Repositories` folders with `Features/` without improving ownership or reducing change coupling is only a file move.

### Neighboring architecture choices remain independent

| Choice | Question answered | Independent constraint |
| --- | --- | --- |
| Single production project | How many assemblies are compiled? | One project can contain many logical slices; [single-project guide](single-project-guidance.md) |
| Traditional layers / physical N-tier | Where are technical responsibilities and runtime tiers? | Feature organization does not permit infrastructure-coupled policy; [layered guide](layered-n-tier-guidance.md) |
| Hexagonal | Which actors and external capabilities interact through ports? | If adopted, every identified inbound/outbound port has the explicit interface required by STD-012 |
| Clean | Which code constitutes the protected Application Core? | If adopted, all designated core code remains independent of concrete infrastructure/presentation |
| DDD | Who owns domain meaning and invariants? | A feature can orchestrate domain behavior without becoming an aggregate or bounded context |
| Modular monolith | Which business capabilities own behavior and data within one deployment? | A module can contain multiple slices; no automatic one-to-one mapping |
| Microservices | Which services deploy and operate independently? | Separate deployment decision under [STD-017](standards/microservices.md#std-017), with [on-demand guidance](microservices-guidance.md) |

For example, `Orders/Features/CancelOrder` can be a slice inside an `Orders` module. An `Inventory` module still owns stock reservations and their consistency rules. `CancelOrder` should request an approved Inventory capability rather than directly update Inventory's tables. This example has one deployment and says nothing about microservices, CQRS, or required project count.

## Level 2 — Organize behavior without unnecessary machinery

### Example A — One project, several cohesive operations

The following is **one optional directory layout**, not a prescribed template:

```text
Shop/
  Features/
    Orders/
      CreateOrder.cs
      CancelOrder.cs
      GetOrderDetails.cs
    Inventory/
      ReserveStock.cs
  Domain/
    Order.cs
    OrderCancellationPolicy.cs
    InventoryReservationPolicy.cs
  Infrastructure/
    SqlOrderStore.cs
  Program.cs
Shop.Tests/
  Orders/
    CancelOrderTests.cs
    CreateOrderTests.cs
```

All production code may reside in one compiled project. The domain policies are shown separately because multiple operations may need them; unrelated policy could instead be near its sole feature. The SQL implementation remains technical infrastructure. `Program.cs` represents an outer composition entry point **only where an application host actually has one**; a pure library need not invent it. Feature tests focus on observable operations, not a mandatory one-test-class-per-source-class convention.

Namespaces and folders do not enforce references inside an assembly: `internal` in C# means accessible within the **assembly**, including other feature folders. Stronger compiler boundaries might warrant multiple projects, but project count remains Optional under STD-003. Test features through meaningful public behavior where possible; do not make every implementation type public or add `InternalsVisibleTo` automatically just for test convenience. If type visibility is part of the public API, consider compatibility and intended consumers before moving or exposing types.

### Example B — A cohesive application service without a handler framework

An operation can be an ordinary method on a cohesive feature-specific application service. The following **partial C# 7.3-compatible excerpt is illustrative, not a compiled sample**; supporting domain and contract types are intentionally omitted.

```csharp
public sealed class OrderCancellationService
{
    private readonly IOrderAccess orders;
    private readonly OrderCancellationPolicy policy;

    public OrderCancellationService(IOrderAccess orders,
        OrderCancellationPolicy policy)
    {
        this.orders = orders;
        this.policy = policy;
    }

    public CancellationResult Cancel(Guid orderId)
    {
        Order order = orders.Find(orderId);
        CancellationResult result = order.TryCancel(policy);
        if (result.Allowed)
        {
            orders.Save(order);
        }

        return result;
    }
}
```

`IOrderAccess` expresses the use case's required persistence capability in technology-neutral terms; a concrete SQL implementation would sit outside protected business policy. The domain operation `Order.TryCancel` evaluates the authoritative `OrderCancellationPolicy` and protects the mutation, while the application service coordinates the use case. Other mutation paths must likewise preserve the invariant. The actual transaction, concurrent updates, and successful persistence would still need implementation and verification. A real production implementation must also define missing/not-found behavior and authorization at the appropriate boundary.

This example does **not** establish that an interface is required for every use case. If Hexagonal Architecture is adopted and this operation is an identified inbound port, [STD-012](standards/hexagonal.md#std-012) independently requires an explicit interface for it. If Clean Architecture is adopted, its complete Application Core remains infrastructure-independent under [STD-013](standards/clean.md#std-013).

Possible alternative implementations:

| Mechanism | Useful when | Cost or caution |
| --- | --- | --- |
| Direct method or static pure operation | Small, stable behavior with no extra dispatch needs | Keep business policy independently testable and avoid hidden global state |
| Cohesive feature-specific service | Related operations share meaningful state, policy, or orchestration | Avoid a broad service accumulating unrelated features |
| One request handler | Operation complexity benefits from narrow request ownership | Extra classes and mapping may add noise for trivial calls |
| Framework endpoint handler | Web host conventions provide useful request integration | Do not hide domain policy in transport-specific code |
| Mediated dispatch | Many operations need consistent dispatch or a justified interception mechanism | Indirection, registrations, debugging cost, and vendor coupling |

Neither MediatR nor another library is mandated. Choose the simplest mechanism satisfying the actual feature's responsibilities and any separately adopted Hexagonal/Clean obligations.

### Example C — Local duplication versus shared authoritative policy

Two independent features may each format a date or map a similar response field. Unifying those snippets can create more coupling than it removes.

By contrast, imagine `RefundOrder` and `CancelOrder` each independently calculate a legally or financially consequential maximum refund. If both implement the **same authoritative business rule**, separate calculations can drift when that rule changes. Prefer one domain policy with well-defined inputs and appropriate ownership, or an approved owner operation, rather than two incompatible copies.

The same distinction applies to stock availability versus actual reservation. An independently calculated availability display is not a reservation guarantee. Inventory's authoritative reservation operation must enforce concurrency and consistency in its actual persistence transaction. A passing in-memory feature test cannot prove those guarantees.

Shared domain policy is not the same thing as a universal `SharedServices` layer. Avoid common helpers that depend on every feature's private DTOs or route unrelated business decisions through one service. Assess whether the common abstraction represents genuine stable meaning, not merely similar-looking lines of code.

### Example D — Commands, queries, and CQRS are different decisions

| Design choice | Meaning | Automatically implied by slices? |
| --- | --- | --- |
| Feature-oriented organization | Keep related application behavior discoverable and cohesive | Yes, for adopted VSA |
| Command/query operation naming | Describe an action that changes state or retrieves information | No |
| Separate read/write application models (CQRS) | Distinct models or paths optimized for reads and writes | No |
| Separate databases | Distinct physical stores with synchronization concerns | No |
| Event sourcing | Persist business events as the authoritative history/state representation | No |
| Asynchronous messaging | Move communication through queues/events and deal with eventual outcomes | No |

Jimmy Bogard's [original article](https://www.jimmybogard.com/vertical-slice-architecture/) describes his request-per-use-case approach as naturally using CQRS. This is **his chosen design**, not a mandatory consequence of organizing by feature. Microsoft's [CQRS pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) defines separation of read and write models and explains its benefits and complexity, including more serious consistency obligations with separate data stores.

Start with ordinary direct read/write operations unless a different query model, throughput pattern, security separation, or consistency need justifies CQRS. If the read and write models differ, the same database can remain adequate; if physical stores split, explicitly evaluate propagation delays, failure handling, authorization, stale reads, and durability. Do not infer event sourcing or message brokers from CQRS.

### Example E — Cross-cutting concerns and composition

| Concern | Potential shared mechanism | Local feature responsibility or caution |
| --- | --- | --- |
| Authentication | Host authentication support | Use authorized identities; avoid relying on caller assumptions |
| Authorization | Framework policies, service-level checks | Protect resource/action-specific decisions across every relevant invocation path |
| Input validation | Endpoint filters, framework validation, focused reusable components | Business invariants still enforced by authoritative policy |
| Logging and telemetry | Shared instrumentation, middleware, decorators | Preserve feature context without contaminating domain rules with provider APIs |
| Transactions | Application coordinator, provider transaction facilities | Test actual atomicity, concurrency, rollback, and failure semantics |
| Caching | Shared infrastructure with focused cache policy | Account for invalidation, stale data, authorization, and sensitive results |
| Exceptions | Middleware, filters, application result contracts | Distinguish expected business denial from technical failure |
| Object composition | Manual factories or supported DI | Check actual registration, scope, disposal, and startup when materially changed |

ASP.NET Core [middleware](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/) and [filters](https://learn.microsoft.com/en-us/aspnet/core/mvc/controllers/filters) can centralize common HTTP behavior. Decorators or mediation may be appropriate elsewhere. A framework's presence is not a reason to install an additional behavior pipeline, and an application with no HTTP host should not adopt HTTP-only mechanisms. For older .NET Framework applications, use the libraries and manual composition supported by the actual project.

### Example F — Slices within an adopted modular monolith

Suppose a single deployed application has `Orders` and `Inventory` modules. `Orders` can contain `PlaceOrder`, `CancelOrder`, and `GetOrder` slices, while `Inventory` owns `ReserveStock` and `ReleaseStock` operations. The Orders slice may call Inventory's approved operation through a direct facade or interface. The Inventory module protects its own stock mutations. No broker, event bus, separate database, or new assembly is necessary simply because both module and slice boundaries exist.

When [STD-015](standards/modular-monolith.md#std-015) is adopted, it governs module ownership, acyclic implementation dependencies, and meaningful module-facing contracts. STD-016 governs the **feature/use-case organization within or across the application**. A feature directory called `Inventory` does not automatically constitute an adopted module, and a module does not need one slice per public method.

## Level 3 — Review, test, and modernize proportionately

### Scenario-based architecture review

| Scenario | Inspect or test | What evidence cannot establish by itself |
| --- | --- | --- |
| Add an order detail field | Trace endpoint, mapping, use case, and tests for the actual change | A feature folder alone does not prove change locality |
| Cancel an order in permitted and rejected states | Exercise the public operation and authoritative policy | A green unit test cannot prove persistence under concurrency |
| Two features enforce one refund ceiling | Identify the policy owner and all material mutation paths | One shared type name does not prove a single enforced rule |
| Feature A uses Feature B | Inspect intended operation surface, direct calls, and implementation imports | One-way project references may hide runtime or semantic cycles |
| Authorization through HTTP and background job | Verify both entry paths apply the relevant business authorization | Middleware test alone may miss an internal bypass |
| Introduce CQRS read projection | Test semantic consistency, projection authorization, and relevant stale-data handling | Separate classes do not prove actual CQRS value or guarantees |
| Introduce or change a SQL adapter | Test meaningful real-provider or validated-contract behavior under STD-009 | An in-memory fake cannot establish SQL behavior |
| Change composition | Exercise significant registrations, constructor lifetimes, and startup | Unit tests with hand-built objects do not prove host wiring |
| Move a legacy use case into a feature | Compare behavior and published public contracts before/after | A successful source move does not prove compatibility |

### Practical evidence strategy

1. **Identify the actual material change.** Name the use case, existing callers, business decisions, technical boundaries, tests, and public contracts.
2. **Inspect change locality and dependencies.** Trace the relevant source files, imports, application services, direct collaborators, domain models, and integration calls. Decide whether technical code is reused appropriately or private feature internals are leaking.
3. **Test meaningful behavior first when executable work changes.** Follow [STD-001](standards/engineering-principles.md#std-001)'s Red/Green/Refactor expectations, targeting observable successful, rejected, and failure behavior rather than private method counts. Feature-oriented test directories are optional.
4. **Exercise significant real boundaries.** Use representative adapter/integration evidence per [STD-009](standards/testing.md#std-009), actual transaction and authorization tests where those properties matter, and material composition checks when changed. [Microsoft's ASP.NET Core integration-testing guidance](https://learn.microsoft.com/en-us/aspnet/core/testing/integration-testing) explains the tradeoff between isolated and broader tests.
5. **Review semantics and disclose limits.** A reference graph, directory naming rule, or build cannot prove cohesion, invariant ownership, or domain fidelity. Record the exact revision, actual executed commands and results, environments, manual review, exceptions, and unverified concerns.

No architecture analyzer, test framework replacement, blanket handler test, or new CI gate is required merely to adopt slices. If a project already has useful architecture checks, extend them selectively for a demonstrable boundary rather than building a general-purpose framework.

### Incremental modernization of an existing application

For a traditional ASP.NET/.NET Framework or layered application:

1. Select one feature that is already being changed or repeatedly causes cross-layer coordination.
2. Characterize existing success/failure behavior, published APIs, and important integration assumptions using supported tests and review.
3. Identify the business-policy decisions and ensure they do not depend on concrete UI/provider types (Required STD-011).
4. Localize only the meaningful application operation and feature-specific mapping; reuse existing viable infrastructure adapters and shared domain policies.
5. Preserve caller contracts, supported C# syntax, `.csproj` format, packages, and actual build/test tooling until a separate compatibility decision authorizes changing them.
6. Verify the modified behavior, important real dependencies, and composition; reassess whether further slicing would improve actual maintainability.

Microsoft's [Strangler Fig pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig) is one **larger-scale migration option** for replacing independently routed functionality. In-process incremental feature reorganization does **not** require a facade, new service, new deployment, or adoption of that pattern.

### Review questions, not a mandatory checklist

- Can a maintainer locate a meaningful operation and understand its actual dependencies without navigating unrelated application services?
- Are feature boundaries sized around changes that occur together rather than arbitrary request or endpoint counts?
- Does any slice directly depend on another's internal persistence, mutable state, or technical implementation without a deliberate collaboration contract?
- Can business invariants be bypassed through a different feature, adapter, job, or HTTP route?
- Would sharing or removing a proposed abstraction reduce coupling, or would it create a central hub of unrelated responsibilities?
- Are handler, DTO, mediator, pipeline, project, and interface choices justified independently of a VSA label?
- Do tests prove meaningful behavior and the actual external guarantees they claim?
- Are the exact observed toolchain, revision, tests, limitations, and compatibility risks recorded?

If a slice participates in a consequential event-mediated workflow, evaluate the separately conditional [STD-018](standards/event-driven.md#std-018) and its [event-driven guide](event-driven-guidance.md). A feature handler, mediated request or slice boundary does not itself call for asynchronous messaging, CQRS or event sourcing.

## Primary references and boundary of claims

- [Microsoft — Feature organization in ASP.NET Core MVC](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/develop-asp-net-core-mvc-apps#feature-organization) and [Feature Slices for ASP.NET Core MVC](https://learn.microsoft.com/en-us/archive/msdn-magazine/2016/september/asp-net-core-feature-slices-for-asp-net-core-mvc): alternatives to technical-type folders, not requirements for one class per endpoint.
- [Microsoft — Architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles): separation, encapsulation, explicit dependencies, and dependency inversion.
- [Microsoft — CQRS pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs): when distinct read and write models help and when their complexity matters.
- [Microsoft — Designing a DDD-oriented service](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice): domain models and application coordination in a specific example.
- [Microsoft — ASP.NET Core integration testing](https://learn.microsoft.com/en-us/aspnet/core/testing/integration-testing): focused testing of important real dependencies.
- [Jimmy Bogard — Vertical Slice Architecture](https://www.jimmybogard.com/vertical-slice-architecture/): original April 2018 primary account of request-focused change locality and selective abstractions.

These are **source-informed design recommendations**, not evidence that a particular consumer project adopted the pattern. All code and layout examples above are illustrative. No example in this document is claimed to have compiled, executed, met performance goals, or passed CI.
