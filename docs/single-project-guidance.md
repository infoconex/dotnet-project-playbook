# Proportionate single-project architecture: on-demand .NET guidance

Use the simplest architecture that satisfies actual requirements while retaining sound engineering principles. A cohesive library or small application may have **one production project** and a separate test project without adopting a multi-project layering scheme.

This is **illustrative implementation guidance, not a new normative standard, executable template, or verified project**. The authoritative rules remain [Optional STD-003 — Separate compiled projects](standards/engineering-principles.md#std-003), [Required STD-010 — SOLID](standards/solid.md#std-010), [Required STD-011 — Business-policy dependency direction](standards/dependency-direction.md#std-011), and the independently [Recommended STD-012 — Hexagonal](standards/hexagonal.md#std-012) and [Recommended STD-013 — Clean](standards/clean.md#std-013) styles when adopted. [STD-001](standards/engineering-principles.md#std-001) and conditional [STD-009](standards/testing.md#std-009) govern relevant testing. Issue #22 established that no **single-project-specific** standard was warranted. Separately, [STD-014](standards/ddd.md#std-014) addresses conditional Domain-Driven Design and domain-model fidelity; it does not change any single-project rule or require more compiled projects.

The sections are optional levels of explanation, not an automated assessment or a required checklist.

## Level 1 — Choose the simplest adequate shape

Start with actual responsibilities, dependencies, testing needs, and constraints, not a prescribed number of projects.

| Project context | Practical starting point | Reconsider when |
| --- | --- | --- |
| Small pure library (calculations, parsing, domain rules) | One production class library, plus a test project when appropriate; cohesive types with direct collaborators | Independently reusable components or meaningful dependency-enforcement needs emerge |
| Small CLI, worker, or application with limited integration | One production project can organize entry point, behavior, and technical code by responsibility | Policy begins to depend on concrete mechanisms, tests require real infrastructure unnecessarily, or integration complexity grows |
| Dependency-rich application | Logical policy, use-case, adapter, transport, and composition boundaries; consider separate compiled projects where they enforce important rules | Independent release, reuse, ownership, enforcement, or more complex external-adapter behavior makes physical separation valuable |
| Existing .NET Framework application | Preserve functioning project format, public contracts, and build constraints; improve affected logical boundaries incrementally | A focused extraction produces a measurable compatibility, testability, or dependency benefit |

These are **starting considerations**, not a rule that all small applications must have one project or that every database integration must create multiple assemblies. A small application with a meaningful external dependency can still use one compiled project and correctly isolate business decisions. Conversely, a compact but independently distributed component may justify multiple projects.

Microsoft's [common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) describes both all-in-one applications and the advantages and costs of evolving to multiple projects.

### Keep project count, logical structure, and deployment separate

| Term | What it identifies | What it does *not* prove |
| --- | --- | --- |
| Solution/repository | A development grouping of projects and files | A runtime application or deployment boundary |
| Compiled project / assembly | A build unit and generally its principal assembly output; project references can enforce assembly-level dependency restrictions | A deployment unit, a required architectural layer, or sound responsibility placement |
| Logical responsibility boundary | Separation of domain decisions, use cases, entry-point translation, composition, and integrations in source organization | Compiler enforcement merely because it has a folder or namespace |
| Test project | Independently compiled test code referencing production behavior when the chosen tooling supports it | An additional **production** layer |
| Deployment unit | The application and required artifacts deployed/released together | The number of compiled projects used to build it |

A solution can contain three production libraries/projects and still ship one application deployment. A project can also be built as part of more than one distribution workflow; neither source project count nor assembly count alone determines deployment topology. Microsoft distinguishes *logical layers* from *physical deployment tiers* in its [architecture discussion](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures).

## Level 2 — Worked project-shape examples

### Example A: a small pure-library rule

An illustrative source layout is:

```text
PriceRules/
  src/
    PriceRules/
      PriceRules.csproj
      DiscountPolicy.cs
  tests/
    PriceRules.Tests/
      PriceRules.Tests.csproj
      DiscountPolicyTests.cs
```

There is **one production project** (`PriceRules.csproj`). The test project references that project. There is no database, network adapter, composition root, Domain project, Application project, artificial repository interface, or DI container.

```csharp
// DiscountPolicy.cs — illustrative C# 7.3-compatible syntax.
using System;

namespace PriceRules
{
    public sealed class DiscountPolicy
    {
        public decimal Apply(decimal price, decimal discountRate)
        {
            if (price < 0m)
                throw new ArgumentOutOfRangeException(nameof(price));
            if (discountRate < 0m || discountRate > 1m)
                throw new ArgumentOutOfRangeException(nameof(discountRate));

            return price * (1m - discountRate);
        }
    }
}
```

An illustrative NUnit test exercises the behavior directly:

```csharp
// DiscountPolicyTests.cs — illustrative test excerpt.
using NUnit.Framework;
using PriceRules;

namespace PriceRules.Tests
{
    [TestFixture]
    public sealed class DiscountPolicyTests
    {
        [Test]
        public void Apply_ValidDiscount_ReturnsDiscountedPrice()
        {
            var policy = new DiscountPolicy();

            Assert.That(policy.Apply(100m, 0.15m), Is.EqualTo(85m));
        }

        [Test]
        public void Apply_NegativePrice_IsRejected()
        {
            var policy = new DiscountPolicy();

            Assert.Throws<System.ArgumentOutOfRangeException>(
                () => policy.Apply(-1m, 0.15m));
        }
    }
}
```

This arrangement keeps the rule independent of infrastructure and testable without substitutes. Introducing `IDiscountPolicy` solely because one concrete rule is used once would not, by itself, demonstrate better SOLID design. Add a meaningful abstraction if a real consumer, extension, or substitution need appears; retain any applicable contract design obligations from [STD-010](standards/solid.md#std-010) and [STD-011](standards/dependency-direction.md#std-011).

The excerpts omit real `.csproj` contents, test package versions, target frameworks, and runner configuration. They are **not compiled or executed examples**. The [testing guide's pure-library example](testing-guidance.md#example-a--a-pure-c-library) discusses scenario selection and why isolated tests are useful. [STD-001](standards/engineering-principles.md#std-001) still requires test-first behavior for applicable changes; a displayed passing-looking test cannot prove TDD chronology.

### Example B: an application with real external dependencies

Consider an order API coordinating business approval rules, SQL persistence, and HTTP endpoints. A team may begin with one production project containing logically distinct `Domain/`, `Application/`, `Infrastructure/`, and `Transport/` code *if the boundaries remain understandable and correct*. Folder names alone do not prevent domain logic from importing a SQL provider.

If concrete dependencies and complexity warrant stronger compiled separation, an **illustrative** shape is:

```text
OrderService/
  src/
    OrderCore/                   # Domain rules, use cases, inward contracts
    OrderInfrastructure/         # SQL and external-system implementations
    OrderApi/                    # HTTP host, translation, composition
  tests/
    OrderCore.Tests/             # Independent use-case/policy tests
    OrderInfrastructure.Tests/   # Representative adapter verification
```

Example compile-time references:

- `OrderInfrastructure → OrderCore`: outer implementations depend on inward contracts.
- `OrderApi → OrderCore + OrderInfrastructure`: host composition knows contracts and implementations.
- `OrderCore` has **no compile-time reference** to `OrderInfrastructure` or `OrderApi`.
- `OrderCore.Tests → OrderCore`; adapter tests reference only the production artifacts they need.

The API, core, and infrastructure assemblies can **still be deployed together as one application**; creating multiple projects is not automatically microservices or multiple deployment units.

When **Clean Architecture** is selected, its core-wide dependency rule applies even if all roles initially reside in one assembly. When **Hexagonal Architecture** is selected, every identified inbound and outbound port has the explicit interface required by [STD-012](standards/hexagonal.md#std-012). Neither style is automatically adopted just because a folder resembles a layer. See the [Clean Architecture guide](clean-guidance.md) and [Hexagonal guide](hexagonal-guidance.md) for worked boundary examples.

A technical coordinator with no business policy may reasonably depend on a concrete technical implementation under [STD-011](standards/dependency-direction.md#std-011). Business decisions themselves must not depend on concrete SQL clients, controllers, or provider-specific types. A host may construct or register concrete implementations at an outer composition boundary. For significant adapter behavior, [STD-009](standards/testing.md#std-009) requires representative real-dependency or appropriately validated contract evidence when its applicability trigger is met.

### Interfaces, construction, and dependency injection

- **Pure or trivial collaborators:** Prefer ordinary constructors, method calls, and cohesive concrete types when no meaningful substitute, external capability, or behavioral variation exists. A new interface is not a scorecard item.
- **Actual external capability used by policy:** Put a small, technology-neutral consumer contract inward; keep the concrete implementation and vendor types outward. This can be done inside one assembly using source-level boundaries, although project references will not enforce it there.
- **Composition:** Manual construction can be enough for a small library/CLI. For a host with lifetimes or many registrations, its supported built-in DI facilities may be useful. A third-party container and mandatory `IServiceCollection` pattern are not prerequisites for all .NET targets.
- **Adopted architectural style:** Do not use simplicity to silently waive [STD-012's](standards/hexagonal.md#std-012) explicit interfaces for actual hexagonal ports or [STD-013's](standards/clean.md#std-013) core boundary. A documented simpler alternative remains possible without claiming to adopt either style.

Microsoft's [architectural principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles) address separation of concerns, explicit dependencies, and dependency inversion. Its [dependency injection guidelines](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines) apply when services and DI composition are used; they do not require every pure class library to install a container.

## Level 3 — Reassess, verify, and migrate proportionately

### When physical project separation adds real value

Look for observable signals, not an arbitrary count of files, classes, or developers:

1. A significant policy-to-infrastructure dependency keeps recurring despite logical separation, and a separate core assembly would enable useful compiler-enforced restrictions.
2. Tests for important business behavior routinely require the host, database, network, or unrelated integration code to execute.
3. A component genuinely needs independent reuse, distribution, ownership, compatibility management, or controlled visibility.
4. Changes repeatedly ripple across unrelated responsibilities, and source-level encapsulation is no longer sufficient.
5. The dependency graph or composition is complex enough that meaningful boundaries can be more easily reviewed and enforced with project references.

First consider a focused responsibility refactor or improved source-level boundary. Physical separation has costs: more project files and references, API surface decisions, build configuration, dependency/version management, and migration risk. It is useful when the benefit outweighs those costs; [STD-003](standards/engineering-principles.md#std-003) remains **Optional**.

### Review the actual code and evidence

For a new or materially changed design, perform only checks supported by its risks and actual tooling:

1. **Name responsibilities and dependency risks.** Identify business decisions, stable collaborators, external adapters, entry points, and composition. Locate any provider-specific imports inside policy code.
2. **Inspect physical references where present.** Examine `ProjectReference` relationships or project metadata for forbidden edges if the chosen design depends on compiled enforcement. In a single assembly, inspect source dependencies and actual type usage instead; folders cannot enforce direction.
3. **Exercise meaningful behavior independently.** Use focused tests of pure rules or application behavior with controlled substitutes only for real external capabilities. Follow [STD-001](standards/engineering-principles.md#std-001); don't add a mock solely to satisfy a perceived architectural quota.
4. **Check real boundaries when required.** Verify significant changed adapter behavior under [STD-009](standards/testing.md#std-009); test material composition paths when changing application wiring. Apply additional adopted Hexagonal/Clean verification requirements according to their own standards.
5. **Report evidence honestly.** Record the exact revision, examined paths, actually run commands and results, tool/target versions where relevant, assumptions, unresolved semantic judgments, and unverified paths. A build, a clean import scan, or many unit tests alone do not prove separation of concerns.

No specific analyzer, CI architecture gate, per-interface test, or project-count threshold is prescribed here. For **documentation-only** changes, review the source claims, sample plausibility, links, and consistency; that is not evidence of sample compilation or framework compatibility.

### Modern .NET and traditional .NET Framework

The architectural choices are independent of SDK-style versus traditional project format. However, implementation and verification are not automatically interchangeable:

- **Modern SDK-style .NET:** Use the actual installed SDK, target framework, test adapter/platform, and host features. `dotnet build` and `dotnet test` may be appropriate, depending on the test platform and project configuration.
- **Traditional non-SDK .NET Framework:** Existing `.csproj` files, reference formats, package management, and Windows/MSBuild tooling may differ. Use the installed compatible MSBuild/Visual Studio toolchain and an appropriate test runner; do not copy SDK-only project XML or assume a modern `dotnet test` invocation works.
- **Language syntax:** The C# excerpts above intentionally avoid features newer than C# 7.3, but language syntax compatibility does **not** establish successful compilation, dependency compatibility, runtime support, or platform support.
- **Existing code:** Preserve public contracts and characterize affected behavior where feasible. Move the smallest meaningful policy decision away from concrete mechanisms first, then decide whether a physical split provides additional value. There is no universal requirement to rewrite an existing application into several projects.

See Microsoft's [SDK project overview](https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview), [.NET Framework porting discussion](https://learn.microsoft.com/en-us/dotnet/core/porting/framework-overview), and [test platform guidance](https://learn.microsoft.com/en-us/dotnet/core/testing/test-platforms-overview), together with the [playbook's version-aware testing guide](testing-guidance.md#version-aware-execution-and-verification).

## How this guidance relates to other architecture choices

| Authority | What remains independently assessable |
| --- | --- |
| [STD-003](standards/engineering-principles.md#std-003) | Separate compiled projects are Optional, selected by real boundaries |
| [STD-010](standards/solid.md#std-010) | SOLID remains Required without an interface-per-class mandate |
| [STD-011](standards/dependency-direction.md#std-011) | Business-policy independence remains Required in one or many assemblies |
| [STD-012](standards/hexagonal.md#std-012) | Recommended Hexagonal adoption; explicit interfaces for identified ports if adopted |
| [STD-013](standards/clean.md#std-013) | Recommended Clean adoption; protect the entire logical Application Core if adopted |
| [STD-001](standards/engineering-principles.md#std-001), [STD-009](standards/testing.md#std-009) | Test-first changes and conditional external-boundary evidence |

This guide explains **when less architectural machinery is appropriate**. It grants no exception to a Required standard, creates no new applicability level, and does not relabel an unadopted architecture as compliant with its optional pattern-specific rules. See [standards governance](governance/standards.md) for authority, applicability, and exceptions.
