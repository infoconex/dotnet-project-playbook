# Planned AI-assisted adoption and template architecture

**Status: design only.** No AI discovery agent, existing-repository assessor, project generator, NuGet template package, consumer AI instruction template, profile, or reusable project asset has been published or verified yet. This document defines implementation boundaries for later issues.

## Asset ownership

| Asset | Responsibility |
| --- | --- |
| Root `AGENTS.md` | Provider-neutral guidance for agents helping use or maintain the playbook; not consumer-project instructions to copy. |
| `docs/` | Normative standards, adoption policy, and decisions. |
| `templates/` (future) | Canonical source for reusable project files, including a distinct, adaptable consumer `AGENTS.md` template when justified. |
| `scripts/` (future) | Reproducible validations and template packaging; focused script tests can live alongside scripts under `scripts/tests/`. |
| `tests/` (future) | Generated-output and integration acceptance checks. |
| `examples/` | Real-world decisions and evidence, without a second competing copy of template assets. |
| `.github/` | Governance for the playbook itself and, when justified, CI; not the entire consumer template catalog. |

Create a directory only when it contains meaningful assets. Do not duplicate one canonical `.editorconfig`, build configuration, or CI script in multiple consumer templates unless a documented compatibility difference requires it.

## AI-first adoption and assessment

The planned AI experience is an interactive workflow, not a requirement to build a custom installer or to copy the playbook's own agent instructions into a target repository.

1. **Establish context:** Obtain access to the playbook and target repository. Determine whether the task is new-project creation, assessment-only, or authorized implementation. Inspect existing repositories before proposing their redesign.
2. **Discover decisions:** Ask focused questions about application type, toolchain, architecture, constraints, and optional capabilities; ask one at a time by default. Use the playbook's opinionated baseline while allowing project-specific choices and justified exceptions.
3. **Evaluate and propose:** Apply standard applicability levels, identify existing compliance and meaningful differences, explain options and risks, and provide a reviewable plan. Do not silently classify ambiguous differences as errors.
4. **Apply within authorization:** If approved, compose reusable assets and project-specific structure without overwriting unrelated local conventions. Reuse existing tools and platform-supported generators where appropriate.
5. **Verify and report:** Run applicable behavioral and configuration checks, disclose unsupported checks, and record actual results and revisions in the change review. Offer on-demand reassessment as playbook standards evolve.

The authoritative standards are independent of the AI provider. Optional tool-specific adapters may explain how an agent locates the playbook or invokes a capability, but they must link to, rather than replicate, normative rules. No playbook-specific tracking file is required in a target repository; assessments infer state from its existing files and ask about unrecorded decisions.

## Planned composition

1. **Common repository foundation:** repository guidance, code style, basic security/contribution policy, and locally runnable quality checks.
2. **Project profile:** library, CLI, web API, worker, or other actual application type with appropriate compiled boundaries and tests.
3. **Optional capabilities:** Native AOT, NuGet distribution, additional infrastructure adapters, or specialized CI checks only when applicable.
4. **Platform/target compatibility:** modern SDK-style .NET by default; legacy .NET Framework requires its own validated build and toolchain guidance.

The standard .NET template engine is a candidate implementation tool for parameterized names, namespaces, and solution structures when practical and verified; it is not the required entry point for adoption. AI-guided composition and manual reuse can use the same canonical assets. GitHub repository templates may also provide a convenience entry point later, but should not create a competing definition of starter content.

## Consumer contract to verify

Two practical scenarios should shape future acceptance: **creating a new repository** from guided discovery and **assessing an existing repository** for applicable standards without altering it in assessment-only mode. Use disposable repositories and controlled expected outcomes for repeatable tests, supplemented by read-only assessment of real projects. Evaluate the relevance and clarity of AI recommendations through scenario review; use deterministic checks to verify implemented assets and behavior.

For generated profiles, future tests should use a non-default name, then verify output paths and namespaces, restore, build, execute relevant tests, enforce naming and architecture constraints, and test packaging or startup where relevant. Cross-platform claims require actual Windows, Linux, and macOS verification for the advertised profile. CI should call the same validation operations that developers can run locally.

Record relevant template versions and source revisions in the change proposal or review evidence when applying them, rather than requiring a new provenance manifest in every consumer repository. Document configuration choices that must be applied through GitHub settings, such as branch rulesets and secret scanning; copying a file alone does not activate those services.

Do not infer that a future capability works from the existence of this design or a review of documentation.
