# Business-policy dependency direction: on-demand C# guidance

This is an **illustrative guide**, not a second normative standard. The [Required STD-011](standards/dependency-direction.md#std-011) defines applicability, exceptions, and the business-policy independence rule. [STD-010 — SOLID](standards/solid.md#std-010) addresses Dependency Inversion as part of object design, while [STD-003](standards/engineering-principles.md#std-003) leaves separate compiled projects Optional.

During ordinary new-repository setup or assessment, assume developers understand the basic architectural concepts. **Do not require an architecture tutorial or a five-layer interview.** Offer the following detail only when requested, or answer a specific question directly:

1. [**Level 1 — Quick boundary refresher**](#level-1-quick-boundary-refresher): who owns policy, what may depend on what, and when to introduce a port.
2. [**Level 2 — C# and project-reference examples**](#level-2-c-and-project-reference-examples): before/after policy code, an adapter, thin orchestration, and composition.
3. [**Level 3 — Review and verification**](#level-3-review-and-verification): how to evaluate actual repositories, including legacy constraints and what cannot be proved by a static check.

These levels are documentation and conversational options, **not a shipped interactive agent, analyzer, or project generator**. Examples use C# syntax available in C# 7.3, without assuming that a specific .NET Framework or modern .NET project will build until its actual references and toolchain are checked. Separate code blocks are illustrative excerpts, not one ready-to-run solution or tested database integration. Production types would ordinarily live in their own files.

## <a name="level-1-quick-boundary-refresher"></a>Level 1 — Quick boundary refresher

Ask two questions first:

1. **Where is the business decision?** A domain object, an application use case, or even a command handler might enforce a business limit or invariant. Its name or physical assembly does not decide whether it is policy.
2. **What does the decision know about the outside world?** Needing a customer's outstanding-invoice count is a business-relevant capability; knowing the SQL driver, UI controller, file layout, or host's lifetime to obtain that count is a technical coupling.

| Relationship | Interpretation |
| --- | --- |
| Policy → neutral domain types and relevant consumer-oriented contracts | Appropriate when the policy truly needs those collaborators. |
| Database/file/network adapter → policy-owned contract | Appropriate when an external mechanism supplies a policy-needed capability. |
| Presentation → use case or application entry point | Appropriate for translating requests and formatting responses. |
| Composition root → policy contracts **and** concrete adapters | Appropriate for selecting and connecting implementations. |
| Business-policy code → concrete SQL client, UI control, host container, or storage format | A violation when the mechanism is required to express/evaluate the business decision; assess any justified exception explicitly. |
| Thin technical orchestration → concrete infrastructure | Potentially appropriate if it does not decide or encode business rules. |

In Clean Architecture, an Application Core is commonly kept entirely independent of infrastructure; in other Microsoft examples, application-layer command handlers coordinate infrastructure directly while the domain model remains independent. [STD-011](standards/dependency-direction.md#std-011) deliberately protects *business policy by responsibility* in both settings instead of requiring one assembly structure. See Microsoft's [Clean Architecture discussion](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) and [DDD application-layer implementation](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-application-layer-implementation-web-api).

## <a name="level-2-c-and-project-reference-examples"></a>Level 2 — C# and project-reference examples

### Business policy coupled to a database mechanism

**Problematic excerpt:** The business decision needs the database connection and query shape to determine its outcome. This is not merely a command handler transporting a request; it contains the business rule itself.

```csharp
using System;
using System.Data.Common;
using System.Globalization;

public sealed class OrderApprovalPolicy
{
    private readonly DbConnection _connection;

    public OrderApprovalPolicy(DbConnection connection)
    {
        _connection = connection;
    }

    public bool CanApprove(Guid customerId)
    {
        using (DbCommand command = _connection.CreateCommand())
        {
            command.CommandText =
                "SELECT COUNT(*) FROM Invoices " +
                "WHERE CustomerId = @customerId AND IsPaid = 0";

            DbParameter parameter = command.CreateParameter();
            parameter.ParameterName = "@customerId";
            parameter.Value = customerId;
            command.Parameters.Add(parameter);

            int unpaidCount = Convert.ToInt32(
                command.ExecuteScalar(), CultureInfo.InvariantCulture);
            return unpaidCount < 3; // Business rule mixed with SQL.
        }
    }
}
```

This code assumes an already-open connection and a compatible database schema; it is a coupling illustration, **not a validated query or production provider example**. Parameterization avoids one unrelated flaw but does not solve policy independence.

### Policy contract with an outer adapter

**Policy-side excerpt:** The business decision depends on the outcome it needs, not a database provider or query language. The contract belongs with the consumer's policy boundary; it need not become a universal shared-repository library.

```csharp
using System;

public interface IOutstandingInvoiceCount
{
    int ForCustomer(Guid customerId);
}

public sealed class OrderApprovalPolicy
{
    private readonly IOutstandingInvoiceCount _invoiceCount;

    public OrderApprovalPolicy(IOutstandingInvoiceCount invoiceCount)
    {
        _invoiceCount = invoiceCount;
    }

    public bool CanApprove(Guid customerId)
    {
        return _invoiceCount.ForCustomer(customerId) < 3;
    }
}
```

**Adapter-side excerpt:** The technical implementation can use `System.Data.Common` without forcing the policy to know it. An application might supply different implementations for different databases or test environments; do not create alternatives without a real need.

```csharp
using System;
using System.Data.Common;
using System.Globalization;

public sealed class DbOutstandingInvoiceCount : IOutstandingInvoiceCount
{
    private readonly DbConnection _connection;

    public DbOutstandingInvoiceCount(DbConnection connection)
    {
        _connection = connection;
    }

    public int ForCustomer(Guid customerId)
    {
        using (DbCommand command = _connection.CreateCommand())
        {
            command.CommandText =
                "SELECT COUNT(*) FROM Invoices " +
                "WHERE CustomerId = @customerId AND IsPaid = 0";

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

**Composition-root excerpt:** An outer host is allowed to depend on both policy and adapter. The host is responsible for creating/configuring an appropriate `DbConnection`; the snippet does not establish connection lifetime, transaction handling, retries, or provider compatibility.

```csharp
using System.Data.Common;

public static class ApplicationComposition
{
    public static OrderApprovalPolicy CreatePolicy(DbConnection connection)
    {
        IOutstandingInvoiceCount count =
            new DbOutstandingInvoiceCount(connection);

        return new OrderApprovalPolicy(count);
    }
}
```

The *runtime call* travels from `OrderApprovalPolicy` through `IOutstandingInvoiceCount` to the database adapter. The *compile-time policy dependency* is on the interface, not on `DbConnection` or the adapter assembly. A DI container is one possible composition mechanism, not a prerequisite.

**Tradeoff:** A port pays for itself when isolating a genuine business decision from an external mechanism. If the consumer has no business-policy responsibility, another abstraction may merely forward methods and increase maintenance. Also, splitting policy from database code does not demonstrate that the SQL adapter is correct: [STD-009](standards/testing.md#std-009) may require representative real-boundary evidence when significant adapter behavior changes.

### Direct concrete dependencies can be appropriate

This coordinator only writes already-prepared CSV content. It has no decision about which customers qualify, what data is permissible, or how business values are calculated:

```csharp
using System.IO;

public sealed class CsvSaveJob
{
    private readonly string _path;

    public CsvSaveJob(string path)
    {
        _path = path;
    }

    public void Save(string preparedCsv)
    {
        File.WriteAllText(_path, preparedCsv);
    }
}
```

An interface such as `ICsvFileWriter` is not required *solely* to satisfy STD-011. If `Save` starts deciding whose records may be exported, those policy decisions need a technology-neutral boundary; if this operation becomes important external-adapter behavior, consider the applicable testing requirements. Security, path validation, error handling, and lifetime management are separate concerns not established by this abbreviated illustration.

### Project references versus logical boundaries

When separate SDK-style assemblies *are useful*, the following excerpt shows one possible reference arrangement, **not** a Required project template:

```xml
<!-- ApplicationPolicy.csproj: depends on technology-neutral Domain. -->
<ItemGroup>
  <ProjectReference Include="../Domain/Domain.csproj" />
</ItemGroup>

<!-- Infrastructure.csproj: implements policy-side contracts. -->
<ItemGroup>
  <ProjectReference Include="../ApplicationPolicy/ApplicationPolicy.csproj" />
</ItemGroup>

<!-- Host.csproj: composition references both sides. -->
<ItemGroup>
  <ProjectReference Include="../ApplicationPolicy/ApplicationPolicy.csproj" />
  <ProjectReference Include="../Infrastructure/Infrastructure.csproj" />
</ItemGroup>
```

`Domain` can have no project references. An application assembly containing only technical orchestration might refer directly to infrastructure under the approved responsibility-based rule, so **do not infer a violation from a project name alone**. Conversely, putting domain policy in the same assembly as the SQL adapter does not make its coupling acceptable. A traditional non-SDK .NET Framework `.csproj` has a different surrounding XML structure and may include project identifiers/names for references; inspect its actual format rather than copying an SDK-style skeleton. A folder boundary provides organization but no compiler-enforced dependency direction.

## <a name="level-3-review-and-verification"></a>Level 3 — Review and verification

### Suggested review sequence

1. **Find the rules:** Which types enforce eligibility, limits, calculations, invariants, permissions, or other business outcomes? Search beyond `Domain` namespaces; application handlers, controllers, and background jobs can contain policy.
2. **Trace the required knowledge:** Does the rule depend on a business fact/contract, or must it instantiate/configure a concrete client or know a transport/storage format? Are application-level DTOs accidentally provider-specific?
3. **Classify technical collaborators:** Is this code merely orchestrating infrastructure, or making a decision? A type called `Adapter` can still contain policy; a type called `Service` may be entirely technical.
4. **Check compilation boundaries:** If distinct assemblies exist, inspect `.csproj`/solution references and source imports. If there is one assembly, examine logical dependencies and tests; `namespace` naming is not an enforced boundary.
5. **Review changes and exceptions:** Identify the affected rule, existing compatibility surfaces, feasible incremental separation, actual tests, and any documented exception. Do not require a whole-repository redesign for a narrowly scoped legacy change.

### Illustrative checks and their limits

On a repository with PowerShell, Bash, or another shell, basic source/references inspection can start with:

```text
rg 'ProjectReference' --glob '*.csproj'
rg 'using (Microsoft\.Data\.SqlClient|System\.Data\.SqlClient|Microsoft\.AspNetCore)' --glob '*.cs'
```

These are **inspection examples only**: `rg` is not installed by this playbook, matches are neither complete dependency graphs nor proof of a violation, and aliases, global imports, reflection, generated code, and same-assembly design can escape such searches. Check the actual build graph using tooling already supported by the target project if that adds value. No single static or build check can determine whether business policy was coupled semantically.

When executable behavior changes, [STD-001](standards/engineering-principles.md#std-001) governs test-first development; [STD-009](standards/testing.md#std-009) supplies additional external-boundary evidence when its trigger applies. For this documentation-only guide, manually check navigation, consistency, syntax as far as possible, and honesty about unverified behavior; do not invent a passing compilation or provider test.

### Existing code and exceptions

An older .NET Framework application might have a single project, legacy non-SDK references, and an application service that contains SQL plus a business limit. The independent rule still matters, but a compatible migration might first extract the pure limit decision behind an interface or value supplied by existing orchestration, retain the public service signature, characterize behavior, and then decide if a physical project split is worthwhile. If a real policy-to-infrastructure dependency must remain temporarily, document the affected boundary, concrete obstacle, alternative evidence, residual risk, and reviewable follow-up under [standards governance](governance/standards.md#applicability-levels).

An unchanged legacy area is not automatically subjected to a speculative rewrite. Nor should an existing design be declared compliant merely because an interface was introduced. Evaluate actual responsibilities and observed tests.

## Microsoft guidance and neighboring standards

- [Microsoft's .NET architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles) explain dependency inversion and separation of concerns.
- [Common application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) describe Clean Architecture's compile-time direction and runtime composition.
- [DDD-oriented microservice](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice) discusses domain-model independence.
- [Microservice application layer implementation](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-application-layer-implementation-web-api) illustrates orchestration that may interact with infrastructure.

This guidance neither establishes a new requirement for Clean Architecture, Hexagonal Architecture, or DDD nor preempts the separate planning issues for those standards. The [authoritative STD-011](standards/dependency-direction.md#std-011) remains the sole definition of the playbook's Required policy-independence obligation.
