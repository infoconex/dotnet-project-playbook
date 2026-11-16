# Microservices Architecture: on-demand .NET guidance

This guide helps assess whether **independent service deployment is worth its total lifecycle cost**. It is practical advice for a new application, an existing monolith, or an already distributed system. [STD-017 — Microservices Architecture](standards/microservices.md#std-017) is the **only normative definition** of the playbook's conditional Recommended adoption and service-autonomy expectations. This guide introduces no new Required obligations, mandates, tests, or executable templates.

**Start simple:** A cohesive monolith or [modular monolith](modular-monolith-guidance.md) can be the correct permanent design. Microservices become useful when real business and operational needs justify more deployment boundaries—not because a design has multiple modules, bounded contexts, HTTP endpoints, handlers, or teams. Microsoft's [architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices), [domain analysis](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis), and [microservices readiness assessment](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/microservices-assessment) inform these choices.

## Level 1 — Choose deployment autonomy deliberately

### First compare the simplest adequate architecture

| Observed circumstance | Usually start with | When to reconsider |
| --- | --- | --- |
| Small pure library, cohesive CLI, or straightforward CRUD | One production project or a simple monolith | Significant external dependencies or growing independent business change pressures; still not automatically services |
| Several business capabilities with shared release goals and useful local transactions | Modular monolith, optionally with Vertical Slices | Measured independent release, resource, availability, or ownership needs outweigh distributed coordination |
| Complex domain with evolving rules and distinct meanings | DDD-guided model boundaries; choose deployment separately | A particular boundary needs a genuinely independent release or failure domain |
| Two teams working in the same business capability | One cohesive ownership boundary and collaboration plan | Releases repeatedly block one another **and** service operations are supportable |
| Independent load profiles or material availability isolation | Evaluate independent deployment and scaling for specific responsibilities | A common host cannot meet verified capacity/availability targets economically |
| High-regulation or sensitive data | Define identity/data boundaries and assurance controls in any architecture | A separate service is shown to improve access isolation, control ownership, or compliance evidence |
| Existing Windows/.NET Framework system | Behavior-preserving incremental modularization | A specific service extraction solves a measured problem with supportable contracts and infrastructure |
| Small operational team with no credible 24/7 distributed support | Monolith or modular monolith | Team gains sufficient deployment, observability, on-call, rollback and recovery capacity |

The **decision record** should name the business problem, affected workload or organizational boundary, candidate architectures, expected independence benefit, network and data tradeoffs, operating cost, and what evidence would make the decision change. No fixed service count, latency threshold, throughput metric, or engineering-team size universally determines the answer.

**Scenario A — business complexity without deployment pressure:** Orders, Inventory, and Billing each have significant rules, and DDD bounded contexts may help. If the same small team releases the system together, orders need a consistent local transaction, and operations are healthy, a modular monolith can offer useful ownership without separate deployments. More business capabilities do **not** by themselves justify microservices.

**Scenario B — justified service boundary:** A tenant-specific document-conversion workload has materially distinct CPU demand, needs independently controlled rollout and failure containment, and can own its input/output state behind a stable contract. An independently deployed converter can be justified if the team can operate it, control timeouts and retries, and verify recovery and authorization. The surrounding application may remain monolithic.

**Scenario C — misleading distribution:** Orders and Inventory run in different containers but share mutable tables; changing a column or business rule requires deploying both in a maintenance window. This is evidence of a distributed monolith, not proof of release autonomy. Either restore an owner-controlled contract and safe evolution, or reunite the tightly coupled behavior.

### Map the boundaries accurately

| Concept | Practical meaning | Common incorrect inference |
| --- | --- | --- |
| Feature / vertical slice | Cohesive operation or group of use cases | Every slice becomes its own service |
| Module | Business capability with an internal public surface | Every module needs a process |
| DDD bounded context | Scope in which a domain model and language have meaning | Every context needs exactly one deployment |
| Assembly / C# project | Compilation and reference boundary | More projects means more microservices |
| Process / container | Running execution unit | Isolated process means independently releasable |
| Deployment unit | Separately replaceable release unit | Independent release automatically guarantees safe contract and data evolution |
| Microservice | Business-owned capability with independent deployability and operability | One process per team, one repo, or one database server |

A bounded context can help identify candidate services, but service design also weighs nonfunctional requirements, coupling, and transactions. Services can have internal layered, hexagonal, clean, or feature-oriented organization. Microsoft's [boundary evaluation guidance](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/microservice-boundaries) recommends revisiting decomposition as evidence changes.

### Independently deployable means more than isolated processes

Ask whether a significant service update can be built, configured, tested, released, and, when necessary, rolled back/forward **while unaffected services remain on their compatible versions**. This may use a shared monorepo, a shared CI platform, centralized deployment approvals, one observability stack, or shared host infrastructure. Reusable pipelines are not a sign of coupling; a **mandatory synchronized release train** often is.

Look for:

- versioned release artifacts and deployment ownership appropriate to the service;
- backward- and forward-compatible APIs/events during a meaningful migration window;
- database schema/data migration compatible with live consumers and, where necessary, rolling instances;
- independently configurable secrets, identity, health checks, and resources;
- documented recovery, rollback/roll-forward, operational alerts and responsibilities;
- service-level objectives for critical components, not an SLO quota for every technical process.

A rollback is not always a database schema rollback: a safe roll-forward or expand/migrate/contract sequence may be the realistic recovery route. Do not claim a rollback strategy works solely because a workflow declares a rollback command. [Microsoft CI/CD guidance](https://learn.microsoft.com/en-us/azure/architecture/microservices/ci-cd) discusses independent service releases, shared pipeline infrastructure, and compatible side-by-side updates.

## Level 2 — Design service contracts, state, reliability, and trust

### Business boundaries before networks

A service should control coherent decisions and owned state, not merely act as a remote database table or wrap each entity with an endpoint. Identify the owner of each important invariant, transaction, and consumer-facing operation. Separate shared business concepts by meaning and context where necessary; use stable identifiers or published contracts instead of a globally shared mutable domain object model.

If a split creates frequent synchronous round trips, cycles, cross-service write-through, or repeated atomic transactions, reconsider granularity. A larger coherent service may be more autonomous than many tiny services. Conversely, an independently scaled costly workload or strict security boundary may warrant separation despite a shared broad business domain. Domain analysis informs; it does not mechanically prescribe deployment counts.

### Own data logically, not by mandatory server count

| Data concern | Practical choice | Risk to evaluate |
| --- | --- | --- |
| Authoritative writes | Mutations go through the owning service | Other services writing owned tables bypass invariants and coordinated schema evolution |
| Shared database infrastructure | Separate logical schemas/stores and access permissions on the same physical server can be valid | Shared tables, unchecked direct reads, shared migrations, and broad SQL credentials collapse ownership |
| Immediate critical decision | Consult the source-of-truth service or keep invariants within one transaction boundary | Stale replicas may be unacceptable |
| Cross-service reporting | Owner-approved API/export, replicated projection, read model, or dedicated analytics pipeline | Freshness, schema dependency, privacy, lineage, and recovery |
| Local transaction | Use normal ACID transactions within the owner's persistence where supported | Calling remote services inside a local transaction does not make a global transaction atomic |
| Multi-service workflow | Define stages, durable progress, retries, idempotency and compensating/reconciliation behavior according to business impact | Partial completion, irreversible actions, duplicate processing, delayed messages |
| Asynchronous events | Publish defined integration contracts, schema/version and delivery behavior when justified | Missed publications, duplicates, out-of-order messages, consumer lag |

**Scenario D — inventory reservation:** If an order may be confirmed only when stock is reserved, identify which service owns stock and reservation invariants. A direct owner API can give an immediate confirmed/rejected outcome when availability requirements permit. If a durable asynchronous workflow is chosen, define a pending state, timeout, cancellation, compensation, and user-visible reconciliation. A saga does not magically create an ACID transaction across services.

**Scenario E — reporting:** A finance report needs Orders and Payments. Consider a projection populated from owner-approved events or exports, or an orchestrated read interface. Do not grant every reporting component uncontrolled write access to those services' schemas. Describe acceptable staleness and how missed updates are repaired.

A shared physical database **server** is not inherently prohibited by Microsoft's [data considerations](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/data-considerations); shared authoritative **tables and schemas** undermine independent ownership. Strictly audit technical access even when code-level intentions look sound.

### Choose collaboration semantics, not a fashionable transport

**Synchronous request/response** is often appropriate when an immediate answer is essential and a bounded dependency is acceptable. HTTP/JSON is broadly interoperable; gRPC can be useful where supported tooling, strongly defined contracts, or measured payload/latency needs justify it. Account for DNS/service discovery, secure identities, client budgets, cancellation, API versioning, and client-visible failures.

**Asynchronous messages** are useful when independent availability, buffering, workload smoothing, or durable fan-out materially helps. A domain event inside a model is not automatically an externally published integration event. For messages define owner/publisher, consumer authorization, durable publication requirements, schema/version, delivery guarantee, ordering assumption, deduplication, poison/dead-letter handling, replay, and operational reconciliation where relevant.

A transactional outbox may solve the **commit succeeded but event was never published** gap when a database write and external publication must be coordinated. An inbox/idempotent consumer may handle at-least-once redelivery. Neither pattern guarantees all downstream business effects happen exactly once; external side effects and repeat processing need their own semantics. Use these patterns only when material failure scenarios warrant them. See Microsoft's [communication guidance](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/interservice-communication), [idempotent consumer](https://learn.microsoft.com/en-us/azure/architecture/patterns/idempotent-consumer), and [transactional-outbox example](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos).

For meaningful remote calls, establish a **total latency budget**, including potential retries. Retry only failures and operations safe to repeat; bound attempts and avoid retry storms. Consider circuit breaking, bulkheads, backpressure, rate limits, cached/fallback results, and partial availability when their identified risk merits them. No mandatory resiliency library or service mesh. Microsoft's [retry guidance](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry), [circuit breaker guidance](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker), and [partial-failure discussion](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/implement-resilient-applications/partial-failure-strategies) explain the tradeoffs.

### Contracts must evolve independently

Prefer changes that old consumers tolerate and new providers can handle. For breaking API or message changes, plan coexistence, consumer migration, version negotiation or routing, and explicit deprecation. Schema evolution may use expand/migrate/contract. Verify real consumer/provider interactions rather than treating a shared DTO package or successful compile as a compatibility guarantee.

An API gateway may simplify external routing, authentication and rate limiting; it is not automatically required for an internal-only system and does not replace service authorization. For direct callers or asynchronous consumers, validate the actual identity and permissions at the receiving boundary. See Microsoft's [API design](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/api-design) and [.NET security guidance](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/secure-net-microservices-web-applications/).

### Security and tenant boundaries travel with the request

For each material caller and consumer, consider:

- user authentication, service-to-service/workload identity, delegated identity, and authorization for the requested operation;
- tenant isolation on reads, writes, cached data, messages, logs, and projections;
- TLS and appropriate service identity validation where trust boundaries require it;
- secrets at rest, in transit, at runtime, and in CI; rotation and least-privilege data access;
- explicit API ingress/egress controls and service discovery/network rules;
- message publisher trust, subscriber permissions, integrity, replay/duplication, and payload sensitivity;
- audit trails, correlation, retention and redaction of potentially sensitive telemetry;
- supply-chain provenance, secure service release permissions, vulnerability handling, and recovery access.

Gateway authentication alone cannot be treated as sufficient when a service is separately reachable. A monolith requires strong security too; distribution adds identities and paths to administer, not an automatic security improvement.

### Select hosting by requirements

A microservice can be hosted on VMs, managed application hosts, serverless functions, containers, on-premises infrastructure, or hybrid environments if its independent release and operational semantics are real. Kubernetes and a service mesh are tooling options for specific scale/network/operations demands. One service may contain multiple compiled projects; several runtime processes may still constitute one jointly released application. A separate repository, database server, or container is **not** the service contract.

For .NET Framework, confirm actual Windows/IIS/Windows Service or other supported hosting, MSBuild/Visual Studio and available C# language level; do not infer support for modern .NET-only hosting APIs, Native AOT, Linux, or a particular container image. For SDK-style modern .NET, verify specific SDK, runtime target and OS/RID constraints as needed. A technical stack migration is a separate choice from domain/service decomposition.

## <a name="level-3--assess-verify-and-evolve"></a>Level 3 — Assess, verify, and evolve

### Representative scenario review

| Scenario | What to check | What evidence would justify the conclusion |
| --- | --- | --- |
| Service A releases without B | API compatibility, schema migration, release dependency graph | Observed A deployment with unchanged compatible B in a representative environment, plus relevant contract evidence |
| New and old clients overlap | Versioned contracts and handling of missing/added fields | Provider-validated consumer interactions or representative side-by-side API tests |
| A shared database server hosts two services | Schema/table ownership and credentials | Access-control/schema inspection and tests that unauthorized cross-service writes fail |
| Network call hangs or target becomes unavailable | Timeouts, fallback, latency budget, incident signals | Measured failure behavior in running representatives; static retry configuration alone is insufficient |
| Duplicate event is delivered after consumer restart | Idempotency and durable effect handling | Representative duplicate delivery and state/effect assertions against the actual relevant dependencies |
| Workflow fails after payment or stock reservation | State machine, reconciliation, compensation and irreversible actions | Relevant partial-failure and recovery tests; explain what is not reversible |
| Tenant A calls Tenant B's resource through an internal endpoint | Service authorization and data isolation | Negative security/integration test through the real entry path; gateway policy alone is inadequate |
| Deployment introduces a bad schema change | Compatibility window, rollback/roll-forward and migrations | Representative migration rehearsal and recovery outcome |
| Cross-service request cannot be diagnosed | Trace propagation, service metrics and sensitive-data redaction | Observed correlated telemetry across the meaningful flow and privacy inspection |
| Service claims independent scaling | Actual separate resource settings, bottleneck, load profile | Measurements in a representative environment under meaningful load; not merely autoscale configuration |

This is a **scenario menu**, not a mandatory ten-test checklist. Select material paths according to the system's business consequences and architecture claims. Apply [STD-001](standards/engineering-principles.md#std-001) to executable changes and [STD-009](standards/testing.md#std-009) to significant new/changed external adapters; a fake-only suite does not establish real provider behavior.

### What each form of evidence can establish

1. **Design documents and static/source inspection** can locate boundaries, declared ownership, API definitions, dependencies, permissions, and configured pipelines. They cannot prove deployed releases, actual security enforcement, or network recovery.
2. **Domain/application tests** establish exercised business outcomes with controlled collaborators. They cannot prove a remote provider, broker, database transaction, or deployed service conforms.
3. **Provider-validated contracts and representative integration tests** check selected compatibility and real dependency behavior. They cannot alone prove independent production rollout, disaster recovery, or availability.
4. **Deployment/release and failure exercises** can demonstrate important startup, coexistence, rollback/roll-forward, timeouts, duplicate processing, authorization, and recovery in the tested environment. They do not certify every network/traffic condition or provider version.
5. **Observability and performance measurements** demonstrate instrumented flows and measured load cases, not universal resilience or linear scalability. Report environment, revision, workload, versions, results, limitations, and what remains unknown.

Prefer fast local unit tests and selective contracts/integrations, supplemented by expensive deployed-system checks where the consequential properties require them. No universal per-service staging cluster, chaos suite, test runner, cloud provider, or coverage threshold is imposed by this guide.

### Incremental adoption and de-adoption

For an existing monolith or modular monolith:

1. Characterize the relevant behavior, public interfaces, domain authority, persistence transactions, and actual build/hosting constraints.
2. Identify one cohesive candidate whose release or operations pressure is **already evidenced**; compare leaving it in process.
3. Establish a stable owner-controlled contract, permissions and data evolution plan before traffic moves. Consider an anti-corruption layer or a Strangler Fig routing transition where warranted.
4. Move behavior and authoritative state in safe, reviewable increments. Preserve compatibility and monitor dual-write/migration/reconciliation risks; do not assume wholesale database extraction is required at once.
5. Deploy and verify the new boundary, including representative compatibility, authorization, partial failures and recovery, before claiming service autonomy.
6. Reassess whether separation paid for its operating cost. Merge services or return behavior to a modular monolith when chronic coordination outweighs benefits.

This can be done with modern .NET, legacy .NET Framework, on-premises, or hybrid systems, subject to real toolchain constraints. Microsoft's [assessment and readiness guidance](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/microservices-assessment) and [Strangler Fig pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig) support gradual change. Neither pattern requires that modernization end with all capabilities distributed.

### Relationship to neighboring styles

- [Single-project guidance](single-project-guidance.md): one production project can be a sound architecture; project counts and deployments are different.
- [Traditional layered/N-tier guidance](layered-n-tier-guidance.md): tiers may be remote yet remain one jointly released system; services may internally use technical layers.
- [Hexagonal](standards/hexagonal.md#std-012) and [Clean](standards/clean.md#std-013): separately Recommended internal dependency patterns; adoption is independent of service deployment.
- [DDD](standards/ddd.md#std-014): context-specific meaning and invariants inform candidate service boundaries without dictating a one-to-one mapping.
- [Modular Monolith](standards/modular-monolith.md#std-015): an alternative, sometimes preferable **single-deployment** ownership architecture; no inherent microservices migration obligation.
- [Vertical Slice](standards/vertical-slice.md#std-016): use-case organization within a monolith, module or microservice; a slice is not a deployment unit.
- [STD-003](standards/engineering-principles.md#std-003): separate compiled projects remain Optional.
- [STD-011](standards/dependency-direction.md#std-011): business-policy independence remains Required in both monolithic and distributed applications.

## Source and verification boundary

Authoritative Microsoft material: [architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices), [service boundaries](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/microservice-boundaries), [data considerations](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/data-considerations), [communication](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/interservice-communication), [API design](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/api-design), [CI/CD](https://learn.microsoft.com/en-us/azure/architecture/microservices/ci-cd), [security](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/secure-net-microservices-web-applications/), [monitoring](https://learn.microsoft.com/en-us/azure/well-architected/design-guides/monitoring), [testing](https://learn.microsoft.com/en-us/azure/well-architected/design-guides/testing), and [readiness](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/microservices-assessment).

All scenarios and references here are **illustrative guidance**, not a compiled, deployed, tested, or vendor-certified implementation. Review actual consumer code, environment, tests, traces, and releases before describing any such property as verified. This documentation-only repository currently has no executable template generator, validation script, or CI workflow to prove those runtime properties.
