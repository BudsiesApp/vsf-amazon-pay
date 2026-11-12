# Proposal

## Why

The VSF API currently receives `API/amazon-pay` through GitPkg. Redmine [#37220](https://redmine.gorbunov.studio/issues/37220) requires a prepared public package asset that can be downloaded without that service or credentials.

The pinned migration is implemented and accepted within its original scope. The approved preview extension (ticket inputs 8–10 and decisions D25–D28) also supports routine unmerged-branch testing without per-iteration publishing configuration/test commits or manually prepared tags.

## What Changes

- Add isolated packaging and a release-tag-triggered GitHub Actions workflow selecting an explicit Amazon Pay source revision from the tagged release configuration.
- Publish the existing API package as a GitHub release asset without modifying its runtime implementation or dependencies.
- Record source commit, packaging revision and archive checksum, and reject replacement of conflicting existing assets.
- Document publication, consumer lockfile updates, source traceability and retention of historical URLs.
- Add one on-demand Python/Git/GitHub CLI preview command, runnable from a committed packaging feature revision without default-branch workflow changes; resolve a selected branch/ref or commit once.
- Publish or reuse an immutable matching `package-preview-*` release and return exact package/provenance/checksum URLs, including later branch iterations and final merged-source selection.
- Preserve the explicit tag path, initial-pin regression evidence and existing assets; do not automate push/PR publication or VSF dependency changes.

## Capabilities

### New Capabilities

- `amazon-pay-package-publication`: preparation, traceable publication and retention of the Amazon Pay API package release asset.

### Modified Capabilities

None; this repository previously had no canonical OpenSpec capabilities.

## Impact

New scripts, focused tests, a publication workflow and maintenance documentation in `BudsiesApp/vsf-amazon-pay`, based on maintained `optimuspro`, which contains the initial source pin. The companion API change replaces the dependency and Yarn Classic lock entry. Frontend Amazon Pay files, payment business logic, package versions, registries, GitPkg hosting and production deployment are unchanged.
