# Security engineering and software supply-chain guidance

This is **non-normative, on-demand guidance** for choosing proportionate security controls in new .NET projects and assessing existing SDK-style, traditional .NET Framework, and mixed repositories. The authoritative playbook obligations are [STD-019–STD-021](standards/security.md), interpreted through [standards governance](governance/standards.md). Existing [engineering](standards/engineering-principles.md), [compiler/analyzer](standards/csharp.md#std-008), [external-boundary verification](standards/testing.md#std-009), and [build/dependency guidance](build-dependency-guidance.md) retain their independent scope.

**Sources reviewed:** November 15, 2026 (America/Los_Angeles). Tool availability, GitHub plan/organization/repository settings, language support, SDK and NuGet versions, and advisories may change. Recheck current vendor guidance for the **actual** target. This guide is documentation, not evidence that security products are enabled, any scan ran, or a target project is protected.

## Start from exposure and evidence

For a **new project**, learn its purpose, project kind, intended users, sensitive data, dependencies, hosting/release path, supported operating systems, and any known external exposure. Propose the smallest protection and review foundation that covers the realistic risks. Avoid a mandatory security questionnaire for a simple, offline, dependency-free utility. Ask only when an unknown materially changes the proposal.

For an **existing repository**, first inspect its project/solution files, package formats and sources, workflows, permissions, dependency visibility, security controls, secrets and logging conventions, deployment assumptions, and documented decisions. Distinguish what was **observed** from what could be inferred. An older project system, absent `dependabot.yml`, or disabled optional scanner is not automatically a defect: establish applicability, actual risk, alternatives, and existing compensating controls before proposing an incremental change.

| Context | Initial security focus | Conditional extension; do not assume by type alone |
| --- | --- | --- |
| Pure library | Released package/consumer trust, safe error behavior, third-party references, synthetic test data, publisher credentials when distributed. | No standalone web DAST or application authentication layer without a deployed web surface. Assess sensitive data if the library actually processes it. |
| CLI tool | Filesystem/process input, output redaction, optional network calls, package/tool distribution, build/release permissions. | Credential storage, OS-specific permissions, or signature/provenance controls when its actual use warrants them. |
| Web API | Authentication/authorization, input handling, request boundaries, logs, host/configuration secrets, exposed dependencies. | Threat models and dynamic testing for consequential exposure; no universal security framework or identical environment requirements. |
| Worker/background processor | Message/job trust, identity and data access, poison/error paths, retry logs, privileged deployment credentials. | Broker credentials, tenant isolation, and replay risks when those mechanisms exist. |
| Traditional .NET Framework | Supported MSBuild/NuGet paths, `packages.config` or PackageReference visibility, Windows build/runtime requirements, legacy credential and configuration patterns. | Use version-compatible advisory tools and incremental mitigations; modern SDK installation alone does not establish Linux/macOS buildability. |
| Mixed/modernizing solution | Per-project dependencies, inherited configuration, distinct CI/build paths, incompatible tools and runtime assumptions. | Stage controls by supported subsystem and verify all affected paths; do not enforce one scanner or target framework on the entire solution blindly. |

## Which obligation applies?

| Standard | Trigger | Evidence to seek | Not automatically required |
| --- | --- | --- | --- |
| [STD-019 — Secrets and sensitive-data protection](standards/security.md#std-019) | Credentials, tokens, keys, relevant sensitive data or pathways that could expose them; baseline no live secrets in commits. | Protected injection, access limits, redacted logs/tests, exposure handling, observed configuration and gaps. | A new vault product for a project with no runtime secrets; assuming user secrets secure production data. |
| [STD-020 — Dependency vulnerability management](standards/security.md#std-020) | Third-party packages/components, including relevant transitive, tool, or image inputs. | Known inventory/coverage, current advisory review, prioritized dispositions, mitigations and owners. | CPM, lock files, Dependabot config, fixed remediation-day SLAs, or paid SCA in every repo. |
| [STD-021 — Security-sensitive change review](standards/security.md#std-021) | Material changes to trust, identity, privilege, sensitive-data flows, exposed behavior, cryptography, or privileged build/deploy. | Review of change effects, threats, controls, verification, reviewer and residual risk. | Formal threat model, DAST, or penetration test for every PR. |

These obligations are distinct: protection addresses the *handling* of secrets/data; dependency management addresses *known risks in externally supplied components*; sensitive-change review addresses *new or changed security assumptions*. One piece of evidence can inform more than one standard, but a tool being enabled cannot substitute for their separate decisions.

## Secrets, sensitive data, and response

- **Development:** Use fake or synthetic credentials in examples and tests. ASP.NET Core [user secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets) separate local development values from source but are not encrypted production storage. Keep live tokens out of `.json`, `.props`, `.targets`, `nuget.config`, `packages.config`, logs, fixtures, generated files, and commit history.
- **Deployment:** Prefer protected environment configuration, workload identity, or an appropriate managed secrets store. Limit visibility to the processes and maintainers that need it; avoid broad reusable credentials and avoid passing secrets to untrusted build steps. The actual store depends on hosting environment, regulatory obligations, and operations.
- **Data:** Determine what data is sensitive *in this project*; evaluate authorization, validation, transport/storage protections, retention/deletion, diagnostic redaction, and export boundaries proportionately. Minimize collected data and avoid printing credentials or personal data in errors, trace logs, test recordings, or build artifacts. See [OWASP logging guidance](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).
- **Detection:** GitHub [secret scanning supported patterns](https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns) and [detection scope](https://docs.github.com/en/code-security/reference/secret-security/secret-scanning-scope) differ by secret type, repository configuration and feature availability. [Push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection) may block some supported patterns; it is not an all-secrets firewall. Inspect actual settings, supported languages/patterns, alert history, bypass controls, and reviewer process.
- **Incident:** For a suspected committed key, treat it as exposed even if the current file is cleaned. Contain its access, revoke or rotate as appropriate, investigate scope of use and artifact/log/history copies, follow private vulnerability reporting/incident procedure, and record mitigation/review. Avoid publishing the compromised value in tickets, PRs, and audit notes. [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) provides lifecycle practices.

Repository [`SECURITY.md`](../SECURITY.md) is the existing vulnerability-reporting route for **this playbook**; a consuming repository should inspect and honor its own security policy. A reporting file is not a secret store or proof that controls operate.

## Dependency security and update handling

Inventory **direct** references, **transitive** closure where the package format/tool supports it, build/release tools and other relevant supplied components. Review vulnerable version ranges, source trust, and package compatibility instead of equating a version bump with a fixed issue. When a dependency is not reached in the deployed path, record the evidence and remaining uncertainty; do not assume all advisories are exploitable or all unlisted versions safe.

| Capability | Where it helps | Important boundary to verify |
| --- | --- | --- |
| [NuGetAudit](https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages) | Vulnerability warnings in supported NuGet restore workflows. | Installed client, target project format, advisory-source accessibility, direct/transitive behavior and warning policy. .NET 10 changes [transitive audit defaults](https://learn.microsoft.com/en-us/dotnet/core/compatibility/sdk/10.0/nugetaudit-transitive-packages); never assume a legacy `packages.config` path has equivalent coverage. |
| [GitHub dependency graph](https://docs.github.com/en/code-security/reference/supply-chain-security/dependency-graph-supported-package-ecosystems) | Visibility for supported manifests and package ecosystems. | Actual detected manifests, generated dependencies, private or missing components, and branch/ref coverage. |
| [Dependabot alerts](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts) | Reports applicable advisories for recognized dependencies. | Current feature settings and detected graph; a clean alert queue does not cover every vulnerability or every input. |
| [Dependabot security updates](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-security-updates) | Proposed changes responding to eligible vulnerability alerts. | Whether enabled, eligible manifest/manager/graph, update restrictions, compatibility, review and test outcomes. |
| [Dependabot version updates](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates) | Scheduled routine version maintenance via configured `dependabot.yml`. | This is distinct from security updates; grouped routine PRs must not defer urgent remediation. Scheduling and grouping are project choices. |
| Lock files, CPM, package-source mapping | Controlling versions, coordinating PackageReference, or constraining sources in suitable projects. | See the [build/dependency guide](build-dependency-guidance.md). These are not substitutes for review of a vulnerable dependency and are not universal obligations. |

**Triage and remediation flow:**

1. Verify the reported package, affected and resolved ranges, applicable TFM/RID/project, direct/transitive path, and advisory credibility. Determine actual reachability or material exposure when feasible.
2. Prioritize based on exploit conditions, severity, data/privilege exposure, deployment, exploit availability, and the consequences of leaving the dependency in place. Do not apply an arbitrary severity-only universal deadline.
3. Prefer a compatible patched update, removal, or replacement; where impossible, identify mitigation and isolation. Do not suppress an audit warning without a recorded disposition.
4. Review resulting transitive resolution, package source/provenance, API/runtime compatibility, and relevant tests. Preserve the difference between restore success and actual application verification.
5. Record owner, decision, evidence, unresolved risk, review trigger, and follow-up. Expedite credible high-risk security changes independently of scheduled grouped maintenance PRs.

Use trusted feeds and least-privileged credentials. NuGet [configuration inheritance and package-source choices](build-dependency-guidance.md) are not automatically proof of package authenticity. Secrets in feed configuration should be protected, not stored as plaintext in the repository. For unsupported ecosystems or older .NET Framework tooling, document alternate advisory sources and the unassessed portions of the graph; lack of a compatible NuGetAudit mode does not imply lack of risk.

## Choose security verification by the question

| Activity | Question it can help answer | Limitation and applicability |
| --- | --- | --- |
| SAST / CodeQL | Are analyzable code patterns associated with known vulnerability classes? | Language/build support, query coverage, scan selection and actual result matter. It does not prove authorization, runtime deployment, or complete absence of bugs. |
| SCA / dependency audit | Are known advisories associated with recognized dependency versions? | Dependent on manifest/lock visibility, advisory completeness, direct/transitive scope and timing. |
| Secret scanning / push protection | Were certain recognizable credentials committed or about to be pushed? | Supported patterns and repo settings differ; may miss secrets and may be bypassed. |
| Threat modeling / security review | What assets, assumptions, trust boundaries, abuse cases or missing controls does a change introduce? | Human/context-sensitive reasoning; a diagram or checklist alone is not runtime verification. |
| DAST / dynamic probing | How does a **running** reachable application respond to classes of hostile inputs/configurations? | Requires safe representative environment, authorization, realistic identity/data boundaries; not normally meaningful for an offline pure library. |
| Boundary and integration tests | Does security-relevant behavior work with the real dependency or a provider-validated contract? | Tests demonstrate only exercised environments and paths; consult [STD-009](standards/testing.md#std-009). |
| CI/release provenance review | Were build privileges, artifact origin, inputs, and publishing paths appropriate? | Configuration inspection alone is not evidence of artifact reproducibility, signed provenance, or supply-chain integrity. |

GitHub's [CodeQL setup guidance](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning) distinguishes available setup mechanisms; inspect the **repository's actual languages, configured tools, latest analysis results and coverage**, not merely whether default setup was clicked. A repository with no supported analyzable code may have no CodeQL scans. Other SAST tools or manual review may be justified where CodeQL does not cover a particular language or project system. Do not require every SAST, SCA, DAST, penetration-testing, and threat-modeling tool for every small project. The [OWASP Web Security Testing Guide](https://wstg.owasp.org/) and [ASVS](https://asvs.owasp.org/) can inform suitably scoped web security checks.

### CI and contribution trust boundaries

Inspect workflow permissions, triggers, token scopes, secret availability, third-party Actions and build/publish steps. Use least-privilege permissions and reviewed publishers or pinned/controlled dependencies as appropriate. Especially distinguish trusted branches and maintainers from externally supplied pull-request content: [GitHub's `pull_request_target` guidance](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) cautions against running untrusted PR code with privileged credentials. Separate untrusted validation from credential-bearing release workflows when necessary. A green status check does not prove the workflow has safe permission boundaries, and this guide does not change any actual repository settings.

## Security-sensitive change review

For a material change under [STD-021](standards/security.md#std-021), review the *changed behavior*, not just a dependency diff or security label. Use the smallest record that is reviewable; this can live in an existing issue/PR. Expand to a structured [Microsoft threat-modeling](https://learn.microsoft.com/en-us/security/engineering/threat-modeling-with-dev-ops) exercise for consequential trust-boundary changes or non-obvious attack paths; consider STRIDE as a method, **not** a required framework. Focus DAST or specialist review where a safe running service and exposure justify it.

**Example review note (illustrative, not a required form):**

> **Change/boundary:** API endpoint now accepts cross-tenant resource IDs; authorization depends on the resolved tenant, not merely authentication.
>
> **Assets/threats:** Another tenant's records could be read through object-level authorization bypass. Error and audit logs must avoid sensitive record content.
>
> **Controls:** Tenant-scoped authorization after resource lookup, denial behavior, least-privileged data access, redacted logs.
>
> **Evidence:** List the exact tests executed with identity/tenant variants, environment and result; identify missing representative integration or DAST evidence if not run.
>
> **Owner/disposition:** Named reviewer, unresolved risk, acceptance/mitigation, and follow-up condition.

For a **privileged build/release change**, the analogous review covers who can trigger it, whether untrusted code can run, permissions and secrets available, artifact inputs and publisher access, and tested rollback/recovery. For a **library cryptography change**, it covers algorithm/key/lifecycle assumptions, interoperability, sensitive outputs and tests. A small internal rename that changes none of those assumptions does not need a speculative security review. Emergency review may be expedited only with a recorded owner, risk, containment and follow-up under [STD-021](standards/security.md#std-021).

## Adoption without unnecessary scaffolding

**New project:** Apply applicable Required standards first; identify whether the project genuinely has runtime secrets/sensitive data, third-party dependencies, or material security-sensitive changes. Recommend existing ecosystem capabilities that match its actual language, hosting and exposure. Add only the minimum justified configuration; do not create a security dashboard, vault, threat-model repository, scanner workflow or questionnaire by default.

**Existing project:** Inspect available evidence and distinguish an established safe alternative from a gap. Review actual security settings in GitHub separately from tracked files: a `SECURITY.md` file, `dependabot.yml`, workflow, or badge is not proof that corresponding features are enabled and functioning. Preserve security and compatibility obligations while proposing scoped, incremental upgrades. Do not infer Linux/macOS runtime or build support for traditional .NET Framework simply because .NET CLI tooling is installed.

**Verification and claims:** Use the following labels in a review or adoption report:

| Evidence state | Valid assertion | Invalid leap |
| --- | --- | --- |
| **Documented** | Official vendor documentation describes a feature and its prerequisites at the cited version. | “The target repository is protected by that feature.” |
| **Observed configuration** | A repository setting, tracked workflow, or tool configuration was inspected at a named revision/time. | “It executed and covered all intended files/components.” |
| **Executed/verified** | Exact command or scan, tool/client version, environment, scope, timestamp, and result are available. | “All platforms, dependencies, threats, and deployment contexts are secure.” |
| **Unknown/gap** | Coverage, access, representative environment, or results were unavailable. | “No findings means no risk” or “missing tool means a defect.” |

Record applicable standards, target commit, observed tools and settings, assessed project systems/operating systems, reviewed risk, tests/scans executed, exceptions and residual risk. A private feed timeout, skipped scan, missing security setting access, and unavailable Windows legacy build are **gaps** unless independently resolved. This documentation issue has **not** executed a SAST/SCA/DAST scan, inspected consumer repository settings, verified remediation, or run any security integration tests.
