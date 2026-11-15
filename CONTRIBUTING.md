# Contributing to .NET Project Playbook

The repository documents engineering standards and will eventually distribute .NET starter templates. Begin with the [documentation index](docs/README.md), [engineering principles](docs/standards/engineering-principles.md), and [standards governance](docs/governance/standards.md).

## Change workflow

1. Reference a GitHub issue describing the problem, proposed outcome, and acceptance criteria. One issue should ordinarily have one pull request.
2. For substantive implementation issues, complete the [engineering kickoff](#engineering-issue-kickoff) and obtain approval of its consolidated scope before starting implementation. That approval authorizes implementation within the approved scope; no separate implementation approval is needed. Keep the kickoff proportional; routine, unambiguous maintenance can proceed without a formal kickoff when otherwise authorized.
3. After recording the approved kickoff in the issue body and dated comment (or confirming authorization for routine maintenance), immediately branch from current `main` using `issue/<number>-<short-description>`; do not commit directly to `main`.
4. Identify the authoritative document or template being changed. Preserve existing decisions and explain proposed exceptions explicitly.
5. For executable behavior, start with a meaningful failing test, implement the smallest solution, and refactor. Documentation-only edits do not need a behavioral test or a TDD exception.
6. Perform verification appropriate to the change, then open one PR using the [pull request template](.github/pull_request_template.md). Include applicable commands, actual results or manual review, exact SHA, and limitations; provide environment versions and CI links when applicable.
7. Obtain an explicit second-pass owner review. A merge, tag, release, or package publication requires its own authorization; a green CI run grants none of these permissions.

For significant platform, framework, library, dependency, or tooling decisions, follow the [evidence-based technical decision standard](docs/standards/engineering-principles.md#evidence-based-technical-decisions). Consult applicable existing guidance before designing an experiment; record remaining uncertainty, project-specific verification, and justified deviations in the issue or PR. Routine changes do not require a separate research artifact.

## Engineering issue kickoff

Before implementing a **substantive** engineering issue, conduct a kickoff to validate material technical direction and make the issue a reliable implementation contract. This applies to significant standards, architecture, behavior, reusable templates, validation, security, compatibility, or governance changes. Routine, unambiguous fixes (such as a broken documentation link) do not require a formal kickoff.

1. **Prepare:** Read the issue, applicable standards, existing decisions, repository evidence, and relevant authoritative technical guidance. Identify questions that could materially affect scope, design, implementation, or verification. Do not revisit settled choices without a reason.
2. **Ask:** Resolve one decision question at a time, using actionable interactive choices where supported and labeled text alternatives otherwise. Identify a recommended direction and explain its rationale and relevant tradeoffs when evidence supports one. Allow free-text responses. Do not manufacture questions to meet a quota.
3. **Review and approve:** Present the consolidated kickoff scope, acceptance criteria, implementation plan, and verification approach, including material decisions, alternatives, and any open questions. Obtain explicit owner approval of this outcome before modifying the issue's implementation scope. Approval also authorizes implementation within that scope.
4. **Update the issue:** Reflect approved choices in its objective, scope, constraints, acceptance criteria, and verification approach as applicable. The issue body remains the authoritative *current* implementation contract.
5. **Preserve the feedback:** Add a dated GitHub issue comment recording the material questions and answers, approved directions and rationale, alternatives considered, changes made to the issue, and decisions deferred. The comment preserves the kickoff history; it does not create a competing normative definition.
6. **Begin approved implementation:** After updating the issue and preserving the kickoff comment, immediately create the issue-specific feature branch, implement within the approved scope, commit at meaningful completion boundaries, verify, and open one PR for the required second-pass owner review. No further implementation approval is required. Kickoff approval does **not** authorize merging, tagging, releasing, or publication; each requires separate authorization, and branch protections and required checks must not be bypassed.

For a straightforward substantive issue with no material open choices, the kickoff may be a brief confirmation of the existing direction and a concise comment. If implementation reveals a new material decision or scope expansion, pause before proceeding beyond the approved scope, obtain owner direction, update the issue, and record the follow-up in a new comment. Proceed with any newly approved scope only after that approval is documented.

## Standards and exceptions

Every normative standard identifies applicability and one of **Required**, **Recommended**, or **Optional**. A change to a Required standard needs an explicit reviewed decision. Document meaningful tradeoffs in a [decision record](docs/decisions/README.md). Avoid duplicating normative wording or mutable status across other documents.

Keep the canonical template source separate from illustrative examples. When generator functionality is added, test its output rather than assuming a template source tree proves that generated projects work.

## Verification

The current foundation contains documentation and governance files, with no executable validator or CI workflow. Review proposed changes for accurate links, clear navigation, and consistency with the authoritative standards. Record what was reviewed and any limitations; do not report an unavailable check as passing.

When executable project templates or automation are introduced, add meaningful behavioral tests and locally reproducible verification. Where practical, CI should invoke the same repository-owned checks.

## Security

Report plausible vulnerabilities privately according to [SECURITY.md](SECURITY.md). Do not post secrets, sensitive test data, or exploitation instructions in public issues or pull requests.
