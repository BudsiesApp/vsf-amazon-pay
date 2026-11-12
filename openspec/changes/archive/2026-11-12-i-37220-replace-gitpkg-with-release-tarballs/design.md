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

This describes the retained explicit-release interface. The approved on-demand command below bypasses per-iteration configuration/test edits while leaving that path available.

This selects the ticket's release-tag interface rather than adding both triggers. A tag workflow can run from the packaging revision without first installing `workflow_dispatch` on stale default `master`. Execute packaging code only from that checkout; safely pass configured revisions as data and resolve them via Git, without evaluating shell text or source lifecycle hooks.

### Package the selected API tree only

Use `git archive` of the selected `API/amazon-pay` tree into an isolated staging directory. Pack it with lifecycle execution disabled and npm-compatible `package/` layout. Preserve `index.js`, any package runtime files, package name/version and all runtime dependencies. No package install, frontend preparation, standalone build or runtime-source edit is needed. Do not include repository-root frontend files or a root lockfile. Keep the explicit workflow's pinned runtime; previews record their exact runtime in identity, with stable archive ordering/metadata for reruns.

Unlike Vue there is no entry generation or transport rewrite inside the source manifest. Archive verification compares extracted payload files and manifest to that source tree, documenting only any necessary packaging metadata differences. An unrelated dependency upgrade is not a packaging change.

### Release assets and provenance

The proposed initial tag is `packages-37220-v1`; if occupied, use a new unused `packages-*` tag instead of changing it. Publish `amazon-pay.tgz`, `release-manifest.json` and `SHA256SUMS`. The consumer URL is:

`https://github.com/BudsiesApp/vsf-amazon-pay/releases/download/<release-tag>/amazon-pay.tgz`

Metadata identifies repository, release tag, full packaging commit, package name/version, full source commit, `API/amazon-pay`, archive filename and SHA-256. `SHA256SUMS` covers the archive. Omit volatile timestamps/run IDs so identical reruns can reuse the existing metadata. Release notes distinguish source and packaging revisions and link metadata assets. Repository source archives and Actions artifacts are not substitutes.

### Conflict-safe publication

For the explicit tag workflow, use the repository token with `contents: write` only for publication; download URLs require no credentials. Serialize that workflow by repository/tag without canceling an active publication. Preflight all corresponding existing archive and metadata assets and the tag's packaging revision. Reuse exact matches; reject incompatible provenance or bytes before changing any existing asset. Upload missing assets without clobber/deletion; a race/error fails or verifies identical existing bytes. A rerun can finish a partial matching publication, but success requires the whole metadata/archive set to agree.

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

## Approved on-demand preview extension

### Current baseline and runnable command

The original pinned migration is implemented, published as `packages-37220-v1` and accepted within its scope (D18–D21). Current PR #3 head is `fec15d5`. Keep existing assets, recorded packaging provenance and completed unchanged acceptance evidence. The preview extension is pending.

Add `scripts/preview-packages.py`, invoked from the checkout containing its committed implementation with existing Python 3.11+, Git and authenticated GitHub CLI: `python3 scripts/preview-packages.py --source-ref <feature-branch-or-full-commit>`. This source input is required; the command does not silently substitute the tracked release configuration. Packaging identity is the full committed HEAD of the publishing tools, not the requested source commit. Require committed versioned publishing inputs rather than attributing dirty publishing code to HEAD. The maintainer initially fetches/checks out and pushes that packaging feature revision so GitHub can target its SHA; subsequent source selections require no publishing edits/commits.

This is the one required on-demand surface, not an additional GitHub dispatch workflow. Source default `master` remains stale; `workflow_dispatch` default-branch availability is therefore avoided. GitHub CLI's documented `gh release create --target <full-commit>` creates a missing tag at the specified packaging revision, so command-managed publication is feasible from an unmerged pushed feature revision. No new account, credential or host-tool installation is selected; missing tool/access prerequisites go to the lead.

Feasibility check: available tools are Python 3.12.3 (`python3`), Git 2.55.0 and GitHub CLI 2.45.0; `python3.11` and managed 3.11.11 are unavailable. Both existing source suites pass on the available Python (two tests each). Use that supported command runtime without host installation, retaining workflow Python 3.11.11. Record exact Python/zlib runtime versions in preview identity/provenance to distinguish packaging environments.

