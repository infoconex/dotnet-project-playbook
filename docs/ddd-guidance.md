# Domain-Driven Design and domain modeling: on-demand .NET guidance

Use Domain-Driven Design (DDD) to make **meaningful business complexity explicit and safe to change**. Begin with real business scenarios and vocabulary; adopt tactical patterns only when they protect actual behavior or consistency boundaries. Microsoft's [strategic DDD](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis) and [tactical DDD](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design) guidance provide the technical foundation.

This is **non-normative, illustrative guidance**, not an executable template, a verified domain model, or a second set of obligations. [Recommended STD-014](standards/ddd.md#std-014) is authoritative for the conditional DDD expectation. The independent [SOLID](standards/solid.md#std-010), [business-policy dependency](standards/dependency-direction.md#std-011), [Hexagonal](standards/hexagonal.md#std-012), [Clean](standards/clean.md#std-013), [Optional compiled-project separation](standards/engineering-principles.md#std-003), [TDD](standards/engineering-principles.md#std-001), and [conditional external-boundary testing](standards/testing.md#std-009) standards continue to apply on their own terms.

The three levels below are optional explanations, not a mandatory onboarding sequence or maturity score.

## Level 1 — Decide whether DDD helps

Ask: **Would a carefully maintained domain language and behavior model prevent real business mistakes or recurring coupling?** If not, start simpler.

| Project/area | Proportionate starting choice | Reassess when |
| --- | --- | --- |
| Core business workflow with complex rules, states, and changing policies | Strategic context discovery plus selected tactical DDD around significant invariants | Competing definitions, cross-context interactions, or accidental invalid states appear |
| Supporting capability with moderate rules | Clear domain terms, simple cohesive behavior, explicit invariants; selectively add richer patterns | Rules span concepts or multiple teams/consumers interpret the model differently |
| Generic authentication or commodity capability | Prefer a proven service/library and a clear integration boundary | The organization's business meaning differs materially from the external system's model |
| Straightforward CRUD application | Simple data-centric operations and validation; no mandatory aggregate/repository hierarchy | Editing one field starts affecting other business state transitions or cross-record consistency |
| Pure parsing/calculation library | Small functions/value types, direct callers, and independent tests | Domain vocabulary or real business policy becomes central to its purpose |
| Existing .NET Framework application | Characterize changed behavior, isolate one useful rule/boundary, preserve contracts | Focused improvements reveal a cohesive domain model worth extracting |

**Strategic DDD** answers which business problems and meanings belong together. **Tactical DDD** answers how to represent and protect rules inside a selected context. Strategic analysis can be valuable without adopting every tactical pattern, and different bounded contexts in the same application can make different choices.

An **important distinction**: a domain is the overall business problem space; a subdomain is a business capability or problem area; a bounded context is the boundary within which one model and language have defined meaning. These do not necessarily map one-to-one. A bounded context can be a module in a monolith, not a microservice or separate compiled project.

## Level 2 — Practical strategic and tactical modeling

### Start with subdomains and language, not technical layers

Consider a fictional order-processing product, strictly as a learning example:

| Area | Possible classification | Relevant language and responsibility |
| --- | --- | --- |
| Order acceptance and fulfillment | Core **if** it differentiates this business | Ordering accepts customer requests; fulfillment decides and records physical dispatch |
| Invoicing and adjustments | Supporting | Billing owns charges, invoices, credits, and payment-facing terms |
| Account sign-in | Generic | Identity can use an established external provider behind a suitable boundary |

These classifications depend on **this business's actual competitive priorities**, not on fixed labels. For a different company, billing might be core and fulfillment generic. In real work, confirm the classification with business stakeholders rather than deriving it from folder names.

Within the **Ordering** bounded context, `Order` may mean a commercial request with lines, acceptance rules, and cancellation eligibility. Within **Fulfillment**, an order reference may instead mean a dispatch instruction and shipment status. They can share an identifier without sharing the same object model or the same meaning of every attribute.

When contexts interact, record only important relationships:

| Context interaction | Question to settle | Possible approach |
| --- | --- | --- |
| Ordering → Fulfillment | Who decides an order is accepted, and who owns dispatch? | Explicit published contract translating order acceptance to fulfillment instruction |
| Fulfillment → Ordering | When does dispatch become an irreversible cancellation boundary? | A clearly defined business event or operation, with delivery/ordering safeguards chosen for the actual consistency need |
| Billing ↔ Ordering | Does `Customer` mean an account owner or invoice recipient? | Independent models, translation or anti-corruption boundary where meanings conflict |

This small table can serve as a context map; a formal diagram, event-storming workshop, or independent development team for every context is not required. Consider upstream/downstream ownership, contract negotiation, and an anti-corruption layer where an external model would otherwise leak into the domain. [Microsoft's domain analysis](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis) discusses core/supporting/generic subdomains, context maps, and team considerations.

### Model a real rule through meaningful operations

Suppose the agreed fictional business rules are:

1. An order must contain at least one line before submission.
2. A line quantity must be positive.
3. An order can be cancelled while Draft or Submitted, but not after Dispatch.

The following **illustrative C# 7.3-compatible excerpts** intentionally omit actual `.csproj` files, namespaces and using directives, transaction management, persistence, and concurrency control. They have **not been compiled or executed**. They show the responsibility placement, not a production-ready ordering subsystem.

`Quantity.cs` — a small immutable value object with value equality:

~~~csharp
public struct Quantity : System.IEquatable<Quantity>
{
    public int Value { get; }

    public Quantity(int value)
    {
        if (value <= 0)
            throw new System.ArgumentOutOfRangeException(nameof(value));

        Value = value;
    }

    public bool Equals(Quantity other) => Value == other.Value;
    public override bool Equals(object obj) =>
        obj is Quantity && Equals((Quantity)obj);
    public override int GetHashCode() => Value.GetHashCode();
}
~~~

For an actual domain, decide whether the default zero-initialized `struct` is a valid value or whether a class/factory or additional validation is needed. This is one reason a quick illustrative type is not proof of a complete domain invariant.

`Order.cs` — an identity-bearing entity that can act as a one-entity aggregate root if the described order state is a genuine consistency boundary:

~~~csharp
public enum OrderStatus { Draft, Submitted, Dispatched, Cancelled }

public sealed class Order
{
    private int _lineCount;

    public System.Guid Id { get; }
    public OrderStatus Status { get; private set; }

    public Order(System.Guid id)
    {
        if (id == System.Guid.Empty)
            throw new System.ArgumentException("An order ID is required.", nameof(id));

        Id = id;
        Status = OrderStatus.Draft;
    }

    public void AddLine(Quantity quantity)
    {
        if (Status != OrderStatus.Draft)
            throw new System.InvalidOperationException("Only draft orders can change.");
        if (quantity.Value <= 0)
            throw new System.ArgumentOutOfRangeException(nameof(quantity));

        checked { _lineCount += quantity.Value; }
    }

    public void Submit()
    {
        if (Status != OrderStatus.Draft || _lineCount == 0)
            throw new System.InvalidOperationException("A draft needs a line.");

        Status = OrderStatus.Submitted;
    }

    public void Dispatch()
    {
        if (Status != OrderStatus.Submitted)
            throw new System.InvalidOperationException("Only submitted orders dispatch.");

        Status = OrderStatus.Dispatched;
    }

    public void Cancel()
    {
        if (Status != OrderStatus.Draft && Status != OrderStatus.Submitted)
            throw new System.InvalidOperationException("Dispatch prevents cancellation.");

        Status = OrderStatus.Cancelled;
    }
}
~~~

This abbreviated model counts line quantities rather than representing actual products, pricing, fulfillment reservations, or child line entities. An actual order aggregate would need those concepts only if the business scenarios require them. The important property shown is that callers cannot set `Status` directly or bypass the transition methods. The guard in `AddLine` also rejects a default/invalid `Quantity`; the value object alone would not prevent all invalid default struct values.

`OrderTests.cs` — illustrative NUnit 3-style behavioral scenarios:

~~~csharp
[Test]
public void Submit_WithLine_ChangesState()
{
    var order = new Order(System.Guid.NewGuid());
    order.AddLine(new Quantity(2));

    order.Submit();
    Assert.That(order.Status, Is.EqualTo(OrderStatus.Submitted));
}

[Test]
public void Submit_WithoutLines_IsRejected()
{
    var order = new Order(System.Guid.NewGuid());
    Assert.Throws<System.InvalidOperationException>(() => order.Submit());
}

[Test]
public void Cancel_AfterDispatch_IsRejected()
{
    var order = new Order(System.Guid.NewGuid());
    order.AddLine(new Quantity(1));
    order.Submit();
    order.Dispatch();

    Assert.Throws<System.InvalidOperationException>(() => order.Cancel());
    Assert.That(order.Status, Is.EqualTo(OrderStatus.Dispatched));
}
~~~

These examples illustrate independent domain tests, **not observed TDD execution**, because no red/green run occurred. In a real change [STD-001](standards/engineering-principles.md#std-001) governs the failing-test-first process. The public API, identity, value equality, cancellation rule, exception behavior, and consistency scope must be agreed with domain stakeholders, not inferred from this hypothetical sample.

### Keep use-case orchestration distinct

An application operation might load an order, verify the caller's authorization, invoke `order.Cancel()`, persist through an appropriate technology-neutral capability, and return a result. The **domain** decides whether cancellation is allowed; the **application** coordinates loading, authorization and persistence. Some application-level decisions may themselves be business policy and must satisfy [STD-011](standards/dependency-direction.md#std-011), wherever implemented. An explicit repository is one possible persistence contract, **not** an obligation for every entity or application. See Microsoft's [persistence-layer guidance](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design).

Where a rule genuinely spans several domain objects but belongs to none of them, a focused **domain service** can express it. Where a business event needs meaningful reactions, distinguish a **domain event** from an externally published **integration event**, including whether publication must occur only after a successful commit. Direct calls may remain simpler when no independent reaction is needed. Neither pattern changes the Required source dependency direction or demands an event bus, CQRS, or event sourcing.

### Counterexample: simple CRUD does not need a rich aggregate

A small internal table editor that allows permitted users to update a non-sensitive display description may only need authorization, input validation, persistence, and ordinary tests. Do not invent `DescriptionAggregate`, `IDescriptionRepository`, or domain events unless real business rules or meaningful boundaries emerge. A simple persistence model is not automatically an unacceptable "anemic domain"; [Microsoft explicitly distinguishes simple CRUD from complex business models](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model).

## <a name="level-3-review-testing-and-evolution"></a>Level 3 — Review, testing, and evolution

### Domain behavior and boundary scenarios

Select only scenarios that matter to the changed model:

| Scenario | Relevant evidence | What it does not establish |
| --- | --- | --- |
| A Draft order with lines submits | Independent domain behavior test | Database persistence or authorization |
| Empty order submission is rejected | Negative domain invariant test | Protection against every persistence bypass |
| A dispatched order cannot cancel | State-transition test with unchanged resulting state | Correct behavior during concurrent updates in two processes |
| Two contexts use different meanings of `Customer` | Domain scenario/term review and translation-contract inspection | That runtime messages are delivered correctly |
| Two concurrent operations race on the same order | Representative persistence/concurrency test, with actual transaction and conflict strategy | Correctness for every database/provider configuration |
| Domain event becomes an external notification | Integration test of commit/publish/failure handling where significant | Exactly-once delivery unless specifically demonstrated |

For a real model, examine whether constructors, setters, serializers, ORM materialization, concurrency, or direct child mutations can bypass invariants. Some domain constraints require database uniqueness constraints, optimistic concurrency, transactional coordination, or downstream reconciliation. A green isolated domain suite alone does not establish those guarantees; apply [STD-009](standards/testing.md#std-009) when materially significant external-adapter behavior is involved. Avoid assuming domain events are synonymous with eventual consistency or that an in-process event implies a durable integration event.

### Architectural and legacy checks

- Review terms, scenarios, and ambiguous assumptions with available domain experts; disclose when business validation was unavailable.
- Check boundaries semantically: a `Domain` namespace, assembly, context diagram, or `IAggregateRoot` marker cannot prove model correctness.
- Apply STD-011 for required business-policy independence. If Hexagonal is adopted, satisfy STD-012's explicit identified port interfaces; if Clean is adopted, protect the entire defined Application Core under STD-013. DDD adoption does not silently opt in to either style.
- Keep physical projects Optional under STD-003. A .NET Framework application with C# 7.3 can implement useful model boundaries without records, EF Core, ASP.NET Core DI, SDK-style projects, or modern language syntax. Conversely, modern .NET can use records/value types where their equality and construction semantics fit the domain.
- In legacy work, characterize affected existing behavior, improve one meaningful rule or context boundary at a time, retain public contracts unless change is authorized, and review actual regressions. Do not mandate a whole-system rewrite.
- Record the exact revision, tests actually run, business evidence reviewed, unsupported environment scenarios, and unresolved consistency risks. Documentation-only examples here have no compiled/tested verification claim.

## Microsoft references and interpretation

- [Use domain analysis to model microservices](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis) — strategic concepts, subdomains, bounded contexts, and ownership.
- [Use tactical DDD to design microservices](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design) — entity/value semantics, aggregates, domain services, events.
- [Design a DDD-oriented microservice](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice) — domain complexity, logical layers, and simpler CRUD alternative.
- [Design a microservice domain model](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model) — domain behavior and aggregate invariants.
- [Design the infrastructure persistence layer](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design) — optional custom repositories and transaction concerns.
- [Domain events: design and implementation](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation) — domain/integration event distinctions.

The sources' microservice-specific deployment advice is **not** a requirement to deploy this learning example as microservices. The choice of domain patterns should follow the business problem, not the deployment model.
