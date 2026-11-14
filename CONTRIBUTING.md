# Contributing to .NET Project Playbook

The repository documents engineering standards and will eventually distribute .NET starter templates. Begin with the [documentation index](docs/README.md), [engineering principles](docs/standards/engineering-principles.md), and [standards governance](docs/governance/standards.md).

## Change workflow

1. Reference a GitHub issue describing the problem, proposed outcome, and acceptance criteria. One issue should ordinarily have one pull request.
2. Branch from current `main` using `issue/<number>-<short-description>`; do not commit directly to `main`.
3. Identify the authoritative document or template being changed. Preserve existing decisions and explain proposed exceptions explicitly.
4. For executable behavior, start with a meaningful failing test, implement the smallest solution, and refactor. Documentation-only work should explain why a behavioral red test does not apply.
5. Perform verification appropriate to the change, then open one PR using the [pull request template](.github/pull_request_template.md). Include applicable commands, actual results or manual review, exact SHA, and limitations; provide environment versions and CI links when applicable.
6. Obtain an explicit second-pass owner review. A merge, tag, release, or package publication requires its own authorization; a green CI run grants none of these permissions.

For significant platform, framework, library, dependency, or tooling decisions, follow the [evidence-based technical decision standard](docs/standards/engineering-principles.md#evidence-based-technical-decisions). Consult applicable existing guidance before designing an experiment; record remaining uncertainty, project-specific verification, and justified deviations in the issue or PR. Routine changes do not require a separate research artifact.

## Standards and exceptions

Every normative standard identifies applicability and one of **Required**, **Recommended**, or **Optional**. A change to a Required standard needs an explicit reviewed decision. Document meaningful tradeoffs in a [decision record](docs/decisions/README.md). Avoid duplicating normative wording or mutable status across other documents.

Keep the canonical template source separate from illustrative examples. When generator functionality is added, test its output rather than assuming a template source tree proves that generated projects work.

## Verification

The current foundation contains documentation and governance files, with no executable validator or CI workflow. Review proposed changes for accurate links, clear navigation, and consistency with the authoritative standards. Record what was reviewed and any limitations; do not report an unavailable check as passing.

When executable project templates or automation are introduced, add meaningful behavioral tests and locally reproducible verification. Where practical, CI should invoke the same repository-owned checks.

## Security

Report plausible vulnerabilities privately according to [SECURITY.md](SECURITY.md). Do not post secrets, sensitive test data, or exploitation instructions in public issues or pull requests.