### Source resolution and generic packaging

Fetch the selected branch/ref from `BudsiesApp/vsf-amazon-pay` once and resolve the fetched object to a full source commit, or fetch/verify the supplied full SHA. Package only that resolved tree; later branch motion cannot change it. Invalid refs fail clearly before publication without selecting another source. Validate selections as branch names, full refs or full commit SHAs, not arbitrary Git options/revision expressions. Use argument arrays and the existing Git-tree reader, not shell evaluation, source checkout or source lifecycle execution.

Allow `package-release.py` explicit resolved-source inputs while keeping the existing configuration-backed workflow intact. Reuse Python deterministic `API/amazon-pay` packaging; no runtime-source change, dependency install or build is needed. Generic checks compare the requested tree/name/version/dependencies to the archive; dedicated initial-pin regression coverage continues asserting `d9f6fcd224938bbcb7472306946d2a947c3ae5e6`. Neither the command nor a maintainer changes config or baseline assertions to make arbitrary preview sources pass.

### Identity and complete immutable publication

Use SHA-256 of canonical JSON with format version `1`, repository, full packaging revision, source mapping `{amazonPay: <full SHA>}` and toolchain mapping `{python: <exact version>, zlib: <runtime version>}`, serialized with sorted keys and no insignificant whitespace. The release tag is `package-preview-<full digest>`. Branch spelling/run timestamps are not part of this key or volatile provenance; persist identity fields in metadata. A changed source, packaging commit or recorded toolchain produces a new key even if files are similar. Identical resolved identities can reuse a complete preview.

Prepare/check candidate `amazon-pay.tgz`, `release-manifest.json` and `SHA256SUMS` with the final preview tag before public writes. Create a missing preview release/tag using GitHub CLI with the exact remote-reachable packaging SHA, as prerelease/not latest. This namespace is distinct from `packages-*`, so no retained tag workflow is triggered. Existing tag targets, provenance and all candidate asset bytes must match before adding anything. Retain the explicit workflow's existing-tag verification in its own mode.

Reuse the publisher's non-clobber preflight, missing-asset upload and final verification. Matching complete previews require no asset writes; matching partial sets can finish on rerun, but conflicting bytes/provenance are never replaced/deleted. Concurrent create/upload races may fail clearly and be rerun after inspection; no automatic retry policy or incomplete success is introduced.

Success prints one machine-readable handoff with release tag, packaging SHA/toolchain, source SHA, package name/version/exact anonymous URL and manifest/checksum URLs only after the complete remote set is verified. Logs stay separate; failures exit nonzero without a success handoff. Preserve all earlier assets.

### Maintenance, acceptance and approval

Rewrite the routine feature-testing/post-merge procedure in `scripts/PACKAGE-RELEASE.md` around source selection and this command. Keep the explicit config/tag workflow separately documented, but remove the requirement to edit initial-pin tests for every later source. The maintainer still explicitly updates the API manifest and Classic lockfile in its existing container; API documentation/checks accept preview as well as explicit-release identities. Preview experiments remain in the intended testing graph, not arbitrary replacements of the accepted final pin. No automatic consumer commits/PRs, moving dependency aliases or payment-handler invocation is added.

Implementation tests cover branch/full-commit resolution and failure, generic selected-tree verification, stable keys, changed source/packaging keys, same-key reuse, conflicts, partial completion and exact output. Tester proves actual command publication and anonymous checksum download, an unmerged feature selection followed by branch advancement without configuration/test commits or manually prepared tags, explicit commit selection and targeted API installation/build/router-loading compatibility. The same path accepts final merged commits. Retain prior unchanged migration evidence and choose regression checks from the actual extension diff; do not reopen every original acceptance check merely because scope expanded.

Input-10 authorizes command-managed `package-preview-*` tags/releases/assets in this repository and Storefront UI after source packaging checks pass, preserving existing assets. It supplements, not rewrites, input-4's explicit-tag/workflow approval. Implementer/tester own that later execution; this spec revision publishes nothing. Missing repository write permission goes to the lead. No merge, deployment, archive or issue transition is authorized.
