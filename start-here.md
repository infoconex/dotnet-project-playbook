# Start here: use the .NET Project Playbook

Use this document as the entry point when asking an AI assistant to establish a new .NET project, assess an existing repository, or plan and carry out authorized improvements. It describes a provider-neutral, interactive process. It is not an installed agent, generator, or executable command; see the [current capabilities](README.md#current-state) before making implementation claims.

Engineering-foundation discovery is the primary workflow. Detailed application-feature discovery is a separate, optional second phase, offered when useful rather than assumed. A developer can finish after the foundation proposal without supplying an exhaustive feature specification.

This is guidance for **using** the playbook. The root [AGENTS.md](AGENTS.md) and [contribution guide](CONTRIBUTING.md) also govern work **on this repository**; they are not consumer-project templates. A target repository's own instructions and authorization remain applicable.

## Establish the request

1. Read the [engineering principles](docs/standards/engineering-principles.md), [initial standards catalog](docs/standards/README.md), and [standards governance](docs/governance/standards.md). Consult the [architecture decision](docs/decisions/0001-ai-first-playbook-architecture.md) and [template model](docs/architecture/template-model.md) as the request requires. Standards determine obligations; examples illustrate decisions but do not define universal requirements.
2. Determine the objective: establish a new project, assess an existing repository, implement approved changes, or reassess against current playbook guidance. If the developer has already stated the objective, do not ask again.
3. Establish the authorized mode and access to the relevant repository. An assessment or simulation is read-only. Do not assume that a target repository or its configuration is accessible, and do not interpret a request for advice as permission to make changes.

## Interactive question format

- Ask **exactly one decision question per turn** and wait for the developer's answer before asking another. Do not disguise several questions as subparts of one. Skip questions already answered or resolved by available project evidence.
- When a question has meaningful alternatives, offer a small set of mutually exclusive, clearly labeled choices. **Prefer separate, tappable choice cards when the AI client supports them.** Each card should have a short action-oriented title and a concise description of its purpose or tradeoff. Show a prominent **Recommended** label on the justified preferred card, and let selection submit that answer when supported. Never present decorative controls that appear clickable but have no action. If choice cards are unavailable, use another native interactive control (such as buttons or a choice picker); if no interactive control is supported, use easy-to-reply-to labeled choices such as A, B, and C. Always allow a free-text alternative. These are experience preferences, not requirements for a particular AI provider or visual layout.
- **Identify a recommended option** when the known requirements support one. Label it **Recommended**, preferably first, and briefly explain why it fits, including the most relevant tradeoff. A recommendation is not authorization to implement. If the available evidence does not justify a recommendation, say what is uncertain and ask for the one missing detail needed.
- Keep wording concise and neutral. Adapt each next question to the preceding answer and observed evidence; do not administer a fixed questionnaire or request information already provided. Present known, applicable foundation defaults as a group before asking whether the developer wants to change any of them; do not turn each default into a separate question.

## Phase 1: establish or assess the engineering foundation

- For **new projects**, establish only enough application context to select relevant engineering foundations: a brief purpose, project type, language/framework, supported platforms, and material constraints such as security, deployment, or distribution. Ask for missing details when they affect a foundation decision; do not begin a full feature or requirements interview in this phase.
- For **existing repositories**, first inspect actual source, project files, dependency configuration, tests, workflows, conventions, and documented decisions when access is authorized. Distinguish observed evidence from assumptions. Use the current repository as the baseline, not a hypothetical new-project template. If it cannot be inspected, identify what remains unknown.
- Present the applicable **Required**, **Recommended**, and **Optional** engineering standards and known defaults together, with brief reasons and explicit applicability. Distinguish established normative guidance from proposed settings, unavailable reusable assets, and project-specific choices. The [initial standards catalog](docs/standards/README.md) indexes the practices currently registered; each linked standard owns its detailed normative expectation, while the [engineering principles](docs/standards/engineering-principles.md) remain the baseline. A comprehensive domain catalog, executable defaults, and consumer templates are not yet provided.
- Highlight decisions that depend on the language, framework, project type, platform, existing conventions, or actual constraints. Do not invent defaults for these choices or require every user to answer an exhaustive checklist. Explain material compatibility conflicts and alternatives.
- After presenting the foundation defaults, ask **one question** about whether the developer wants to change anything. Use the [interactive question format](#interactive-question-format), including an evidence-backed recommendation and reason when justified. If the developer requests changes or a necessary choice remains unresolved, address each material decision one at a time.
- For existing repositories, compare the observed foundation against applicable standards, respect intentional exceptions, and ask about ambiguous differences before labeling them defects. Do not treat every difference from the playbook's preferred starting point as noncompliance.
- Apply SOLID and test-first development as described in the [engineering principles](docs/standards/engineering-principles.md). Prefer logical Ports and Adapters boundaries when helpful, but do not impose additional compiled projects without a responsibility-based reason. For cohesive libraries and small applications, consult the [proportionate single-project guide](docs/single-project-guidance.md) to distinguish logical responsibilities, compiled projects, and deployment without adopting a new standard.
- When meaningful business rules, differing business meanings, or important consistency boundaries emerge, assess conditional [Recommended DDD (`STD-014`)](docs/standards/ddd.md#std-014) in that context. Prefer a documented simple design for straightforward CRUD/pure utilities; do not impose aggregates, events, or physical projects universally. Offer the [on-demand DDD guide](docs/ddd-guidance.md) when useful, without making the refresher part of every setup.
- Assume that developers already understand SOLID; do not require a principle-by-principle tutorial during normal foundation discovery. When clarification is requested, use the [on-demand SOLID guide](docs/solid-guidance.md) for a quick refresher, practical C# examples, or a deeper discussion appropriate to the request. Keep [STD-010](docs/standards/solid.md#std-010) authoritative for the actual Required obligation.
- Account for modern .NET and traditional .NET Framework differences. For technical decisions depending on platform behavior, research applicable authoritative guidance before identifying what still requires project-specific verification.

## Propose the engineering foundation

After sufficient **foundation** discovery, provide a concise, reviewable proposal before any optional feature-discovery phase. It should identify:

1. The objective, known application context, applicable foundation defaults, project-specific choices, unresolved questions, and any assumptions.
2. Applicable standards and exceptions, with links to their authoritative sources.
3. The engineering project structure, files, configuration, or changes that **would** be introduced or adjusted, and why. Keep detailed product features outside this foundation proposal unless they materially affect its decisions. Distinguish canonical assets that actually exist from proposed or custom-created content.
4. Compatibility constraints, conflicts between selected capabilities, and choices requiring developer input. Do not silently resolve material conflicts.
5. Verification appropriate to the changes: relevant restore, build, tests, static checks, and environment-specific checks as applicable. Prefer repository-owned scripts callable locally and from CI **when such scripts exist**. Never report a planned check as a passing check.

The proposal is not implementation authorization. In read-only mode, describe intended actions without creating repositories, files, branches, issues, or pull requests.

## Phase 2: offer optional application-feature discovery

Once the foundation proposal is reviewable, decide whether detailed application discovery would add value. This is **secondary** to the engineering foundation, not a prerequisite for proposing it.

- For a **new application**, offer one clear opt-in question, such as "Would you like to continue with detailed application-feature discovery?" Recommend proceeding when substantial behavior or requirements remain undefined, explaining why; allow the developer to stop with the foundation proposal or return later.
- For an **existing repository**, first use its documented and implemented capabilities. Do not automatically restart requirements discovery. Offer targeted feature discovery only when the developer requests it or observed gaps, intended feature changes, or unresolved behavior make it useful. It may be unnecessary for a foundation-only assessment.
- If the developer opts in, explore appropriate capabilities, functional and nonfunctional requirements, acceptance scenarios, and feature boundaries, **one question at a time**. Reuse known facts and adapt the depth to the project; do not require a fixed-length questionnaire.
- If feature discovery reveals a material engineering constraint (for example, security, persistence, platform, or reliability needs), return to the affected foundation choice, explain the impact, and seek any needed decision. Do not silently replace an approved default or repository-specific exception.
- If the developer declines or the second phase is unnecessary, finish the foundation outcome without manufacturing a feature specification. Neither phase authorizes implementation by itself.

## Implement or reassess only within authorization

When implementation is authorized, follow the target repository's governance, preserve unrelated work, use canonical playbook assets where available, and verify actual behavior. This repository's root `AGENTS.md` must not be copied as a consumer `AGENTS.md`; any future consumer instructions are separate, customizable assets.

If the next step needs an asset, tool, or validation capability not yet provided by this playbook, identify that boundary explicitly. Describe the work needed and ask for direction rather than inventing a purported playbook asset or implying that unverified automation ran. General-purpose tools or custom implementation may be proposed, but are not automatically playbook-provided functionality.

For later on-demand assessment, inspect the consumer's current files and decisions. No playbook-specific adoption manifest or continuous synchronization is required. Do not overwrite customizations merely because current playbook guidance differs; identify provenance and verification in the relevant change review when possible.

## Report what is known

Summarize the resulting foundation decisions and proposed or completed actions, noting whether optional feature discovery was completed, deferred, or unnecessary, alongside applicable standards, actual verification results, skipped or unavailable checks, and outstanding questions. Keep documented guidance, implemented assets, and experimentally verified behavior distinct.

The [README](README.md#current-state) describes what this playbook currently offers. Following this conversational process with an AI assistant does **not** itself establish that a dedicated adoption agent, templates, or executable validation have been implemented or tested.
