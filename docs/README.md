# Documentation index

The playbook separates normative standards, their governance, architectural decisions, template implementation design, and examples.

| Area | Primary reference |
| --- | --- |
| AI-guided setup and assessment | [Start here](../start-here.md) |
| Registered engineering standards | [Standards catalog](standards/README.md) |
| Applying Microsoft's .NET testing guidance | [Testing guidance map](testing-guidance.md) |
| Playbook-specific testing standards | [Testing standards](standards/testing.md) |
| Applying Microsoft's C# guidance | [Microsoft C# guidance map](csharp-guidance.md) |
| Playbook-specific C# standards | [C# standards](standards/csharp.md) |
| SOLID design requirements | [STD-010 — SOLID standard](standards/solid.md#std-010) |
| Optional SOLID refresher and C# examples | [SOLID guidance](solid-guidance.md) |
| Business-policy dependency direction | [STD-011 — Dependency direction](standards/dependency-direction.md#std-011) |
| Optional dependency-boundary refresher and examples | [Dependency-direction guidance](dependency-direction-guidance.md) |
| Hexagonal (Ports and Adapters) architecture | [STD-012 — Hexagonal Architecture](standards/hexagonal.md#std-012) |
| Optional ports, adapters, and C# testing examples | [Hexagonal Architecture guidance](hexagonal-guidance.md) |
| Clean Architecture | [STD-013 — Clean Architecture](standards/clean.md#std-013) |
| Optional Application Core, dependency, and C# examples | [Clean Architecture guidance](clean-guidance.md) |
| Domain-Driven Design and Domain Modeling | [STD-014 — DDD standard](standards/ddd.md#std-014) |
| Optional strategic/tactical domain modeling and C# examples | [DDD guidance](ddd-guidance.md) |
| Modular Monolith Architecture | [STD-015 — Modular Monolith Architecture](standards/modular-monolith.md#std-015) |
| Optional module ownership, contracts, data, and verification examples | [Modular Monolith Architecture guidance](modular-monolith-guidance.md) |
| Vertical Slice Architecture | [STD-016 — Vertical Slice Architecture](standards/vertical-slice.md#std-016) |
| Optional feature cohesion, handlers/CQRS, and verification examples | [Vertical Slice Architecture guidance](vertical-slice-guidance.md) |
| Microservices Architecture | [STD-017 — Microservices Architecture](standards/microservices.md#std-017) |
| Optional service selection, data, deployment, security, and operational evidence examples | [Microservices Architecture guidance](microservices-guidance.md) |
| Choosing one production project versus multiple projects | [Proportionate single-project architecture guidance](single-project-guidance.md) |
| Logical layers versus physical N-tier deployment | [Traditional layered and N-tier architecture guidance](layered-n-tier-guidance.md) |
| Engineering principles | [Engineering principles](standards/engineering-principles.md) |
| Standards and exceptions process | [Standards governance](governance/standards.md) |
| Layout, naming, and initial configuration | [Repository organization](governance/repository-organization.md) |
| Template and project profiles | [Template architecture](architecture/template-model.md) |
| Architectural decision rationale | [ADR index](decisions/README.md) |
| AI-first architecture decision | [ADR 0001](decisions/0001-ai-first-playbook-architecture.md) |
| Reference implementation | [.NET Binary Tools](../examples/dotnet-binary-tools.md) |

The root [README](../README.md) describes current availability, and [start-here.md](../start-here.md) defines the interaction flow. [CONTRIBUTING.md](../CONTRIBUTING.md) governs repository changes; [AGENTS.md](../AGENTS.md) guides agents using or maintaining the playbook and is not a consumer-project template. Do not put scenario verification or release state in multiple navigation pages.

For a versioned, read-only conversational test of the entry point, see [Evaluate the playbook](evaluate-playbook.md). This test scenario is non-normative and does not replace executable acceptance tests.
