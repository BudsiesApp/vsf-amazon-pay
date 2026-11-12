# Tasks

## 1. Isolated API package preparation

- [x] 1.1 Add explicit source configuration and isolated extraction of `API/amazon-pay`; verify focused source-identity tests use initial commit `d9f6fcd224938bbcb7472306946d2a947c3ae5e6` independently of packaging HEAD and preserve package name/version/runtime dependencies.
- [x] 1.2 Produce a repeatable npm-compatible archive without dependency installation or lifecycle execution; verify archive tests preserve entry/runtime payloads, exclude repository-root frontend files and GitPkg manifests, and compare allowed packaging differences against the pinned source tree.
- [x] 1.3 Document local packaging, selected source inputs and output layout; verify the documented command and source-versus-packaging distinction match the script and focused tests.

## 2. Traceable non-overwriting publication

- [x] 2.1 Generate deterministic release-manifest.json and SHA256SUMS; verify focused tests recompute the archive hash and match package identity, source path/commit, packaging SHA, release tag and `amazon-pay.tgz` filename.
- [x] 2.2 Add the `packages-*` tag workflow and publication code with tag-scoped serialization, required token permission and no-clobber preflight/upload behavior; verify no-network tests cover absent, identical, conflicting and partial existing assets and preserve all conflicting existing bytes/provenance.
- [x] 2.3 Document authorized tag publication, anonymous download/checksum verification, reruns/conflicts, later source selection, API manifest/lock updates and historical retention; verify every command/asset name matches the implementation and no step requires deleting or replacing historical assets.

## 3. On-demand previews

- [x] 3.1 Add the local preview command's required source branch/ref or full-commit input; verify focused tests resolve once to the requested immutable SHA, keep it after branch movement and fail clearly without fallback on an unresolvable selection.
- [x] 3.2 Refactor preparation for explicit resolved sources without config/test edits per invocation; verify generic archive/source tests exercise selected revisions while dedicated initial-pin regression assertions remain unchanged and the existing explicit release workflow still passes.
- [x] 3.3 Add canonical source/packaging/toolchain identity, command-managed `package-preview-*` prerelease creation at the exact pushed packaging SHA and non-clobber reuse/completion; verify focused tests cover equal keys via different ref spellings, changed source/packaging/toolchain keys, conflicts, partial publication and create/upload races without overwrite or incomplete success.
- [x] 3.4 Return exact package/provenance/checksum URLs only after complete verification and document runnable setup, feature iteration, post-merge selection and approval scope; verify CLI/output tests prove no manual tag or configuration/test-edit ceremony and preview identities cannot trigger the existing `packages-*` workflow.

## Workflow follow-up

- Lead obtains authorization/access before tag publication. Tester proves actual Actions publication, anonymous download/checksum agreement, repeat-publication retention, cache-empty API install, maintained build/checks and non-production extension loading without invoking payment operations.
- Final API URL/lock work depends on published assets. Local packaging is not proof of successful public hosting.
- Archive only when selected by the operator; merges and deployments remain separate work.
- Preview extension: input-10 authorizes command-managed preview publication after source checks; later implementer/tester execution must prove actual command publication and anonymous checksum download, branch/ref plus full-commit selection, branch advancement without publishing edits/manual tags, retained earlier URLs, same-identity reuse and returned-URL API consumption. Live checks are not implementation checkboxes.
- Preserve completed pinned-migration evidence and existing assets. Choose extension regressions from the implementation diff; do not silently replace the accepted API pin with arbitrary preview test sources.
