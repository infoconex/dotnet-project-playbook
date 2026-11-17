# Case B — Modern SDK-style repository conversational evaluation

**Observed evaluation:** November 16, 2026; ChatGPT / GPT-6 as reported; fresh-session initialization not independently established. **Read-only.** No build, tests, repository mutation or new CI execution. This is an AI-behavior report, not independent certification of the consumer repository.

- Playbook revision: `bc9b56e43a45bde90e5908fcdfddb2754dc22965`.
- Target: [dotnet-binary-tools at `610388c5e6022257bafb533ecfa5e86579e4b243`](https://github.com/infoconex/dotnet-binary-tools/tree/610388c5e6022257bafb533ecfa5e86579e4b243).
- Both SHAs were supplied in the opening request; the original retrieval log is unavailable in this retained report.
- **Questions asked: zero.** No options, recommended selections, responses to discovery questions or interactive controls occurred. The fully specified assessment required no discovery or optional feature phase.

## Actual chronological interaction

1. **Developer:** Asked the assistant to follow the pinned `start-here.md` and linked standards, assess the pinned dotnet-binary-tools repository, inspect evidence, and remain read-only.
2. **Assistant:** Said it would inspect both immutable revisions and report evidenced standards findings without making changes; initially summarized the possible classifications in three informal terms.
3. **Assistant:** Reported access to pinned sources; recognized all six canonical outcomes and the difference between documentation, source, tests and executed checks.
4. **Assistant:** Observed that CAP-001–CAP-006 had test/CI traceability while CAP-007, CAP-008 and nonfunctional cases remained planned; cautioned that workflow definitions do not prove execution.
5. **Assistant:** Delivered the standards screening and prioritized findings recorded below, with explicit limitations and no implementation.
6. **Developer:** Ended the evaluation and requested the self-contained retrospective report. This was not a discovery answer or authorization to implement.

No participant question was omitted: the actual assessment proceeded with **zero questions**, appropriate given the complete opening objective. No phase-2 invitation was needed, rather than being offered and declined. The original assistant's tool retrieval payloads were not preserved; the observations below are **reported assessment results**, not new inspection or execution by this evaluator.

## Original standards screening, qualified

| Outcome recorded | Standards | Reported basis / qualification |
| --- | --- | --- |
| Satisfied (12) | STD-002, 003, 004, 005, 006, 007, 008, 009, 011, 013, 021, 022 | Shared validation scripts; compiled boundaries; C# configuration; representative real-filesystem CAP-006 tests; inward dependencies; change review and traceability. Findings are limited to inspected source, configuration and reported candidate CI. |
| Partially satisfied (5) | STD-001, 010, 012, 019, 020 | Test-first commits without observed red-phase failure; concrete CLI use-case invocation despite adopted hexagonal pattern; private security settings and complete advisory dispositions unknown. Missing evidence alone is not a proven defect. |
| Not applicable (5) | STD-014, 015, 016, 017, 018 | No demonstrated complex business domain, separately governed modules, feature-slice need, independently deployed services or event-mediated integration. |
| Gap / Approved exception / Unknown (0) | None at standard-wide level | Several individual settings and execution claims remained unknown within broader scoped assessments; no exception approval was invented. |

**Principal architectural finding:** The assistant reported that `CliApplication.Run` invoked `InputSelectionService`, `InventoryService`, `ReportService`, and `LifecycleRefreshService` directly, while the repository had adopted hexagonal architecture and exposed outbound interfaces. [STD-012](../standards/hexagonal.md#std-012) expressly requires an interface for each *identified* inbound port when adopted; construction at a composition root remains legitimate. The concern is plausible but requires source-level corroboration before becoming a verified consumer-repository defect. Ordinary SOLID does not demand an interface for every class.

**Reported historical evidence:** The assistant identified 190 passing tests on Windows, Linux and macOS, Native AOT smoke checks, security review and coverage on an implementation PR candidate. Its report distinguished candidate `b91f4e7` from the requested final squash revision `610388c5…`, without claiming that the candidate run executed at the final SHA. Underlying job payloads were not preserved in this evaluator's transcript. Planned CAP-007/CAP-008 and nonfunctional scenarios were not presented as failed current obligations.

**Recommended priorities:** Review meaningful inbound-port boundaries; establish GitHub security-setting and advisory evidence; qualify TDD and CI provenance; complete distribution acceptance before release. No changes were authorized or performed.

## AI-behavior judgment and limitations

The assistant respected the assessment-only mode, screened all 22 standards contextually, avoided unnecessary discovery, and distinguished current implementation from future capability and recorded candidate execution. Limitations: original retrieval logs absent; no independent test or source reinspection here; administrator settings inaccessible; some Satisfied/Partially satisfied classifications span both observed and unknown sub-obligations. No observed behavior establishes a generator, installable AI agent, universal compliance or equivalent outcomes from other models.

**Playbook lessons:** Permit zero-question assessments; record source SHA, CI SHA, execution scope and log limitations per material finding; clarify Partial versus Unknown for composite obligations; avoid equating security-control documentation with enabled controls; identify interface adoption choices without extending STD-010; keep release completeness separate from compliance.
