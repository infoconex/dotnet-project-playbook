# Security policy

## Supported versions

This repository is an unreleased engineering playbook. No project template package or generated-product version has been published.

| Version | Security maintenance |
| --- | --- |
| `main` (unreleased) | Reports are evaluated; fixes are made through reviewed pull requests. |
| Published template versions | None yet; no release support commitment exists. |

## Report a vulnerability

Submit vulnerability reports privately through GitHub's [Report a vulnerability form](https://github.com/infoconex/dotnet-project-playbook/security/advisories/new). Private vulnerability reporting is enabled for this repository; reports are delivered to the maintainers without creating a public issue.

Do not publish secrets, exploit details, affected private data, or unredacted diagnostics in a GitHub issue or pull request. Include the affected revision, realistic prerequisites, impact, and a minimal synthetic reproduction in the private report. The maintainer will assess reports and coordinate appropriate remediation and disclosure; no fixed response-time promise is established.

## Security expectations

The repository's future templates and scripts will handle build inputs, package feeds, CI permissions, toolchains, and potentially untrusted project metadata. Review such boundaries for accidental command execution, unsafe file writes, leaked tokens, dependency risks, and overly broad workflow permissions. Requirements for future assets are **not claims that protections have already been implemented or verified**.
