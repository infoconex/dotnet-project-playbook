# ADR 0002: AI-first interactive discovery and project adoption

**Status:** Accepted for the foundational design; implementation and validation are future work.

## Context

The original foundation emphasized reusable templates and generated .NET projects. The intended product also needs to guide developers through engineering decisions, assess existing repositories, and adapt a preferred baseline without presuming that every project has the same needs. The root `AGENTS.md` governs AI working with the playbook, whereas instructions generated for a consumer repository serve that consumer's needs.

The long-term direction is a technology-independent `project-playbook` with .NET as its first technology module. The current .NET-specific repository remains the development and validation location until a separately authorized consolidation.

## Decision

- **AI-first, interactive adoption:** Ask focused discovery questions, one at a time by default, using the owner's opinionated standards as initial recommendations. For existing repositories, inspect actual files and conventions before recommending changes.
- **Two supported workflow goals:** Establish new projects and assess or improve existing ones. Distinguish assessment-only requests from authorized implementation, and respect the consumer repository's own governance.
- **Explicit applicability:** Identify Required, Recommended, and Optional standards, project-specific choices, compatibility constraints, and unresolved questions before proposing changes.
- **Separate agent roles:** Root playbook agent instructions guide use and maintenance of the playbook. Future target-project `AGENTS.md` or provider-specific files are separate, customizable assets; do not copy the root file as a consumer template.
- **Provider-neutral authority:** Standards and reusable assets are authoritative. Optional agent-specific adapters may facilitate their use without duplicating normative guidance.
- **Flexible implementation:** Reuse canonical assets, existing platform tools, or .NET templates where appropriate. No custom installer or template engine is intrinsically required by the AI-first experience.
- **On-demand reassessment:** Rely on consumer repository contents and existing documentation rather than requiring a playbook adoption manifest. Ask about ambiguous differences and do not silently overwrite local choices. Record applicable asset revisions and verification in the implementation review when possible.

## Validation approach

The current foundation contains design and governance documentation, so review clarity, links, and normative consistency manually. Future executable assets should have meaningful behavioral checks. Validate the two adoption goals with disposable repositories and independently evaluated expected results; assess real repositories for practical relevance without changing them absent separate authorization. Cross-platform, build, security, and deployment claims require evidence for the environments and behavior actually tested.

## Alternatives considered

- **Template-generation-first:** Useful for parameterized boilerplate, but does not itself explain applicability or safely assess an existing project.
- **One generic `AGENTS.md` copied everywhere:** Confuses instructions for maintaining the playbook with project-specific engineering instructions.
- **Mandatory adoption manifest or continuous synchronization:** Adds consumer metadata and maintenance obligations that are unnecessary for the chosen on-demand assessment model.
- **Provider-specific copies of all standards:** Risks divergent normative expectations across AI tools.

## Consequences

Future issues must define practical interactive discovery, asset composition, and acceptance scenarios separately from this documentation-only foundation. The accepted separation of standards, templates, validation, and examples in [ADR 0001](0001-playbook-boundaries.md) remains in force; this decision adds an explicit adoption responsibility without rewriting that earlier decision.
