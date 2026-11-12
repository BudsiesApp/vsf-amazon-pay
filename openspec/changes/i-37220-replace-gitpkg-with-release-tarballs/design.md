# Design

## Context

See `proposal.md` for motivation. The default `master` branch is five commits behind the maintained `optimuspro` branch and does not contain initial source `d9f6fcd224938bbcb7472306946d2a947c3ae5e6`. The feature uses updated `optimuspro`, at that source commit. A new local checkout and minimal OpenSpec root were authorized for this work.

At the pinned commit, `API/amazon-pay` is a CommonJS package with `index.js`, version `0.1.0` and seven runtime dependencies. It has no package lifecycle preparation. The same repository also contains frontend components/hooks/store files, which are not this API artifact. VSF API imports the package and calls its router factory in `src/api/index.ts`.

## Goals / Non-Goals

**Goals:** Publish the API subdirectory as an independently selected, traceable prepared package using the same release conventions as the Storefront UI companion change.

**Non-Goals:** Changing payment implementation, packaging the frontend repository root, modifying credentials/configuration, upgrading dependencies, building a new library or exercising payment requests.

## Decisions

### Tag-triggered packaging with explicit source configuration

Add `.github/workflows/publish-packages.yml` for pushes of `packages-*` tags. A tracked `scripts/package-release.json` selects the full `amazonPayRevision`; its initial value is `d9f6fcd224938bbcb7472306946d2a947c3ae5e6`. The release tag points to the packaging commit, recorded separately from the package source. Future publications update the configuration and create a new tag.

This selects the ticket's release-tag interface rather than adding both triggers. A tag workflow can run from the packaging revision without first installing `workflow_dispatch` on stale default `master`. Execute packaging code only from that checkout; safely pass configured revisions as data and resolve them via Git, without evaluating shell text or source lifecycle hooks.

### Package the selected API tree only

Use `git archive` of the selected `API/amazon-pay` tree into an isolated staging directory. Pack it with lifecycle execution disabled and npm-compatible `package/` layout. Preserve `index.js`, any package runtime files, package name/version and all runtime dependencies. No package install, frontend preparation, standalone build or runtime-source edit is needed. Do not include repository-root frontend files or a root lockfile. Use a pinned packaging runtime/tool version and stable archive ordering/metadata for reruns.

Unlike Vue there is no entry generation or transport rewrite inside the source manifest. Archive verification compares extracted payload files and manifest to that source tree, documenting only any necessary packaging metadata differences. An unrelated dependency upgrade is not a packaging change.

### Release assets and provenance

The proposed initial tag is `packages-37220-v1`; if occupied, use a new unused `packages-*` tag instead of changing it. Publish `amazon-pay.tgz`, `release-manifest.json` and `SHA256SUMS`. The consumer URL is:

`https://github.com/BudsiesApp/vsf-amazon-pay/releases/download/<release-tag>/amazon-pay.tgz`

Metadata identifies repository, release tag, full packaging commit, package name/version, full source commit, `API/amazon-pay`, archive filename and SHA-256. `SHA256SUMS` covers the archive. Omit volatile timestamps/run IDs so identical reruns can reuse the existing metadata. Release notes distinguish source and packaging revisions and link metadata assets. Repository source archives and Actions artifacts are not substitutes.

### Conflict-safe publication

Use the repository workflow token with `contents: write` only for publication; download URLs require no credentials. Serialize publication by repository/tag without canceling an active publication. Preflight all corresponding existing archive and metadata assets and the tag's packaging revision. Reuse exact matches; reject incompatible provenance or bytes before changing any existing asset. Upload missing assets without clobber/deletion; a race/error fails or verifies identical existing bytes. A rerun can finish a partial matching publication, but success requires the whole metadata/archive set to agree.

These checks implement explicit existing-asset retention requirements on real external I/O. No automatic retry loop, cleanup service, registry, signing or replacement path is added.

### Verification ownership

The implementer adds focused archive/source-identity tests and publication tests for new, identical, conflicting and partial existing release states using a no-network test double. The tester proves actual workflow publication and anonymous checksum-verified download, then cache-empty frozen installation, API build/maintained checks and extension loading in non-production. Importing the package and creating its router does not require invoking any payment route; no real payment is part of acceptance.

## Risks / Trade-offs

- Existing runtime dependencies/legacy payment code remain intentionally unchanged → test loading on the API's existing Node 14 toolchain, not a library upgrade.
- GitHub administrators can mutate releases → this workflow never overwrites or deletes consumed assets; documentation makes retention explicit without introducing signing infrastructure.
- An interrupted upload can leave a partial release → rerun verifies existing bytes and fills only missing matching assets; do not record publication success early.
- External publication requires authorization/access → lead obtains it before pushing a release tag, and missing publication evidence stays open.

## Migration Plan

Implement/review on `37220-replace-gitpkg-with-release-tarballs`, targeting maintained `optimuspro`. With separate authorization, tag the packaging revision and publish the pinned package. Verify anonymous availability and checksums before the API lockfile selects that URL. API deployment/rollback and source-branch merges are separate authorized work; preserve all historical release and GitPkg URLs throughout.
