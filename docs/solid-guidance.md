# Applying SOLID in C#: on-demand guidance

This is an **illustrative learning and design-review guide**, not a second normative standard. The authoritative Required obligation, applicability, and exception rules live in [STD-010 — SOLID design principles](standards/solid.md#std-010). Microsoft's [architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles), [SOLID overview](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-application-layer-web-api-design), and [interface design guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/interface) provide the underlying technical references.

Developers are assumed to know SOLID during ordinary project creation or repository assessment. **Do not require a five-principle interview or tutorial.** If someone asks for help, use the level they requested, or offer a choice of:

1. [**Level 1 — Quick refresher**](#level-1-quick-refresher): brief concepts and warning signs.
2. [**Level 2 — Practical C# examples**](#level-2-practical-c-examples): before/after code and real tradeoffs.
3. [**Level 3 — Deep dive**](#level-3-deep-dive): design alternatives, refactoring sequences, contract tests, and constraints.

These are conversation and reference options, **not a shipped interactive agent, UI, or generated project**. When someone already asks a specific question, answer directly instead of making them select a level first.

## <a name="level-1-quick-refresher"></a>Level 1 — Quick refresher

| Principle | One-sentence reminder | Warning sign |
| --- | --- | --- |
| **S — Single Responsibility** | Keep a type focused on one cohesive responsibility and reason to change. | Business policy, persistence, and formatting change the same class for unrelated reasons. |
| **O — Open/Closed** | Support real extension points without repeatedly modifying stable selection logic. | Adding each known variant means modifying a central chain of conditions. |
| **L — Liskov Substitution** | Implementations must preserve the promises their clients rely on. | A subtype unexpectedly rejects a valid call or weakens an invariant. |
| **I — Interface Segregation** | Keep client-facing contracts limited to relevant capabilities. | Implementers throw for methods that do not apply to them. |
| **D — Dependency Inversion** | Have important policy depend on a suitable contract instead of a concrete implementation detail. | A business operation instantiates a database client or writes directly to a file. |

These are related judgment tools, not five demands for more interfaces. A small class with one stable concrete collaborator may already be well designed. The [Required standard](standards/solid.md#std-010) determines applicability.

## <a name="level-2-practical-c-examples"></a>Level 2 — Practical C# examples

Each before/after pair illustrates one common pressure, not a universal transformation. Examples use syntax available in **C# 7.3**, so their main design ideas can apply to a traditional .NET Framework project as well as modern .NET. Each block represents a standalone teaching excerpt; types with similar names in different blocks are alternative designs, not a single project to paste together. Real production code would ordinarily put primary types in separate files as described by [STD-005](standards/csharp.md#std-005).

### S — Single Responsibility: pricing versus export formatting

**Before:** Two unrelated reasons to change are kept together.

```csharp
using System.Globalization;

public sealed class PurchaseSummary
{
    public decimal CalculateTotal(decimal[] prices)
    {
        decimal total = 0m;
        foreach (decimal price in prices)
        {
            total += price;
        }

        return total;
    }

    public string FormatCsv(decimal total)
    {
        return total.ToString(CultureInfo.InvariantCulture);
    }
}
```

**After:** A pricing rule and a CSV representation can evolve separately.

```csharp
using System.Globalization;

public sealed class PurchaseTotal
{
    public decimal Calculate(decimal[] prices)
    {
        decimal total = 0m;
        foreach (decimal price in prices)
        {
            total += price;
        }

        return total;
    }
}

public sealed class PurchaseCsvFormatter
{
    public string Format(decimal total)
    {
        return total.ToString(CultureInfo.InvariantCulture);
    }
}
```

**Tradeoff:** A single simple operation that formats its own internal value may not warrant two classes. Separate them when independent change pressures or consumers actually exist, not because a class has more than one method.

**Review cue:** Are we separating *reasons to change* or merely splitting a cohesive responsibility into trivial forwarding classes?

### O — Open/Closed: an actual shipping-rate variation

**Before:** Every new shipping service modifies a growing central conditional.

```csharp
public sealed class ShippingQuote
{
    public decimal Calculate(decimal weight, string service)
    {
        if (weight <= 0m)
        {
            throw new System.ArgumentOutOfRangeException(nameof(weight));
        }

        if (service == "Ground")
        {
            return weight * 1.5m;
        }

        if (service == "Express")
        {
            return weight * 3m;
        }

        throw new System.ArgumentException("Unknown service", nameof(service));
    }
}
```

**After:** If shipping rates really vary independently, the quote depends on a supported rate contract.

```csharp
public interface IShippingRate
{
    decimal Calculate(decimal weight);
}

public sealed class GroundShippingRate : IShippingRate
{
    public decimal Calculate(decimal weight) => weight * 1.5m;
}

public sealed class ExpressShippingRate : IShippingRate
{
    public decimal Calculate(decimal weight) => weight * 3m;
}

public sealed class ShippingQuote
{
    private readonly IShippingRate _rate;

    public ShippingQuote(IShippingRate rate)
    {
        _rate = rate ?? throw new System.ArgumentNullException(nameof(rate));
    }

    public decimal Calculate(decimal weight)
    {
        if (weight <= 0m)
        {
            throw new System.ArgumentOutOfRangeException(nameof(weight));
        }

        return _rate.Calculate(weight);
    }
}
```

**Tradeoff:** The after version is justified when shipping policies are genuinely independently extensible. If there are only two fixed, stable cases, the conditional can be clearer than a hierarchy plus a factory or registration mechanism. OCP is not a rule that every `if` is a design defect.

**Review cue:** Is the extension axis demonstrated by real requirements, or are we designing for hypothetical future plugins?

### L — Liskov Substitution: honest reservation contracts

**Before:** Consumers of `Reservation` reasonably expect `Confirm()` to work, but one derived type rejects that valid operation.

```csharp
public class Reservation
{
    public virtual string Confirm() => "Confirmed";
}

public sealed class ApprovalRequiredReservation : Reservation
{
    public override string Confirm()
    {
        throw new System.NotSupportedException("Approval is required first.");
    }
}
```

**After:** Expose confirmation only on a type that actually promises it.

```csharp
public interface IConfirmableReservation
{
    string Confirm();
}

public sealed class ImmediateReservation : IConfirmableReservation
{
    public string Confirm() => "Confirmed";
}

public sealed class ApprovalRequiredReservation
{
    public string RequestApproval() => "Approval requested";
}
```

**Tradeoff:** A contract may legitimately declare a capability check or documented exceptional behavior; if so, clients must understand it. The problem above is an *unexpected* rejection of a promised operation. Do not replace every concrete type with an interface just to avoid inheritance.

**Review cue:** Are preconditions, postconditions, invariants, and documented failure modes still valid for every substitute?

### I — Interface Segregation: independent report capabilities

**Before:** An offline report generator is forced to implement an unrelated email operation.

```csharp
public interface IReportOperations
{
    string Generate();
    void Email(string report);
}

public sealed class OfflineReport : IReportOperations
{
    public string Generate() => "Report";

    public void Email(string report)
    {
        throw new System.NotSupportedException("No email capability");
    }
}
```

**After:** Clients ask only for the generation capability. Introduce a separate sending contract **when a real sender and consumer need it**, not speculatively.

```csharp
public interface IReportGenerator
{
    string Generate();
}

public sealed class OfflineReport : IReportGenerator
{
    public string Generate() => "Report";
}
```

**Tradeoff:** Do not split cohesive operations into one-method interfaces simply to maximize interface counts. Segregate when consumers or implementers have materially different capability needs, especially across published API boundaries.

**Review cue:** Does each interface describe a useful consumer-facing contract, or is it an artificial fragment?

### D — Dependency Inversion: registration policy versus file storage

**Before:** A business operation directly chooses its storage mechanism.

```csharp
public sealed class RegistrationService
{
    public void Register(string id)
    {
        if (string.IsNullOrWhiteSpace(id))
        {
            throw new System.ArgumentException("An id is required.", nameof(id));
        }

        System.IO.File.AppendAllText("registrations.txt", id + System.Environment.NewLine);
    }
}
```

**After:** The use case depends on a capability it consumes, and a file adapter implements that contract.

```csharp
public interface IRegistrationStore
{
    void Save(string id);
}

public sealed class RegistrationService
{
    private readonly IRegistrationStore _store;

    public RegistrationService(IRegistrationStore store)
    {
        _store = store ?? throw new System.ArgumentNullException(nameof(store));
    }

    public void Register(string id)
    {
        if (string.IsNullOrWhiteSpace(id))
        {
            throw new System.ArgumentException("An id is required.", nameof(id));
        }

        _store.Save(id);
    }
}

public sealed class FileRegistrationStore : IRegistrationStore
{
    public void Save(string id)
    {
        System.IO.File.AppendAllText("registrations.txt", id + System.Environment.NewLine);
    }
}
```

**Tradeoff:** An interface is useful here because storage is an actual external boundary. It is not necessary between every pair of ordinary cooperating in-memory classes. Constructor injection works without a third-party container; production composition decides which `IRegistrationStore` is supplied. More detailed policy dependency rules belong to the [separate architecture issue](https://github.com/infoconex/dotnet-project-playbook/issues/19), not a second definition here.

**Review cue:** Does the abstraction represent an actual policy-facing capability, with implementation details outside that policy?

## <a name="level-3-deep-dive"></a>Level 3 — Deep dive

When a developer wants a detailed explanation, start from their *actual* change request or a clearly hypothetical scenario, then examine relevant principles rather than repeating five unrelated tutorials. A useful worked sequence for the registration example is:

1. **State observable behavior:** Reject blank identifiers and persist valid registrations. Capture it through the applicable [TDD cycle](standards/engineering-principles.md#std-001-cycle) if executable behavior is being changed.
2. **Identify independent reasons to change:** Registration policy, file formatting, and storage availability may change for different reasons. Avoid splitting an already cohesive validation rule merely to produce smaller classes.
3. **Locate a genuine boundary:** File storage introduces I/O and failures that the registration policy should not dictate. Make the consumed capability explicit; the file implementation can remain in the same assembly until a physical boundary is justified.
4. **Test the promises:** A test double can record the `Save` call for policy behavior. Independently verify the real file adapter where that behavior is materially significant, following [STD-009](standards/testing.md#std-009). A mock-only test does not establish that actual file I/O works.
5. **Reconsider variation honestly:** A second persistent store may justify additional implementations. If it never arrives, there is no reason to build a plugin registry or elaborate service locator.
6. **Review compatibility and exceptions:** A published legacy API or external framework may constrain refactoring. Record real obstacles, evidence, and any Required-standard exception instead of claiming that every alternative is equally compliant.

For deeper discussion of a specific principle, ask questions such as:

| Principle | Useful deep-dive question |
| --- | --- |
| SRP | Which independently changing stakeholders or policies are represented in this type? |
| OCP | What concrete variation must be added, and what would a simpler conditional cost? |
| LSP | Which input, output, invariant, or failure promise would a substitute violate? |
| ISP | Which real consumers need which capabilities, and how will a public interface evolve? |
| DIP | Which policy owns a dependency contract, and how is the real adapter verified? |

An extended review can compare two or three viable designs, their maintenance and test costs, and the smallest change that meets current requirements. This on-demand format is a method for discussion, not a mandate to implement all potential abstractions.

## Verification and compatibility of the examples

- The snippets intentionally avoid modern-only syntax such as records, file-scoped namespaces, primary constructors, and default interface methods. They illustrate C# 7.3-compatible language constructs; the target project's actual toolchain still controls compilation.
- Example names and supporting concerns are simplified for teaching. They do not validate a generated project, production persistence, performance, or cross-platform operation.
- Assess actual implementations through the [STD-010 review contract](standards/solid.md#verification-and-limits), relevant behavioral tests, and appropriately scoped real-boundary evidence. No documentation example alone proves architectural compliance.
