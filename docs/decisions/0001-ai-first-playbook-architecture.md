# ADR 0001: AI-first engineering playbook architecture

**Status:** Accepted for the foundational design.

## Context

Developers need a repeatable way to establish new repositories and assess or improve existing ones using dependable engineering standards. The playbook must guide context-specific choices without assuming that every project needs the same files, structure, or tools. Copying an existing project such as .NET Binary Tools would introduce its CLI, Native AOT, .NET 11, and binary-inspection assumptions; maintaining independent copies of common configuration would create drift.

The initial scope is modern .NET and traditional .NET Framework, primarily C#. The longer-term direction is a technology-independent `project-playbook` with .NET as its first module. This repository remains the development and validation location until any consolidation is separately authorized.

## Decision

### AI-first adoption

- **Interactive discovery:** Guide developers through focused questions, one at a time by default, using the opinionated baseline as a starting recommendation. Inspect actual files and conventions before assessing an existing repository.
- **New and existing projects:** Support establishing new repositories, read-only assessment of existing ones, and implementation of separately authorized improvements. Respect the consumer repository's own governance.
- **Contextual standards:** Distinguish Required, Recommended, and Optional practices, compatibility constraints, documented exceptions, and unresolved questions before proposing changes.
- **Agent responsibilities:** This repository's root `AGENTS.md` guides use and maintenance of the playbook. Future consumer `AGENTS.md` templates and provider-specific adapters are separate, customizable assets and must not duplicate or redefine authoritative standards.
- **On-demand reassessment:** Infer applicable decisions from consumer files and existing documentation; do not require a playbook-specific adoption manifest or silently overwrite local choices. Ask about uncertain differences and record applicable asset revisions and verification in the change review when possible.

### Separation of responsibilities

Maintain four distinct concerns:

- **Standards** define authoritative expectations and rationale, with explicit applicability levels.
- **Reusable assets and templates** provide canonical implementations of starting files and project profiles, adapted to each consumer.
- **Validation**, when introduced, verifies applicable constraints and generated project behavior using locally executable operations that CI can orchestrate.
- **Examples** show real-world adoption while remaining project-specific and non-normative.

Adopt the [engineering principles](../standards/engineering-principles.md): SOLID and test-first development as broad expectations, a preference for Ports and Adapters, and separate compiled boundaries only when responsibilities justify them. Do not impose a fixed project graph on small applications.

AI should interpret the project context and adapt canonical assets; it is not itself the source of standards. Existing platform tools or .NET templates may assist implementation, but no custom installer or template engine is mandatory. Start with modern .NET project profiles when implementation begins and explicitly account for traditional .NET Framework differences rather than imposing SDK-style or Native AOT assumptions on every consumer.

## Validation approach

For this documentation-only foundation, review accuracy, links, and consistency manually without claiming an implemented agent or generator. Future acceptance must exercise both new-project creation and existing-repository assessment in disposable repositories with independent expected results. Assess real repositories for practical relevance without modifying them absent separate authorization. Verify generated assets through applicable restore, build, and test operations; substantiate cross-platform, security, packaging, and deployment claims only for behavior and environments actually tested.

## Alternatives considered

- **Copy an existing project or one giant template:** supplies initial files quickly, but imports project-specific assumptions or creates tightly coupled options and a difficult acceptance matrix.
- **Independent copies of common files:** initially simple, but risks configuration and security-policy drift.
- **Template-generation-first adoption:** useful for parameterized boilerplate but insufficient for contextual discovery and safe assessment of an existing repository.
- **Copy this repository's `AGENTS.md` to consumers:** confuses instructions for maintaining the playbook with those for an individual project.
- **Mandatory adoption manifests or automatic synchronization:** adds metadata and maintenance obligations beyond on-demand reassessment.
- **Provider-specific copies of standards:** risks divergent expectations across AI tools.

## Consequences

Future issues must define practical discovery guidance, asset composition and compatibility rules, meaningful acceptance scenarios, and versioned provenance. Keep examples non-normative, avoid empty placeholder folders and speculative configuration, and accurately distinguish planned capabilities from implemented, verified behavior. The foundation can be useful before an installable generator exists.
