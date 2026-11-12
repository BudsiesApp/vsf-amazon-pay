# Proposal

## Why

The VSF API currently receives `API/amazon-pay` through GitPkg. Redmine [#37220](https://redmine.gorbunov.studio/issues/37220) requires a prepared public package asset that can be downloaded without that service or credentials.

## What Changes

- Add isolated packaging and a release-tag-triggered GitHub Actions workflow selecting an explicit Amazon Pay source revision from the tagged release configuration.
- Publish the existing API package as a GitHub release asset without modifying its runtime implementation or dependencies.
- Record source commit, packaging revision and archive checksum, and reject replacement of conflicting existing assets.
- Document publication, consumer lockfile updates, source traceability and retention of historical URLs.

## Capabilities

### New Capabilities

- `amazon-pay-package-publication`: preparation, traceable publication and retention of the Amazon Pay API package release asset.

### Modified Capabilities

None; this repository previously had no canonical OpenSpec capabilities.

## Impact

New scripts, focused tests, a publication workflow and maintenance documentation in `BudsiesApp/vsf-amazon-pay`, based on maintained `optimuspro`, which contains the initial source pin. The companion API change replaces the dependency and Yarn Classic lock entry. Frontend Amazon Pay files, payment business logic, package versions, registries, GitPkg hosting and production deployment are unchanged.
