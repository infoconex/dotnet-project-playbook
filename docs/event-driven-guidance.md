# Event-Driven Architecture: on-demand .NET guidance

Use this guide to decide **whether event-mediated communication is worth its complete lifecycle cost**, and—when justified—how to reason about facts, contracts, consistency, reliable processing, security, testing, recovery and maintenance.

[STD-018 — Event-Driven Architecture](standards/event-driven.md#std-018) alone defines the conditional Recommended playbook expectation. This document is explanatory, **not a second normative standard**, an installable template, or a verified messaging implementation. Follow [standards governance](governance/standards.md) for applicability and exceptions. Microsoft's [Event-Driven Architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven) is the technical starting point.

**Rule of thumb:** Prefer direct synchronous communication when the caller needs an immediate authoritative answer, a local atomic invariant, or simple coordination. Consider events and queues when independent processing, independent consumers, durable work distribution, workload leveling, replay or meaningful integration makes additional failure and operational complexity worthwhile.

## Level 1 — Choose the simplest adequate communication mechanism

### Compare actual mechanisms, not architecture labels

| Mechanism | Useful when | Costs and caution |
| --- | --- | --- |
| Direct in-process method call | Immediate local collaboration with clear owner and direct result | Synchronous coupling, but simple transaction and debugging semantics |
| Synchronous application service | One use case coordinates local domain operations, authorization or a transaction | Keep business decisions in their authoritative model, not orchestration-only handlers |
| In-process domain event | Significant domain occurrence triggers local reactions without changing the producer's explicit collaborators | Define handler timing, exceptions and transaction membership; not necessarily durable or public |
| HTTP request/response | Remote owner can immediately answer a query or decide an operation | Timeouts, transient errors, retry safety, remote availability and contract migration |
| gRPC | Strongly contracted, potentially efficient service-to-service request/response | Remote failure, deployment/contract compatibility and toolchain/platform support still apply |
| Asynchronous command | Addressed work should be performed later, potentially reliably by one responsible processor | Must define acceptance versus eventual completion, duplicate submissions and status/recovery |
| Asynchronous event notification | An occurrence should be announced without requiring the originator to know the reactions | Consumer lag, lost notifications and stale downstream views may matter |
| Publish-subscribe messaging | Multiple independent consumers need the same fact with independent reactions | Subscription governance, schema ownership, consumer isolation, fan-out failures and cost |
| Durable message queue | Buffer or distribute work during downstream outages or bursts | Acknowledgment, retry, duplicate handling, poison messages, DLQ ownership and queue age |
| Event stream/log | High-throughput ingestion, retained history, partition-local order and replay matter | Partition/key choice, offsets/checkpoints, retention, replay side effects, storage growth |
| Event-carried state transfer | Consumers need a useful published snapshot without synchronously querying producer | Larger or sensitive payloads, stale copies, contract churn and data deletion obligations |
| Event sourcing | Authoritative state is deliberately reconstructed from append-only domain history | Event version permanence, projections/rebuilds, compensation, migration and operational complexity |

These are distinct choices, not a progression that every application must follow. For example, a durable **command queue** is not necessarily an event-driven pub/sub model: one processor is asked to perform work. Conversely, an in-process domain event can be synchronous and participate in one transaction. A stream is not equivalent to a short-lived notification subscription. Event sourcing changes the **source of truth**, not merely the delivery mechanism.

A command expresses a requested action (for example, "Reserve inventory for order 123"); an event expresses a completed occurrence (for example, "InventoryReserved for order 123"). Do not label a command as a past-tense event merely to use a bus. If the event reports business state that has not committed, consumers may act on a false fact; separate tentative/in-progress signals clearly from committed integration facts.

Microsoft's [asynchronous messaging guide](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/messaging), [publisher-subscriber pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/publisher-subscriber), [competing consumers pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/competing-consumers), [queue-based load leveling](https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling), [CQRS](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) and [event sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) help assess the alternatives. Illustrative Azure products do not make Azure a required deployment choice.

### Decision scenarios

| Situation | Likely simplest adequate starting point | Change only when evidence supports |
| --- | --- | --- |
| Small CRUD app, pure library, or cohesive CLI | Direct operations, ordinary transactions and tests | An actual asynchronous integration or durable background workload emerges |
| Orders and Inventory in one modular monolith need one atomic reservation | Owner-approved in-process operation and a supported local transaction | Independent processing becomes legitimate and the business can handle pending reservations |
| API must immediately reject an unauthorized payment or unavailable inventory | Synchronous authoritative business decision | Workflow redesign explicitly permits an accepted/pending result |
| Best-effort UI refresh or optional analytics notification | Simple in-process event or non-durable notification as requirements permit | Loss would become materially harmful |
| Receipt generation must survive service restarts and temporary mail-provider outages | Durable background command queue, retry/observability, idempotency for duplicate sends | Independent fan-out would justify pub/sub |
| Several separately maintained systems require an order-accepted fact | Owned integration-event contract and independently managed consumers | Broker/stream design depends on durability, volume, retention and replay requirements |
| Telemetry ingestion with large throughput and consumer replay | Stream with deliberate partition and retention choices | Do not mistake partition-local order for a global business order |
| Long-running multi-party fulfillment | Explicit process state, ownership and outcomes; optional durable coordination | Saga/process manager only if independently committed steps justify it |
| Regulated tenant-separated messaging | Start with authority, data minimization, isolation, access and retention requirements | Add only infrastructure whose controls meet those requirements and can be operated |
| Legacy .NET Framework / on-premises system | Existing supported transaction and communication mechanisms | Incrementally introduce compatible adapters without a runtime or deployment rewrite |

A producer/consumer flow can reside in a single process, single deployment, modular monolith, or multiple independently deployed services. A modular monolith is allowed to use a common database and coordinated local transactions without pretending to be distributed. Conversely, a microservices system can reasonably use synchronous HTTP or gRPC. Avoid replacing one direct call with a queue if the caller still blocks waiting for a reply: that may add broker complexity without achieving temporal independence.

## Level 2 — Design event semantics, contracts and failure behavior

### Domain events, integration events, and ownership

A **domain event** expresses something significant within a domain model. It may trigger local reactions or inform application orchestration, but its existence does not authorize another context to receive an internal entity or does not imply use of a broker. [STD-014](standards/ddd.md#std-014) owns domain invariants, aggregate consistency and bounded-context language.

An **integration event** is an intentional contract published for separately evolving consumers. Its owner should decide when the fact is authoritative and publish only information consumers genuinely need. An event notification may say that an order was accepted and provide an order ID; event-carried state may also include an approved snapshot for consumers that cannot afford a subsequent query. Neither should leak private persistence structures, secrets, unnecessary personal data or a mutable domain object. Consumers own their reactions, but cannot bypass the authoritative owner of the business state described.

For a significant public event, review the following fields by meaning rather than imposing a single mandatory envelope:

| Concern | Example semantics | Why it matters |
| --- | --- | --- |
| Type | OrderAccepted | Stable statement of a completed business occurrence, not a disguised command |
| Event ID | 93c... (opaque unique identity) | Distinguish one event from redelivery; avoid collisions and accidental ID reuse |
| Owner/source | Orders | Which bounded responsibility can assert this fact |
| Business ID | Order 123 | Relate event to business state, without using it as a unique delivery ID for every fact |
| Occurred/committed time | 14:01 UTC | Business time when the occurrence became authoritative |
| Published/enqueued time | 14:02 UTC | Transport time, which may differ after retries or outbox relay |
| Correlation ID | Checkout operation 456 | Relate work and diagnostics across components |
| Causation ID | PaymentAuthorized event 789 | Explain which operation or prior event triggered this fact |
| Contract version | 2 | Consumers recognize their supported payload semantics |
| Tenant context | Tenant A | Enforce isolation and business authorization without exposing extraneous tenant data |
| Payload | Approved order summary | Minimize sensitive information and avoid private domain assemblies |

An event **identity** differs from a business entity ID: one order may produce several different meaningful events. Event timestamps must not silently imply global order, exactly-once processing or a successful downstream business outcome. Treat immutable published events as historical facts; publish a correction or new fact when necessary rather than mutating retained history.

### Event contract evolution and consumer independence

For meaningful independently consumed events:

1. Identify the owner of type names, field meanings, units, identifiers and stability promises.
2. Decide which fields are required, optional or nullable, and how absent/unknown fields are handled.
3. Define backward compatibility (new consumers reading old payloads) and forward compatibility (old consumers reading new payloads) for the actual serialization and validation rules. Adding an optional field may be compatible, but renaming a required field or changing its meaning usually is not.
4. Decide how unsupported versions are rejected, quarantined, translated, reprocessed or migrated; never silently interpret an incompatible version as valid business data.
5. Account for historical retained events and replay after contract evolution, including coexistence of multiple consumer versions and deprecation/retention windows.
6. Make the contract discoverable through suitable docs, source ownership or published schemas; use generation/registries where independent producers and consumers make them valuable.
7. Validate contracts and translations independently of mutable producer domain assemblies; provider/consumer contract verification should check both sides where the risk matters.

A shared contracts package can be useful, but it should define actual published contracts rather than force all services to reference the same internal entity project. CloudEvents, JSON Schema, Avro, Protobuf or a registry can be selected based on interoperability and governance needs; none is required for every message. Microsoft's [Event Hubs schema-registry concepts](https://learn.microsoft.com/en-us/azure/event-hubs/schema-registry-concepts) illustrate backward/forward modes with format-specific limitations; [Event Grid schema guidance](https://learn.microsoft.com/en-us/azure/event-grid/event-schema) describes CloudEvents as a useful standard for that Azure service. Do not transfer one provider's compatibility guarantee to an unrelated broker.

### Publishing relative to a transaction

Consider an Orders component writing an accepted order and announcing OrderAccepted:

| Approach | Critical failure window | Interpretation |
| --- | --- | --- |
| Publish before commit | Event delivered but order write rolls back | A consumer observed a fact that never became authoritative; avoid this for committed-fact integration events |
| Commit, then publish directly | Order commits but publisher crashes or broker rejects event | Consumers may never learn of the order; use only when this loss is acceptable or safely reconciled |
| Persist business state and outbox record atomically, then relay | Relay can stop or resend after ambiguous acknowledgment | Durable publication intent survives, but relay monitoring, retry, consumer deduplication and cleanup remain necessary |
| Dispatch synchronous in-process domain handlers within a local transaction | A handler fails and can roll back the transaction if actually enlisted | Valid when the transaction mechanism truly covers the changes; external network side effects are not made atomic merely by calling inside a transaction |
| Dispatch after commit without durable recording | Process can stop before callback runs | Acceptable only when missed reactions are harmless or another reliable recovery path exists |

An outbox helps with the **database commit versus external publication gap** only when the record and business update participate in the same actual atomic transaction; the relay must eventually publish/retry and operations must detect a stuck backlog. A database change feed or other mechanism may be appropriate if its actual guarantees are verified. An inbox/deduplication record can coordinate consumer-side effects when the deduplication marker and affected business write have a suitable shared atomic boundary. An external payment or email may still require its own idempotency protocol. See Microsoft's [outbox guidance](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos) and [Idempotent Consumer pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/idempotent-consumer).

Where a rule requires strict atomic consistency (for example, "confirm an order only if inventory is reserved"), retain the rule in one supported transaction boundary or use an authoritative synchronous operation that can return a verified outcome. A mere OrderRequested event is not proof stock has been reserved. If eventual consistency is intentionally chosen, expose a pending status and define the acceptable delay, conflict path and customer-visible result.

### Delivery is not the same as business effects

- **At-most-once:** A message may be lost but is not redelivered by the selected mechanism. Appropriate only if occasional omission is acceptable.
- **At-least-once:** A message can be delivered again after failure, lost acknowledgment, restart or retry. Consumers must assess duplicate consequences.
- **Exactly-once claims:** Read the product-specific scope closely (for example, duplicate sends within a retention window, or a transactional operation within one platform). Neither message acceptance nor a transport guarantee establishes exactly-once payment, email, inventory update or other external business effect.

Microsoft's [Service Bus delivery guidance](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-message-loss-and-duplicates) explains at-most/at-least-once tradeoffs; its [AMQP protocol guide](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-amqp-protocol-guide) documents limits of exactly-once transfer and duplicate detection. The specific broker and configuration must be verified before applying those semantics to an implementation.

#### Failure-oriented consumer scenarios

| Input or failure | Consequential question | Proportionate options |
| --- | --- | --- |
| Same event twice | Will the second invocation double-charge, send duplicate mail or write conflicting state? | Stable event ID, durable idempotency marker, business idempotency key, atomic effect/deduplication |
| Two consumers process concurrently | Can both claim the same work or violate ordering/invariants? | Unique constraints, optimistic concurrency, partition/lease ownership, per-key serialization if needed |
| Events out of order | Would an older status overwrite a newer one? | Version/sequence checks, per-key ordering, state-machine validation, reconciliation |
| Ordering within partition but not across partitions | Is globally ordered behavior actually required? | Co-locate related keys, merge by explicit version, or redesign the invariant |
| Event arrives long after occurrence | Is the action still relevant, authorized and permitted? | Requery authoritative state, expiry policy, obsolete-event handling |
| Referenced entity no longer exists | Is it legitimately deleted, moved, inaccessible or inconsistent? | Explicit no-op/reject/reconcile behavior; never recreate blindly |
| Unsupported schema version | Will deserialization reject safely? | Compatibility rules, quarantine/DLQ, version migration or operator repair |
| Business action already completed | Is repeat processing safe and semantically correct? | Idempotent business transition and explicit already-complete outcome |
| Persistent poison message | Does retrying forever block useful work? | Bounded retries, poison classification, DLQ/quarantine, alert and documented repair |
| Producer send times out | Might send have succeeded without acknowledgment? | Stable publication ID, safe resend, outbox and reconciliation |
| Consumer crashes before ack | Might the effect already have committed? | Atomic effect/deduplication, safe redelivery, do not ack before consequential work completes |
| Network partition or extended outage | Can backlog survive and be processed within business time targets? | Durability/retention, backpressure, expiry, catch-up capacity, recovery plan and monitored lag |
| Event replay or bulk reprocessing | Could old data trigger repeat external side effects or bypass present authorization? | Replay modes, business idempotency, access checks, controlled cutover and audit |

Transport acknowledgment confirms only the transport stage. Business completion may require a separate persisted state, confirmation message, reconciliation query or explicit user-visible status. Ordering can be **partition-local**; retrying or dead-lettering and replay can alter observed order. Treat message retention and expiry as business correctness decisions when lost or late work matters. Microsoft's [Event Grid retry guidance](https://learn.microsoft.com/en-us/azure/event-grid/delivery-and-retry) illustrates redelivery, non-guaranteed ordering, configurable retry windows and potentially dropped events without dead-letter handling; do not assume the same defaults for other services.

### Long-running workflows, sagas and irreversible effects

For multi-step fulfillment, separate each locally authoritative state transition from the overall workflow state. Suppose an order is accepted, inventory is reserved, payment is captured and shipment is arranged:

- An orchestration or process manager may track each step and correlate messages where a long-running, independently committed workflow makes that helpful.
- Choreography can fit modest independent reactions but may obscure responsibility for end-to-end completion if no one owns the business outcome.
- A saga coordinates local transactions with conditional compensating actions, not an automatic global atomic rollback. An email cannot be unsent; a shipment might not be recalled; a payment reversal may have independent costs or constraints.
- If one transaction can legitimately protect a critical invariant within a single owner or deployment, it may be simpler and more correct than splitting the invariant into events.

Define completion, failures, timeouts, reconciliation, who may retry a business action, and when human intervention is required. Microsoft's [Saga pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga) explains distributed local transactions and compensation tradeoffs.

### Security, privacy and consumer authorization

Treat the broker, transport, published payload, producer and consumer as actual trust boundaries, not automatically trusted internal infrastructure:

1. Authenticate legitimate producers and consumers using the deployment's supported service identity or credential mechanism.
2. Restrict publish, subscribe, manage and replay permissions independently. Do not grant all services administrative broker access.
3. Enforce business/resource authorization inside the consumer when the message could trigger a privileged state change. Transport acceptance does not establish that the caller or tenant is allowed to perform the requested operation.
4. Carry only necessary tenant context and verify tenant-to-resource relationships in the authoritative application. Shared queue/topic access may otherwise mix tenant information.
5. Minimize sensitive payloads and telemetry. Consider encryption in transit, at rest, integrity/authenticity, appropriate key/secret rotation, data retention and deletion obligations.
6. Consider malicious, forged, stale or replayed messages; signature validation, nonce/time windows or other replay defenses may be warranted for exposed or sensitive ingress.
7. Review audit and incident-response requirements, retention of dead letters/backups, and dependencies and supply-chain risks.

A broker's role-based access control and an application's authorization rules solve different problems. Microsoft's [secure messaging](https://learn.microsoft.com/en-us/azure/service-bus-messaging/secure-service-bus) and [multitenancy](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/service/service-bus) documentation illustrate both platform permission controls and the need for application-aware isolation; their particular Azure identities are not playbook mandates.

### Operational signals and recovery responsibility

For business-consequential flows, identify the **owner of the outcome**, the person/team responsible for incident response, and how to detect:

- Producer failure to persist or publish, aged outbox rows and ambiguous sends.
- Queue depth, age of oldest message, consumer lag, throughput/backpressure and partition hot spots.
- Retry attempts, poison messages, dead-letter count, schema errors and expired/undeliverable messages.
- Correlated producer-consumer traces, causation of downstream actions and where processing stalled.
- End-to-end business completion latency, mismatched state, duplicate business attempts and required reconciliation.
- Replay/reprocessing progress, outage recovery limits, retention/storage costs and sensitive diagnostic leakage.

Technical success (broker accepted message, consumer acknowledged) is not equivalent to business success (order fulfilled, payment settled). Select alerts and dashboards whose thresholds correspond to meaningful consequences and whose operators can actually act. Provider health signals and app-level business signals are complementary; no specific telemetry system is required. Microsoft's [Service Bus Well-Architected guidance](https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-service-bus) offers examples of backlog, latency and dead-letter monitoring.

## Level 3 — Review, verify and modernize

### Risk-based evidence selection

| Property or scenario | Design/unit/component evidence | Higher-fidelity evidence when consequential |
| --- | --- | --- |
| Meaningful domain occurrence and permitted/rejected transitions | Business behavior tests independent of broker | Persistence/concurrency tests for actual invariant enforcement |
| Producer chooses right fact and payload | Producer tests, mapping review, serialization round-trip | Real persistence and outbox publication/integration tests |
| Consumer reacts correctly, including already-completed state | Consumer tests with duplicate, delayed and malformed inputs | Real state store and effect/deduplication transaction |
| Public contract compatibility | Schema fixtures, backwards/forwards decoding, consumer-driven contract tests | Provider verification against actual publisher/serializer and retained versions |
| Broker delivery, lock, order, retention or DLQ | Review declared settings and assumptions; mocks useful for decisions | Representative broker with the actual configuration, failure/restart and redelivery |
| Atomic business write and publication intent | Source/transaction review and local behavior tests | Database transaction/outbox integration with rollback and relay failure |
| Consumer security/tenant isolation | Authorization policy/source tests and negative scenarios | Real entry-path credentials, broker permissions and tenant isolation probes |
| Workflow completion after partial failure | State-machine tests, compensation decision review | Representative multi-component recovery and reconciliation exercise |
| Observability, throughput and outage recovery | Instrumentation/configuration review | Deployed traces, metrics, alerts, delayed backlog and recovery/load observations |

Use [STD-001](standards/engineering-principles.md#std-001) for test-first executable changes and [STD-009](standards/testing.md#std-009) for consequential real external-adapter behavior. A provider-validated contract can establish its checked contract scope; it does not automatically verify a real broker's runtime delivery or a full deployment. Test doubles are useful for deterministic logic, but they do not prove network behavior, atomicity or actual authorization.

Tests for **every** timing, loss, retry, partition and disaster scenario are not universal. Select meaningful business risks, record actual environments, toolchains, broker/database versions, configuration, commands, outcomes and unverified properties. For this **documentation-only playbook issue**, review meaning, sources, links and cross-standard consistency; do not claim examples were compiled, a broker was exercised, or operational guarantees observed.

### Review scenarios, not a universal questionnaire

- An order-accepted event is published but its business transaction rolls back: could a consumer act on a false fact?
- A completed order is committed, but the sender crashes before broker acknowledgment: is a consequential notification lost or duplicated?
- Two consumers restart and receive the same payment-related event: what ensures one authorized business effect?
- A stale InventoryAdjusted event arrives after an item is discontinued: does the consumer enforce current domain and authorization rules?
- A rolling deployment has both old and new consumers: can both read the messages retained during the compatibility window?
- A tenant-scoped event arrives through a shared topic: does the consumer independently validate the resource belongs to the tenant?
- A six-hour outage produces a backlog: how will operators distinguish healthy catch-up from missed business deadlines?
- An old event is replayed for rebuilding a read model: could it accidentally resend customer mail or re-run payment capture?

Each review should identify one concrete risk and relevant evidence, not impose every optional pattern at once.

### Incremental modernization and platform constraints

1. Inventory existing direct calls, domain events, integration contracts, transaction boundaries, jobs, message consumers and business ownership.
2. Characterize meaningful success/failure and public compatibility behavior before moving implementation or publishing a new event.
3. Select **one justified flow**—for example, a durable post-commit notification—without requiring an application-wide conversion, new service or separate database.
4. Introduce the smallest compatible producer/consumer contract and mechanism, preserve existing public behavior, and explicitly manage migration/dual-processing windows if needed.
5. Verify actual failure cases with available supported dependencies; establish monitoring and recovery ownership before relying on asynchronous outcomes.
6. Reassess whether increased complexity still pays for itself; a simpler synchronous path or a modular monolith may remain the preferred long-term architecture.

Apply these steps to traditional .NET Framework, non-SDK projects, supported C# language levels, modern SDK-style .NET, Windows-only components, on-premises or hybrid installations without imposing modern language syntax, hosting APIs or a cloud product they cannot support. Microsoft's [.NET Standard overview](https://learn.microsoft.com/en-us/dotnet/standard/net-standard) can inform library compatibility, but actual package/framework/OS support and build/test behavior must be verified for the target system. Existing published contracts and security requirements survive any architecture change.

### Relationship to neighboring architectures

| Approach | What it answers | What it does not imply |
| --- | --- | --- |
| [Single-project](single-project-guidance.md) | How to keep a cohesive implementation proportionate in one compiled project | Events, broker or distributed deployment |
| [Layered and N-tier](layered-n-tier-guidance.md) | Logical responsibility layering versus physical tiers | Event-driven messaging or one event per layer |
| [Hexagonal](standards/hexagonal.md#std-012) | Explicit ports/adapters when adopted, protecting application interaction boundaries | A broker, event bus or automatically adopted EDA |
| [Clean](standards/clean.md#std-013) | Inward compile-time dependency direction for the adopted Application Core | CQRS, event sourcing or an asynchronous transport |
| [DDD](standards/ddd.md#std-014) | Bounded-context language, domain model, invariant and event meaning | Every domain event is a published integration event |
| [Modular Monolith](standards/modular-monolith.md#std-015) | Coherent module ownership and controlled in-process collaboration | Independent deployment, external broker or eventual consistency |
| [Vertical Slice](standards/vertical-slice.md#std-016) | Feature/use-case cohesion and change locality | Mediator, handler-per-event, async messages or CQRS |
| [Microservices](standards/microservices.md#std-017) | Independent deployment, operations, service ownership and distributed boundaries | Universal use of asynchronous messages or event-driven design |
| [Event-Driven Architecture](standards/event-driven.md#std-018) | Accountable material event-mediated contracts, processing and recovery | Any of the other styles, event sourcing, CQRS or separate databases |

STD-011's business-policy dependency rule applies whichever interaction is selected. When Hexagonal and/or Clean are explicitly adopted, their own port/interface and Application Core rules apply independently. Keep the domain decision independent of a messaging SDK; adapters and composition can implement the chosen transport.

## Source and verification boundary

This guide synthesizes Microsoft's documented patterns and the playbook's explicit proportionality policy. It contains **decision examples and failure analyses**, not executed C# programs, a deployable messaging application, measured throughput, broker integration results, or proof that a particular product guarantees business outcomes. Consult product/version-specific primary documentation and verify real project behavior before claiming compatibility, delivery, consistency, security or resilience.

Primary Microsoft references:

- [Event-Driven Architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven)
- [Publisher-Subscriber pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/publisher-subscriber)
- [Asynchronous Messaging Options](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/messaging)
- [Domain events: design and implementation](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation)
- [Implementing integration events](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/multi-container-microservice-net-applications/integration-event-based-microservice-communications)
- [Idempotent Consumer](https://learn.microsoft.com/en-us/azure/architecture/patterns/idempotent-consumer)
- [Transactional Outbox](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos)
- [Saga pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga)
- [Event Sourcing pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- [Message loss and duplicates](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-message-loss-and-duplicates)
- [Event Grid delivery and retry](https://learn.microsoft.com/en-us/azure/event-grid/delivery-and-retry)
- [Schema Registry concepts](https://learn.microsoft.com/en-us/azure/event-hubs/schema-registry-concepts)
- [Secure Service Bus](https://learn.microsoft.com/en-us/azure/service-bus-messaging/secure-service-bus)
- [Service Bus multitenancy](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/service/service-bus)
- [Service Bus Well-Architected guidance](https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-service-bus)
