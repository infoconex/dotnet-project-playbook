# ADR 0001: Separate standards, templates, validation, and examples

**Status:** Accepted for the foundational design.

## Context

The playbook must be both a reliable source of .NET engineering practices and an eventual way to create new repositories. Copying the entire .NET Binary Tools project would bake in CLI, Native AOT, .NET 11, and binary inspection assumptions. Maintaining unrelated duplicate configurations would create drift.

## Decision

Separate four concerns:

- **Standards** define authoritative expectations and rationale, with explicit applicability levels.
- **Templates** provide a single canonical implementation of reusable starting assets and project profiles.
- **Validation** proves documented constraints and, eventually, generated project behavior using locally executable operations that CI orchestrates.
- **Examples** show real-world adoption while remaining project-specific and non-normative.

Adopt the [engineering principles](../standards/engineering-principles.md): SOLID and test-first development as broad expectations, a preference for Ports and Adapters, and physical compiled boundaries only when real responsibilities justify them.

Start with modern .NET templates when implementation begins; document legacy .NET Framework differences rather than forcing SDK-style or Native AOT assumptions onto every consumer. Avoid adding empty folders or placeholder configuration.

## Alternatives considered

- **Copy an existing project as the starter:** immediately supplies many files but carries project-specific structure and a false impression that unfinished features are validated.
- **One giant template for every project kind:** fewer visible artifacts but many mutually dependent options and a difficult acceptance matrix.
- **Independent copies of common files for each profile:** simple at first but risks configuration and security-policy drift.

## Consequences

Future template issues must define explicit composition and compatibility rules, test generated outputs, and provide versioned provenance. The foundational repository can be useful and accurate before an installable generator exists; documentation must always state which assets are implemented.
