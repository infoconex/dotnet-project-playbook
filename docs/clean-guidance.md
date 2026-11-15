# Clean Architecture: on-demand C# guidance

This is an **illustrative guide**, not a second normative standard. [STD-013 — Clean Architecture](standards/clean.md#std-013) defines the Recommended adoption choice and its protected Application Core. [STD-011](standards/dependency-direction.md#std-011) independently protects business policy even when Clean Architecture is not selected; [STD-012](standards/hexagonal.md#std-012) defines explicit ports when Hexagonal Architecture is adopted. [STD-003](standards/engineering-principles.md#std-003) keeps separate compiled projects Optional.

Offer these levels only when a project needs more detail; ordinary AI-guided adoption should assess actual dependencies without requiring an architecture tutorial or a prescribed project graph:

1. [Level 1 — Quick boundary refresher](#level-1-quick-boundary-refresher): distinguish core responsibilities, source dependencies, runtime execution, and composition.
2. [Level 2 — C# and dependency examples](#level-2-c-and-dependency-examples): a dependency-rich application, a concrete-coupling violation, and cases needing less architecture.
3. [Level 3 — Review, testing, and migration](#level-3-review-testing-and-migration): evidence for changed boundaries, actual project references, and incremental adoption.

Code excerpts use features available in C# 7.3 to make the *language syntax* more approachable to traditional .NET Framework projects. They are **illustrative excerpts, not a compiled solution, validated SQL integration, or published template**. Actual compatibility depends on the chosen references, compiler, runtime, provider, and environment; production types would ordinarily be in separate files. No command, test, or CI result is asserted by these examples.

## <a name="level-1-quick-boundary-refresher"></a>Level 1 — Quick boundary refresher

Ask **which application behavior must remain independent of an external mechanism?** Then identify the core and the concrete mechanisms outside it. A typical Clean Architecture design separates domain policy from application use cases and keeps *both* independent of infrastructure and presentation, while the outer host constructs the actual implementation graph.

| Responsibility | Example | Key boundary |
| --- | --- | --- |
| Domain | Rule deciding whether an order may be approved | No knowledge of application orchestration, SQL, UI, or host |
| Application Core | Use case that obtains facts and invokes the rule | Uses consumer-oriented external capability contracts, not database implementations |
| Infrastructure | SQL implementation of the fact lookup | Implements a core-owned contract and knows SQL/provider details |
| Presentation | CLI or HTTP endpoint that accepts a request | Calls the use case; does not reimplement the approval rule |
| Composition root | Entry point that creates/wires dependencies | May deliberately reference both core and concrete adapters |

The apparent contradiction is resolved by separating **compile-time knowledge** from **runtime execution**:

- **Source dependencies:** The application use case knows an inward interface; the SQL adapter knows and implements that interface. The core does not need a reference to the SQL adapter.
- **Runtime calls:** A CLI can invoke the use case, which calls the interface, whose SQL implementation executes a query. Runtime execution crosses outward even though source dependencies do not.
- **Composition:** The outer root references both sides to make the runtime chain possible. This is an allowed composition exception, not an infrastructure dependency from the core.

The same architecture can live in one assembly with reviewed logical boundaries, or use multiple projects for compiler-enforced references. **Namespaces and folders organize code but do not enforce reference direction.** Clean Architecture is an internal organization choice, not a requirement to deploy microservices or separate processes.

## <a name="level-2-c-and-dependency-examples"></a>Level 2 — C# and dependency examples

### Example: a real external dependency behind an inward contract

Suppose an order-approval use case needs the unpaid-invoice count from a database. The business rule is that fewer than three unpaid invoices permits approval. The example separates **the business decision**, **use-case orchestration**, **the SQL implementation**, **the caller**, and **composition**.

**Domain — independently testable rule:**

```csharp
public sealed class OrderApprovalRule
{
    public bool CanApprove(int unpaidInvoiceCount)
    {
        return unpaidInvoiceCount < 3;
    }
}
```

**Application Core — the consuming contract and use case:**

```csharp
using System;

public interface IUnpaidInvoiceCount
{
    int ForCustomer(Guid customerId);
}

public sealed class CheckOrderApproval
{
    private readonly IUnpaidInvoiceCount _invoiceCount;
    private readonly OrderApprovalRule _rule;

    public CheckOrderApproval(
        IUnpaidInvoiceCount invoiceCount,
        OrderApprovalRule rule)
    {
        _invoiceCount = invoiceCount ?? throw new ArgumentNullException(nameof(invoiceCount));
        _rule = rule ?? throw new ArgumentNullException(nameof(rule));
    }

    public bool Execute(Guid customerId)
    {
        int unpaidCount = _invoiceCount.ForCustomer(customerId);
        return _rule.CanApprove(unpaidCount);
    }
}
```

The core contract describes the fact the use case needs, not a SQL query, connection, or provider-specific return type. The example uses an interface because a genuine external capability crosses the boundary. This does **not** imply an interface is required for `OrderApprovalRule`, `CheckOrderApproval`, or every other internal class. If the project also adopts Hexagonal Architecture, [STD-012](standards/hexagonal.md#std-012) additionally requires explicit interfaces for *identified inbound ports*.

**Infrastructure — an outward adapter:**

```csharp
using System;
using System.Data.Common;
using System.Globalization;

public sealed class SqlUnpaidInvoiceCount : IUnpaidInvoiceCount
{
    private readonly DbConnection _connection;

    public SqlUnpaidInvoiceCount(DbConnection connection)
    {
        _connection = connection ?? throw new ArgumentNullException(nameof(connection));
    }

    public int ForCustomer(Guid customerId)
    {
        using (DbCommand command = _connection.CreateCommand())
        {
            command.CommandText =
                "SELECT COUNT(*) FROM Invoices " +
                "WHERE CustomerId = @customerId AND Paid = 0";

            DbParameter parameter = command.CreateParameter();
            parameter.ParameterName = "@customerId";
            parameter.Value = customerId;
            command.Parameters.Add(parameter);

            return Convert.ToInt32(
                command.ExecuteScalar(), CultureInfo.InvariantCulture);
        }
    }
}
```

The connection is assumed to have been supplied and opened by the host; the abbreviated sample does not establish schema correctness, provider parameter conventions, connection ownership, transaction scope, cancellation, failure handling, or production security. Those need separate design and actual [representative adapter verification under STD-009](standards/testing.md#std-009) where applicable. A fake used for the core cannot prove the SQL query works.

**Presentation — one possible CLI-facing caller:**

```csharp
using System;

public sealed class ApprovalCommand
{
    private readonly CheckOrderApproval _check;

    public ApprovalCommand(CheckOrderApproval check)
    {
        _check = check ?? throw new ArgumentNullException(nameof(check));
    }

    public string Run(Guid customerId)
    {
        return _check.Execute(customerId) ? "Approved" : "Not approved";
    }
}
```

This caller references the concrete *application use-case class*, which is within the core; Clean Architecture alone does not require a separate inbound interface. It does not depend on the concrete SQL adapter. If this invocation is identified as a Hexagonal inbound port in a project also adopting STD-012, introduce its required explicit interface.

**Outer composition — manual wiring is sufficient:**

```csharp
using System.Data.Common;

public static class ApplicationComposition
{
    public static ApprovalCommand Create(DbConnection openConnection)
    {
        IUnpaidInvoiceCount count =
            new SqlUnpaidInvoiceCount(openConnection);
        var useCase = new CheckOrderApproval(count, new OrderApprovalRule());

        return new ApprovalCommand(useCase);
    }
}
```

Only the **outer** composition code knows the SQL implementation and the Application Core together. A modern ASP.NET Core host might register equivalent dependencies with its supported DI container; a traditional .NET Framework host might use a manual factory. Neither approach establishes runtime success without exercising the actual composition and adapter.

### Counterexample: concrete infrastructure inside the Application Core

The following illustrates a **core-wide STD-013 violation** if it is placed in the declared Application Core:

```csharp
using System;
using System.Data.Common;

public sealed class CheckOrderApproval
{
    private readonly SqlUnpaidInvoiceCount _database;

    public CheckOrderApproval(DbConnection connection)
    {
        _database = new SqlUnpaidInvoiceCount(connection);
    }

    public bool Execute(Guid customerId)
    {
        return _database.ForCustomer(customerId) < 3;
    }
}
```

It directly names and constructs an infrastructure implementation and requires a database connection to create the use case. It also mixes a business limit with provider coupling, violating independently [Required STD-011](standards/dependency-direction.md#std-011). Even if the business rule were moved into a separate domain type, an Application Core use case that still directly referenced `SqlUnpaidInvoiceCount` would fail the adopted Clean Architecture boundary. Rename-only layers or adding an interface implemented by the concrete provider but owned by Infrastructure would not fix that source dependency.

### Alternatives with fewer layers or projects

| Project context | Proportional arrangement | Why it can be appropriate |
| --- | --- | --- |
| Pure calculation or domain class library | Domain classes, focused tests, no artificial application/infrastructure/presentation components | No meaningful external capability or hosted use-case boundary exists |
| Small single-project application with a meaningful boundary | Logical Domain, Application, Infrastructure, and entry-point responsibilities in one assembly; manual source review | Protects the selected core without forcing another compiled project |
| Growing application with multiple external integrations | Distinct Core and Infrastructure assemblies, plus host or presentation as justified | Project references can make some forbidden dependencies fail compilation |
| Trivial technical file-copy or CSV-save job without business decisions | Direct technical collaboration, perhaps no Clean Architecture adoption | A forwarding abstraction may cost more than the isolation provides; still evaluate security and test needs independently |

**Example of technical collaboration outside a protected core:**

```csharp
using System.IO;

public sealed class PreparedCsvSaveJob
{
    public void Save(string path, string preparedCsv)
    {
        File.WriteAllText(path, preparedCsv);
    }
}
```

This excerpt contains no business decision about whose data is exportable or how values are computed. It does not need an interface solely to satisfy Clean Architecture if the system has not chosen that pattern for the operation, or if it stays outside an adopted core. The excerpt does not establish safe path handling, authorization, or reliable filesystem behavior.

## <a name="level-3-review-testing-and-migration"></a>Level 3 — Review, testing, and migration

### Review sequence

1. **Identify the claim:** Is Clean Architecture actually adopted, and for which scope? If not, apply independently Required standards without inventing a Clean Architecture compliance failure.
2. **Find responsibilities:** Locate domain invariants, application use cases, genuinely technical orchestration, transport translation, external providers, and composition. Names like `Core`, `Service`, and `Adapter` are clues, not proof.
3. **Trace source knowledge:** Check whether core code names an infrastructure assembly/type, framework-specific data model, controller, or container API, including through a supposedly neutral contract. Distinguish runtime invocation through an abstraction from source dependency on implementation.
4. **Inspect physical enforcement:** Where separate projects exist, review project references and imports; where code shares an assembly, inspect logical source edges and focused tests. A namespace boundary has no compiler protection.
5. **Verify real behavior:** Test meaningful application behavior with controlled substitutes, significant composition wiring with the actual host, and material external adapters with representative real dependencies or validated contracts when STD-009 applies. Retain TDD evidence where behavior changed.
6. **Record the actual result:** Identify revision, affected boundaries, relevant source references, commands/results actually run, manual judgments, justified simpler alternatives or reviewed deviations, and what remains unknown.

### Example inspection commands (not executed by this guide)

```text
rg 'ProjectReference' --glob '*.csproj'
rg 'using (Microsoft\.Data\.SqlClient|System\.Data\.SqlClient|Microsoft\.AspNetCore)' --glob '*.cs'
```

These are starting points, not a verifier shipped by this repository. Imports may be aliased, fully qualified, generated, or hidden by reflection; a match may belong in composition or another outer role; an absent match does not establish a clean core. Inspect the project's actual reference graph and code. Traditional non-SDK `.csproj` files use different XML surroundings from modern SDK-style projects; an SDK-only command or architecture-testing package is not universally applicable.

### What tests can and cannot establish

- **Core test:** A controlled `IUnpaidInvoiceCount` returning 2 or 3 can exercise the `CheckOrderApproval` rule and boundary without a database. This demonstrates behavior for supplied facts, not SQL correctness or runtime wiring.
- **Composition check:** Starting or constructing the real host can reveal missing registrations, incompatible lifetimes, or failed construction. It cannot by itself prove every business use case or external dependency works.
- **Real adapter check:** A representative provider environment or validated contract can establish SQL lookup behavior for exercised cases, not untested providers, schemas, or operating systems.
- **Architecture/reference check:** Can identify a specific forbidden compile-time edge when an enforcement boundary exists. It cannot determine whether the use case is truly policy-free, whether abstractions are well designed, or whether a successful build proves architecture quality.

No runnable test fixture or integration environment accompanies these snippets. [STD-001](standards/engineering-principles.md#std-001) controls test-first development; [STD-009](standards/testing.md#std-009) controls significant external-adapter evidence and reviewed exceptions. Avoid inventing a passing test count, code coverage, platform result, or CI run.

### Incremental legacy adoption

For a traditional .NET Framework application with a controller that directly computes approval decisions and queries SQL, first capture relevant existing behavior where feasible. Extract a technology-neutral rule and application-facing capability contract for the changed decision, move the concrete lookup to an outer implementation, and compose it at the existing entry point. Preserve public signatures or introduce an explicit compatibility migration when necessary. A separate Domain/Application assembly may help later but is not a prerequisite to a useful logical boundary.

If unchanged legacy areas remain tightly coupled, state the adopted scope precisely instead of claiming the entire repository now follows Clean Architecture. An actual remaining business-policy violation needs the documented [STD-011 reviewed exception](standards/dependency-direction.md#std-011); choosing a simpler architecture alone does not exempt it.

## Microsoft guidance and further reading

- [Common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) — protected Application Core, composition, and the distinction between compile-time and runtime arrows.
- [Architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles) — separation of concerns, explicit dependencies, and inversion.
- [Microservice application layer implementation](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-application-layer-implementation-web-api) — valid alternative organizational examples, which do not automatically claim Clean Architecture compliance.

The [authoritative STD-013](standards/clean.md#std-013), not this guide or an external template, defines adoption and compliance expectations.
