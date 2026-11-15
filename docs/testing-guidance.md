# Applying Microsoft's .NET testing guidance

Microsoft's published testing documentation is the primary technical reference for .NET projects using this playbook. This guide explains how to select tests and interpret their evidence; it is **not a second normative testing rulebook**. The existing [Required TDD standard (STD-001)](standards/engineering-principles.md#std-001) owns the test-first obligation. The playbook adds one separate, conditional [external-boundary verification standard (STD-009)](standards/testing.md#std-009). Consult [standards governance](governance/standards.md) for applicability and reviewed exceptions.

**References reviewed:** November 15, 2026. Recheck the applicable documentation and installed framework, runner, target, SDK, MSBuild, and OS before adopting a command or feature. The examples below are illustrative C#, **not compiled sample projects or observed test results**.

## Microsoft references and their scope

| Concern | Primary official reference | Application |
| --- | --- | --- |
| Testing levels and framework choice | [Testing in .NET](https://learn.microsoft.com/en-us/dotnet/core/testing/) | Distinguishes unit and integration tests, test frameworks, and execution platforms. |
| Unit-test quality | [Unit testing best practices](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices) | Fast, isolated, repeatable tests; naming; Arrange–Act–Assert; test doubles; coverage limitations. |
| ASP.NET Core boundaries | [Integration tests](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests) | Test-host setup, request/response verification, and relevant real infrastructure. |
| Database fidelity | [EF Core testing strategy](https://learn.microsoft.com/en-us/ef/core/testing/choosing-a-testing-strategy) | Real-provider testing and limitations of SQLite, in-memory providers, and mocks. |
| Asynchronous execution | [C# async guidance](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/async) and [MSTest test methods](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-mstest-writing-tests) | Awaitable tests, completion, and error propagation; avoid `async void` test methods. |
| Test execution | [`dotnet test`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test) and [testing with `dotnet test`](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test) | Version-aware VSTest and Microsoft.Testing.Platform modes. |
| Platform choice | [VSTest vs. Microsoft.Testing.Platform](https://learn.microsoft.com/en-us/dotnet/core/testing/test-platforms-overview) | Compatibility and reporter tradeoffs; do not blindly mix platforms. |
| Traditional test execution | [VSTest.Console options](https://learn.microsoft.com/en-us/visualstudio/test/vstest-console-options?view=vs-2022) | Direct assembly execution and results on compatible Visual Studio/Windows toolchains. |
| Coverage collection | [Code coverage for unit testing](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-code-coverage) and [MTP coverage](https://learn.microsoft.com/en-us/dotnet/core/testing/microsoft-testing-platform-code-coverage) | Collectors, report formats, and runner-specific configuration. |

Microsoft's examples often use a particular framework or project type; that example choice does not require every adopting repository to select it. Distinguish Microsoft recommendations from the stronger playbook obligations linked above.

## Choosing the first test and broader evidence

The [STD-001 cycle](standards/engineering-principles.md#std-001-cycle) is **red → green → refactor**. Start with a failing example of **what a consumer should observe**, not a test asserting how private implementation happens. Check that the failure is about the missing or incorrect behavior, satisfy it with the smallest production change, refactor with tests passing, and repeat.

For a defect, reproduce the incorrect outcome first where possible; a test describing existing behavior is a *characterization*, while a regression test expresses the intended corrected behavior. When the usual red state cannot reasonably be obtained, follow STD-001's [reviewed exception guidance](standards/engineering-principles.md#std-001-cycle). Documentation-only edits are not behavioral TDD exceptions.

Choose the lowest-cost test boundary that can genuinely answer the question, then add broader evidence for risks that the first test cannot cover:

| Level | What is exercised | Good use | What a pass does **not** establish |
| --- | --- | --- | --- |
| **Unit** | One behavior with controlled in-process collaborators and no real infrastructure | Pure calculations, parsing rules, domain decisions | Database, filesystem, network, or deployment compatibility |
| **Component** | A cohesive group of application objects through a public component boundary, with controlled external ports | Application orchestration, business workflows, failure mapping | Fidelity of substituted external systems |
| **Integration** | Multiple real components or a real infrastructure boundary in a controlled environment | Actual database/provider queries, file I/O, protocol/serialization integration | Every production configuration or an entire deployed user journey |
| **Contract** | A producer/consumer agreement, such as request/response schema, error status, or message format | Compatibility between independently changed clients and services | Provider behavior unless the contract is verified against that provider; full operations and deployment |
| **End-to-end** | A representative user-visible path through the assembled application and relevant dependencies | Authentication and a critical transaction across deployed components | Every failure mode, branch, or lower-level boundary case |

These are **selection descriptions**, not a universal test pyramid quota. A small pure library may need only focused unit tests. A web service with external adapters may need component tests, selected real integration/contract tests, and a small number of valuable end-to-end journeys. Component and contract terminology varies among teams; state the boundary and dependency fidelity rather than relying only on the label.

### Choosing the layers in two project profiles

| Question | Small pure library | Adapter-backed application |
| --- | --- | --- |
| Initial failing test | Public behavior of a pure type/function | Public application use case or adapter behavior at the smallest meaningful boundary |
| Controlled dependencies | Usually none | Stub/fake external ports for application policy; control time or randomness as needed |
| Broader evidence | Add only for actual integration surfaces | Focused tests of consequential adapter behavior using real dependencies or appropriately validated contracts under [STD-009](standards/testing.md#std-009) |
| Typical exclusions | No invented database or web host | No requirement to test every orchestration permutation through a deployed system |

## Example A — A pure C# library

Suppose a library exposes `PageRange.Clamp(requested, totalPages)` and an existing implementation incorrectly returns zero when `requested` is zero. First add a behavioral regression test. This illustration uses **NUnit 3 syntax**, but the principle also works in xUnit, MSTest, or another compatible framework. The code uses C# 7.3-compatible constructs; the test project still needs its chosen runner and references.

```csharp
using NUnit.Framework;

[TestFixture]
public class PageRangeTests
{
    [Test]
    public void Clamp_RequestBelowFirstPage_ReturnsFirstPage()
    {
        // Arrange
        const int requested = 0;
        const int totalPages = 10;

        // Act
        int actual = PageRange.Clamp(requested, totalPages);

        // Assert
        Assert.That(actual, Is.EqualTo(1));
    }

    [TestCase(5, 10, 5)]
    [TestCase(15, 10, 10)]
    public void Clamp_ValidAndAboveLastRequests_ReturnExpectedPage(
        int requested, int totalPages, int expected)
    {
        Assert.That(PageRange.Clamp(requested, totalPages), Is.EqualTo(expected));
    }
}
```

The first test **would fail** against an implementation returning `Math.Min(requested, totalPages)` because the actual result would be `0`, not `1`. The expected failure is a behavioral mismatch, not a broken test fixture. A minimal correction could be:

```csharp
using System;

public static class PageRange
{
    public static int Clamp(int requested, int totalPages)
    {
        if (totalPages < 1)
        {
            throw new ArgumentOutOfRangeException(nameof(totalPages));
        }

        return Math.Min(Math.Max(requested, 1), totalPages);
    }
}
```

Then run the focused test, add relevant invalid-input cases, and refactor any duplication while retaining the expected results. No mock is necessary. The test names describe a scenario and outcome rather than the private use of `Math.Min` or `Math.Max`. **These are proposed example outcomes, not tests executed by this repository.**

## Example B — An application with an infrastructure adapter

Imagine an invoice-report use case that depends on an application-owned `IInvoiceSource` port. Its production adapter reads CSV files. Test the application policy without real file I/O, then exercise the important file-format and I/O behavior against a real, isolated file. These are **illustrative excerpts** referencing hypothetical application types; the playbook does not ship their implementations or fixtures.

The application-level behavioral test uses a simple stub to represent a missing invoice:

```csharp
using System.Threading;
using System.Threading.Tasks;
using NUnit.Framework;

[TestFixture]
public class InvoiceReportTests
{
    [Test]
    public async Task GenerateAsync_MissingInvoice_ReturnsNotFound()
    {
        IInvoiceSource source = new MissingInvoiceSource();
        var useCase = new GenerateInvoiceReport(source);

        ReportResult result = await useCase.GenerateAsync(
            "INV-42", CancellationToken.None);

        Assert.That(result.Status, Is.EqualTo(ReportStatus.NotFound));
    }

    private sealed class MissingInvoiceSource : IInvoiceSource
    {
        public Task<Invoice> ReadAsync(string id, CancellationToken cancellationToken)
        {
            return Task.FromResult<Invoice>(null);
        }
    }
}
```

That test specifies **application behavior when the port reports absence**. It does not establish that the CSV adapter can parse a quoted field, handle file encodings, or report a real I/O error. For material file-format behavior, use an integration test against actual file I/O, with cleanup even if an assertion fails:

```csharp
using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using NUnit.Framework;

[TestFixture]
public class CsvInvoiceSourceTests
{
    [Test]
    public async Task ReadAsync_QuotedCustomerName_PreservesEmbeddedComma()
    {
        string path = Path.Combine(
            Path.GetTempPath(), Guid.NewGuid().ToString("N") + ".csv");

        try
        {
            File.WriteAllText(path, "id,customer\nINV-42,\"Acme, Inc.\"\n");
            var source = new CsvInvoiceSource(path);

            Invoice invoice = await source.ReadAsync("INV-42", CancellationToken.None);

            Assert.That(invoice.CustomerName, Is.EqualTo("Acme, Inc."));
        }
        finally
        {
            if (File.Exists(path))
            {
                File.Delete(path);
            }
        }
    }
}
```

This would catch a naive comma-splitting parser and demonstrates the actual filesystem boundary, although it does not prove behavior under every file permission, encoding, operating system, or deployment setting. Add an important real failure case—such as missing-file or denied-access behavior—in the appropriate environment, asserting the adapter's public error contract rather than its internal exception-handling calls.

For a SQL-backed adapter, a comparable integration test should use the intended database provider and representative configuration. Substituting SQLite or EF Core's in-memory provider for SQL Server can change query, collation, transaction, or raw-SQL behavior; [Microsoft explains the tradeoffs](https://learn.microsoft.com/en-us/ef/core/testing/choosing-a-testing-strategy). For an HTTP service without a safe real environment, provider-validated contract evidence may help, but identify what is still unverified and apply [STD-009's exception process](standards/testing.md#std-009) if the required representative boundary cannot be exercised.

## Test design and deterministic execution

Follow the applicable [Microsoft unit-test recommendations](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices), adapting them to the actual test boundary:

- **Names and structure:** Describe behavior, scenario, and outcome; Arrange–Act–Assert makes the relevant stimulus and observation easy to locate. Do not require a universal method-name template or assert private implementation steps.
- **Isolation:** Avoid hidden dependencies on test order, global mutable state, prior executions, local culture/time zone, live clock, or unrelated network availability. Give parallel tests independent data and resources or deliberately constrain concurrency for a documented reason.
- **Fixtures and data:** Keep common setup small and explicit. Use small representative data plus boundary/negative cases; dispose resources and clean up even after failure. Shared expensive fixtures are acceptable when they cannot cause one test to alter another's expected state.
- **Test doubles:** A stub returns controlled values, a fake supplies a simplified working implementation, and a mock may verify an important externally observable interaction. Prefer asserting outcomes; avoid strict invocation order/count assertions that merely freeze private implementation. A fake does not certify real-provider fidelity.
- **Async behavior:** Return an awaitable `Task` (or a supported equivalent), await work and assertions, and ensure failures propagate to the runner. Avoid `async void`, arbitrary `Thread.Sleep`, and timing-sensitive races. Inject clocks/schedulers or use explicit synchronization where necessary; test cancellation/timeout behavior when it is part of the contract.
- **Test independence:** Run focused tests individually and in suites; repeat or reorder them when diagnosing state leakage. Re-running a flaky test until it passes does not eliminate the underlying reliability problem.

Unit tests normally avoid filesystem, database, and network dependencies. Integration tests intentionally cross some of those boundaries, so their determinism depends on controlled environments, setup, and cleanup—not on pretending the external resources are absent.

## Reading execution evidence

| Observation | Supported conclusion | Not established |
| --- | --- | --- |
| Expected tests executed and passed | Those scenarios passed in the stated revision and environment | Unexecuted scenarios, other platforms, or production equivalence |
| A test failed | That verification run failed; investigate the behavioral or environmental cause | That all other tests are invalid or that the cause is necessarily product code |
| A test was intentionally skipped | The test supplied **no pass/fail behavior evidence** in that run; review its reason and scope | A pass for the skipped requirement |
| An expected test was unexpectedly absent or no tests were discovered | The expected verification is missing, regardless of a zero exit code from some configurations | A passing behavioral test suite |
| A run was blocked by unavailable tools/services | Execution is unverified in that environment; document alternative evidence and risk | A successful test or an automatic STD-001/STD-009 exception |

Report the test selection, discovered/executed/passed/failed/skipped counts when available, exact command, target revision, relevant tool/framework versions, environment, exclusions, and result artifact. A skipped platform-specific test need not automatically fail every PR, but a required behavior exercised **only** by a skipped test cannot be declared verified without appropriate alternative evidence and review. Existing [evidence-based claims](standards/engineering-principles.md) and [CI/local parity (STD-002)](standards/engineering-principles.md#std-002) govern the related reporting and automation principles.

### Code coverage is diagnostic evidence

Line, branch, or method coverage can reveal code that was not exercised and help choose further tests. It cannot prove that assertions are meaningful, that failures are handled correctly, or that a user-visible requirement is satisfied. Microsoft's [unit-testing best practices](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices#code-coverage-and-code-quality) explicitly warns against using an ambitious percentage as a proxy for quality.

Use applicable .NET/Visual Studio coverage collectors or compatible tools when the project benefits, and interpret collection/reporting limitations. **No universal coverage threshold, collector, report generator, or custom coverage processor is required** by this issue. A high percentage is not release approval; a low percentage alone does not establish which missing tests matter most.

## Version-aware execution and verification

| Project/toolchain | Reasonable starting point | Verify before claiming success |
| --- | --- | --- |
| Modern SDK-style project using VSTest-compatible test packages | Run the selected project/solution with `dotnet test`; use a supported results logger such as TRX where configured | SDK, test adapter/framework, target runtime, discovery and exit behavior, output paths |
| SDK-style project using Microsoft.Testing.Platform (MTP) | Use the selected MTP mode or executable runner according to the SDK/platform version | Modern `dotnet test` runner selection, registered reporters/extensions, and option syntax; do not reuse VSTest-only switches blindly |
| Traditional non-SDK .NET Framework project | Build with its compatible MSBuild/Visual Studio toolchain; execute test assemblies with `vstest.console.exe` or another installed compatible framework runner | Windows/runtime, framework version, adapter discovery, architecture, package integration, and result capture |
| Multi-target or multi-OS verification | Execute the relevant target/platform matrix where the behavior matters | Which targets actually ran; platform exclusions and unverified combinations |

Microsoft documents that `dotnet test` supports VSTest and MTP with different options and prerequisites. Modern MTP selection in `dotnet test` is available starting with the .NET 10 SDK; MTP also has version-dependent .NET Framework support, which does **not** imply that every traditional non-SDK project works with the same invocation. See the [test-platform comparison](https://learn.microsoft.com/en-us/dotnet/core/testing/test-platforms-overview), [`dotnet test` reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test), and [VSTest.Console options](https://learn.microsoft.com/en-us/visualstudio/test/vstest-console-options?view=vs-2022). Verify the actual toolchain before adopting command examples.

When repository-owned validation scripts and CI exist, prefer one underlying check invoked locally and in CI under [STD-002](standards/engineering-principles.md#std-002). This playbook repository currently supplies **no executable testing validator, CI workflow, sample projects, or universal test-runner configuration** for consumers. The documentation and snippets above are guidance—not observed compilation, runtime, coverage, or cross-platform evidence.
