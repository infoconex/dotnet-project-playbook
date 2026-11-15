# Start here: use the .NET Project Playbook

Use this document as the entry point when asking an AI assistant to establish a new .NET project, assess an existing repository, or plan and carry out authorized improvements. It describes a provider-neutral, interactive process. It is not an installed agent, generator, or executable command; see the [current capabilities](README.md#current-state) before making implementation claims.

This is guidance for **using** the playbook. The root [AGENTS.md](AGENTS.md) and [contribution guide](CONTRIBUTING.md) also govern work **on this repository**; they are not consumer-project templates. A target repository's own instructions and authorization remain applicable.

## Establish the request

1. Read the [engineering principles](docs/standards/engineering-principles.md) and [standards governance](docs/governance/standards.md). Consult the [architecture decision](docs/decisions/0001-ai-first-playbook-architecture.md) and [template model](docs/architecture/template-model.md) as the request requires. Standards determine obligations; examples illustrate decisions but do not define universal requirements.
2. Determine the objective: establish a new project, assess an existing repository, implement approved changes, or reassess against current playbook guidance. If the developer has already stated the objective, do not ask again.
3. Establish the authorized mode and access to the relevant repository. An assessment or simulation is read-only. Do not assume that a target repository or its configuration is accessible, and do not interpret a request for advice as permission to make changes.

## Interactive question format

- Ask **exactly one decision question per turn** and wait for the developer's answer before asking another. Do not disguise several questions as subparts of one. Skip questions already answered or resolved by available project evidence.
- When a question has meaningful alternatives, offer a small set of mutually exclusive, clearly labeled choices. Prefer the AI client's **native clickable selection controls** (such as buttons or a choice picker) when supported; otherwise use easy-to-reply-to labeled choices such as A, B, and C. Always allow a free-text alternative.
- **Identify a recommended option** when the known requirements support one. Label it **Recommended**, preferably first, and briefly explain why it fits, including the most relevant tradeoff. A recommendation is not authorization to implement. If the available evidence does not justify a recommendation, say what is uncertain and ask for the one missing detail needed.
- Keep wording concise and neutral. Adapt each next question to the preceding answer and observed evidence; do not administer a fixed questionnaire or request information already provided.

## Discover the project context

- For **new projects**, establish the intended capability and project type before choosing a solution shape, language version, target framework, operating systems, testing approach, or optional integrations. Ask about these details only when they affect a decision.
- For **existing repositories**, inspect actual source, project files, dependency configuration, tests, workflows, and documented decisions when access is authorized. Distinguish observed evidence from assumptions. If the repository cannot be inspected, identify what remains unknown rather than inventing a baseline.
- Apply **Required**, **Recommended**, and **Optional** practices according to their documented applicability. Identify intentional exceptions and ask about ambiguous differences before calling them defects.
- Apply SOLID and test-first development as described in the [engineering principles](docs/standards/engineering-principles.md). Prefer logical Ports and Adapters boundaries when helpful, but do not impose additional compiled projects without a responsibility-based reason.
- Consider compatibility between modern .NET and traditional .NET Framework. For technical decisions depending on platform behavior, research applicable authoritative guidance before identifying what still requires project-specific verification.

## Propose a project-specific outcome

After enough discovery, provide a concise, reviewable proposal that identifies:

1. The objective, known facts, chosen defaults, unresolved questions, and any assumptions.
2. Applicable standards and exceptions, with links to their authoritative sources.
3. The project structure, files, configuration, or changes that **would** be introduced or adjusted, and why. Distinguish canonical assets that actually exist from proposed or custom-created content.
4. Compatibility constraints, conflicts between selected capabilities, and choices requiring developer input. Do not silently resolve material conflicts.
5. Verification appropriate to the changes: relevant restore, build, tests, static checks, and environment-specific checks as applicable. Prefer repository-owned scripts callable locally and from CI **when such scripts exist**. Never report a planned check as a passing check.

The proposal is not implementation authorization. In read-only mode, describe intended actions without creating repositories, files, branches, issues, or pull requests.

## Implement or reassess only within authorization

When implementation is authorized, follow the target repository's governance, preserve unrelated work, use canonical playbook assets where available, and verify actual behavior. This repository's root `AGENTS.md` must not be copied as a consumer `AGENTS.md`; any future consumer instructions are separate, customizable assets.

If the next step needs an asset, tool, or validation capability not yet provided by this playbook, identify that boundary explicitly. Describe the work needed and ask for direction rather than inventing a purported playbook asset or implying that unverified automation ran. General-purpose tools or custom implementation may be proposed, but are not automatically playbook-provided functionality.

For later on-demand assessment, inspect the consumer's current files and decisions. No playbook-specific adoption manifest or continuous synchronization is required. Do not overwrite customizations merely because current playbook guidance differs; identify provenance and verification in the relevant change review when possible.

## Report what is known

Summarize the resulting decisions and proposed or completed actions, including applicable standards, actual verification results, skipped or unavailable checks, and outstanding questions. Keep documented guidance, implemented assets, and experimentally verified behavior distinct.

The [README](README.md#current-state) describes what this playbook currently offers. Following this conversational process with an AI assistant does **not** itself establish that a dedicated adoption agent, templates, or executable validation have been implemented or tested.
