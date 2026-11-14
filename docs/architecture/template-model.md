# Planned template architecture

**Status: design only.** No project generator, NuGet template package, profile, or reusable project asset has been published or verified yet. This document defines implementation boundaries for later issues.

## Asset ownership

| Asset | Responsibility |
| --- | --- |
| `docs/` | Normative standards, adoption policy, and decisions. |
| `templates/` (future) | Canonical source for files delivered to generated repositories. |
| `scripts/` (future) | Reproducible validations and template packaging; focused script tests can live alongside scripts under `scripts/tests/`. |
| `tests/` (future) | Generated-output and integration acceptance checks. |
| `examples/` | Real-world decisions and evidence, without a second competing copy of template assets. |
| `.github/` | Governance for the playbook itself and, when justified, CI; not the entire consumer template catalog. |

Create a directory only when it contains meaningful assets. Do not duplicate one canonical `.editorconfig`, build configuration, or CI script in multiple consumer templates unless a documented compatibility difference requires it.

## Planned composition

1. **Common repository foundation:** repository guidance, code style, basic security/contribution policy, and locally runnable quality checks.
2. **Project profile:** library, CLI, web API, worker, or other actual application type with appropriate compiled boundaries and tests.
3. **Optional capabilities:** Native AOT, NuGet distribution, additional infrastructure adapters, or specialized CI checks only when applicable.
4. **Platform/target compatibility:** modern SDK-style .NET by default; legacy .NET Framework requires its own validated build and toolchain guidance.

The standard .NET template engine is the preferred generator for parametrized names, namespaces, and solution structures. GitHub repository templates may provide a convenience entry point later, but should not create a competing definition of starter content.

## Consumer contract to verify

Future tests should generate each supported profile with a non-default name, then verify output paths and namespaces, restore, build, execute relevant tests, enforce naming and architecture constraints, and test packaging or startup where relevant. Cross-platform claims require actual Windows, Linux, and macOS verification for the advertised profile. CI should call the same validation operations that developers can run locally.

Record template version and source revision in generated output. Document configuration choices that must be applied through GitHub settings, such as branch rulesets and secret scanning; copying a file alone does not activate those services.

Do not infer that a future capability works from the existence of this design or a review of documentation.
