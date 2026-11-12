# Tasks

## 1. Isolated API package preparation

- [x] 1.1 Add explicit source configuration and isolated extraction of `API/amazon-pay`; verify focused source-identity tests use initial commit `d9f6fcd224938bbcb7472306946d2a947c3ae5e6` independently of packaging HEAD and preserve package name/version/runtime dependencies.
- [x] 1.2 Produce a repeatable npm-compatible archive without dependency installation or lifecycle execution; verify archive tests preserve entry/runtime payloads, exclude repository-root frontend files and GitPkg manifests, and compare allowed packaging differences against the pinned source tree.
- [x] 1.3 Document local packaging, selected source inputs and output layout; verify the documented command and source-versus-packaging distinction match the script and focused tests.

## 2. Traceable non-overwriting publication

- [x] 2.1 Generate deterministic release-manifest.json and SHA256SUMS; verify focused tests recompute the archive hash and match package identity, source path/commit, packaging SHA, release tag and `amazon-pay.tgz` filename.
- [x] 2.2 Add the `packages-*` tag workflow and publication code with tag-scoped serialization, required token permission and no-clobber preflight/upload behavior; verify no-network tests cover absent, identical, conflicting and partial existing assets and preserve all conflicting existing bytes/provenance.
- [x] 2.3 Document authorized tag publication, anonymous download/checksum verification, reruns/conflicts, later source selection, API manifest/lock updates and historical retention; verify every command/asset name matches the implementation and no step requires deleting or replacing historical assets.

## Workflow follow-up

- Lead obtains authorization/access before tag publication. Tester proves actual Actions publication, anonymous download/checksum agreement, repeat-publication retention, cache-empty API install, maintained build/checks and non-production extension loading without invoking payment operations.
- Final API URL/lock work depends on published assets. Local packaging is not proof of successful public hosting.
- Archive only when selected by the operator; merges and deployments remain separate work.
