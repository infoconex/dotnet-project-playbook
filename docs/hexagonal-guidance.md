# Hexagonal Architecture: on-demand ports, adapters, and C# guidance

This guide is **illustrative**, not a second standard. [Recommended STD-012](standards/hexagonal.md#std-012) is authoritative for adoption, explicit port interfaces, verification, and alternatives. [Required STD-011](standards/dependency-direction.md#std-011) protects business-policy independence whether or not Hexagonal Architecture is used; [STD-010](standards/solid.md#std-010) governs SOLID design.

During ordinary project setup or assessment, **do not require an architecture tutorial**. Answer the user's concrete question or offer these on-demand levels:

1. [**Level 1 — Boundary refresher**](#level-1-boundary-refresher): inbound/driving versus outbound/driven, source versus runtime dependencies.
2. [**Level 2 — C# interfaces, adapters, and composition**](#level-2-c-interfaces-adapters-and-composition): a small order-availability example that includes one implementation of each port, plus an alternative.
3. [**Level 3 — Testing, review, and adoption**](#level-3-testing-review-and-adoption): independent test seams and realistic migration evidence.

The examples deliberately use features available in C# 7.3 and basic .NET APIs. Snippets are **separate illustrative excerpts**, not compiled, production-ready code or a verified .NET Framework/modern .NET template. Production C# types would normally each have their own file. The actual target framework, available packages, project format, test runner, and environment must be verified by an adopting project.

## <a name="level-1-boundary-refresher"></a>Level 1 — Boundary refresher

Think of the application as offering operations and requesting external capabilities. Interfaces describe each *identified port*; adapters translate to and from the actual outside world.

| Direction / name | What it represents | Example | Who implements the port? |
| --- | --- | --- | --- |
| **Inbound port** (driving/primary) | Application operation offered to actors | `ICheckOrderAvailability` | Application use case |
| **Driving adapter** | Actor-facing caller of the application | CLI command or HTTP endpoint | Not an inbound-port implementation; it **consumes** the interface |
| **Outbound port** (driven/secondary) | Capability the application needs from elsewhere | `IInventoryAvailability` | Outside technology adapter |
| **Driven adapter** | Supplier of the application's requested capability | SQL, remote service, or in-memory implementation | **Implements** the outbound interface |
| **Composition root** | Selects and connects real implementations | Host startup | References concrete implementations intentionally |

At **runtime**, a CLI command calls the inbound port, the use case calls the outbound port, and a driven adapter supplies the answer. At **compile time**, the use case knows only the inbound/outbound interfaces and business types, not the chosen database or host. An outer adapter can reference the inward port contract. This means **an interface on both sides is useful even with a single implementation**: an application test substitutes the driven port; a driving-adapter test substitutes the inbound port. But not every ordinary class, DTO, or calculation is an application port.

Hexagonal, Ports-and-Adapters, Onion, and Clean Architecture share dependency-inversion goals, with different emphases and layouts. Microsoft describes these related styles in [Common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures). The playbook chooses the explicit two-sided port rule *when Hexagonal Architecture is adopted*; it does not prescribe Clean Architecture's project graph or mandate the pattern for a pure library.

## <a name="level-2-c-interfaces-adapters-and-composition"></a>Level 2 — C# interfaces, adapters, and composition

### Application-owned contracts

The application exposes an inbound use-case contract and requests an outbound capability. `OrderRequest` is a business input value, **not** another port; its class does not need an interface.

```csharp
// ICheckOrderAvailability.cs — inbound port, owned by the application boundary.
public interface ICheckOrderAvailability
{
    bool CanFulfill(OrderRequest request);
}
```

```csharp
// IInventoryAvailability.cs — outbound port, owned by its consumer.
public interface IInventoryAvailability
{
    bool HasStock(string sku, int quantity);
}
```

```csharp
// OrderRequest.cs — ordinary business data, not a port.
public sealed class OrderRequest
{
    public string Sku { get; }
    public int Quantity { get; }

    public OrderRequest(string sku, int quantity)
    {
        Sku = sku;
        Quantity = quantity;
    }
}
```

### Application behavior implements the inbound port

The `CheckOrderAvailabilityUseCase` makes a small policy decision and relies on the outbound capability, not on SQL, HTTP, or a particular inventory provider. Both interfaces still exist with one use case and one inventory adapter.

```csharp
// CheckOrderAvailabilityUseCase.cs — application policy.
using System;

public sealed class CheckOrderAvailabilityUseCase : ICheckOrderAvailability
{
    private readonly IInventoryAvailability _inventory;

    public CheckOrderAvailabilityUseCase(IInventoryAvailability inventory)
    {
        _inventory = inventory ??
            throw new ArgumentNullException(nameof(inventory));
    }

    public bool CanFulfill(OrderRequest request)
    {
        if (request == null)
            throw new ArgumentNullException(nameof(request));

        if (string.IsNullOrWhiteSpace(request.Sku) || request.Quantity <= 0)
            return false;

        return _inventory.HasStock(request.Sku, request.Quantity);
    }
}
```

This is a deliberately **narrow business example**: checking availability is not an atomic inventory reservation or a durable order placement. A real ordering use case needs transactions, concurrency rules, authorization, and other domain outcomes as appropriate. The contract deliberately promises only an availability check.

### A driving adapter consumes the inbound port

A CLI adapter translates command-line input into a business request. Its compile-time dependency is `ICheckOrderAvailability`, not `CheckOrderAvailabilityUseCase`.

```csharp
// OrderAvailabilityCommand.cs — simplified driving adapter.
public sealed class OrderAvailabilityCommand
{
    private readonly ICheckOrderAvailability _checkAvailability;

    public OrderAvailabilityCommand(ICheckOrderAvailability checkAvailability)
    {
        _checkAvailability = checkAvailability;
    }

    public bool Execute(string sku, string quantityText)
    {
        int quantity;
        if (!int.TryParse(quantityText, out quantity))
            return false;

        return _checkAvailability.CanFulfill(new OrderRequest(sku, quantity));
    }
}
```

### A driven adapter implements the outbound port

An in-memory adapter is enough to illustrate the substitution seam without implying that a specific database has been tested. A real SQL implementation would implement the **same** interface while owning its database details outside application policy.

```csharp
// InMemoryInventoryAvailability.cs — illustrative driven adapter.
using System.Collections.Generic;

public sealed class InMemoryInventoryAvailability : IInventoryAvailability
{
    private readonly IDictionary<string, int> _available;

    public InMemoryInventoryAvailability(IDictionary<string, int> available)
    {
        _available = available;
    }

    public bool HasStock(string sku, int quantity)
    {
        int count;
        return _available.TryGetValue(sku, out count) && count >= quantity;
    }
}
```

### An outer composition root connects implementations

```csharp
// ApplicationComposition.cs — illustrative manual composition.
using System.Collections.Generic;

public static class ApplicationComposition
{
    public static OrderAvailabilityCommand CreateCommand()
    {
        IInventoryAvailability inventory =
            new InMemoryInventoryAvailability(
                new Dictionary<string, int> { { "item-1", 5 } });

        ICheckOrderAvailability application =
            new CheckOrderAvailabilityUseCase(inventory);
        return new OrderAvailabilityCommand(application);
    }
}
```

The composition root legitimately knows both concrete classes. The code does not need a DI container, physical `Domain`, `Application`, or `Infrastructure` assemblies, or modern-only syntax. If separate projects help, a typical reference direction is `Host → Application` and `Host → Infrastructure`, with `Infrastructure → Application` for the outbound contract; `Application` does not refer back to `Infrastructure`. Legacy non-SDK .NET Framework project-reference syntax differs from SDK-style examples—use the actual repository's project format.

### When a direct technical collaboration is simpler

An exporter that writes an already-prepared string to a local file, with no application policy or relevant replacement boundary, may simply call `File.WriteAllText`. Do not introduce `IExportWriter`, an application use case, and adapters merely to give it a hexagonal appearance. If export behavior becomes business-critical or substitutable, reassess the boundary. A justified decision **not to adopt** a Recommended style does not waive independently Required policy isolation or applicable tests.

## <a name="level-3-testing-review-and-adoption"></a>Level 3 — Testing, review, and adoption

### Independent verification at each meaningful boundary

| What to establish | Exercise | Substitute or real dependency | What it does **not** prove |
| --- | --- | --- | --- |
| Application policy | Call `ICheckOrderAvailability.CanFulfill` with valid/invalid requests | Stub `IInventoryAvailability`, with controlled stock answers | Real SQL/service correctness or CLI parsing |
| Significant driving adapter | Call `OrderAvailabilityCommand.Execute` with parseable/malformed inputs | Spy or stub `ICheckOrderAvailability` | Business-rule correctness or inventory provider behavior |
| Significant driven adapter | Execute actual provider translation, queries, failures, or serialization | Representative real provider, or provider-validated contract when [STD-009](standards/testing.md#std-009) is triggered | Full production operations or cross-provider compatibility |

An application test can arrange an inventory substitute returning `true`, call the use case **through `ICheckOrderAvailability`**, and assert its decision and invocation arguments; repeat for invalid requests and insufficient inventory. A driving-adapter test can provide a spy `ICheckOrderAvailability`, call the command with `"3"`, and assert it received `OrderRequest` with quantity `3`; malformed text must not reach the port. These are **test-design examples**, not executed tests or a mandate to test trivial forwarding. A database-backed inventory adapter requires suitably representative provider-level verification when its risk triggers STD-009; an in-memory substitute does not meet that requirement.

### Architecture review questions

1. Which application operations are actual **inbound ports**, and which consumed external capabilities are **outbound ports**? Does each identified port have an explicit interface, including a single-implementation port?
2. Is each interface owned by or placed appropriately for the application consumer? Do contract members express consumer needs, or leak a database, transport, or DI framework?
3. Does a driving adapter call an inbound interface, and does the use case depend on an outbound interface? Can a significant driving adapter and significant application use case be tested independently?
4. Are policy decisions independent of concrete external mechanisms per [STD-011](standards/dependency-direction.md#std-011)? Is an apparent adapter hiding business rules? Is the composition root the deliberate place where concretes meet?
5. What source/project references can be checked objectively? What semantic boundaries still require code review? Are skipped tests or unverified providers disclosed honestly?
6. For a legacy or small project, would an incremental port help more than additional abstractions cost? If not adopting the pattern, what simple design and rationale are recorded?

Where valuable, inspect `.csproj` project references, source imports, interface implementations, use-case constructors, and tests; use the existing build or architecture checks if they establish a specific property. A passing build cannot prove semantic policy isolation or faithful port behavior. There is no required analyzer, CI gate, universal project skeleton, or per-method test quota. [STD-001](standards/engineering-principles.md#std-001) governs applicable test-first behavior, and [STD-009](standards/testing.md#std-009) governs material real-boundary evidence and its reviewed exceptions.

### Context-sensitive adoption

- **New small pure library:** Do not manufacture HTTP/database ports or multiple assemblies. Existing SOLID and policy-isolation obligations remain.
- **New service with meaningful adapters:** Identify the actual inbound use cases and external needs, express both kinds of ports as interfaces, write behavior through those seams, and choose physical projects based on enforcement value.
- **Existing monolith or .NET Framework application:** Start with the changed behavior, keep public API compatibility in view, characterize important outcomes, and extract a useful port without asserting that a single-assembly migration is complete architectural isolation.
- **Trivial technical collaborator:** Prefer a direct concrete call where it carries no policy, significant external boundary, or credible substitution requirement; document the architecture choice proportionately.

Related Microsoft guidance: [Architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles), [Common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures), and [Dependency injection guidelines](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines). These explain relevant design mechanisms; the explicit two-sided interface rule comes from [STD-012](standards/hexagonal.md#std-012), not from a claim that every Microsoft application must use interfaces for all types.
