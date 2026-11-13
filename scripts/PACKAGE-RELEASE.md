# Amazon Pay package releases

The API package source is selected by the full commit SHA in `package-release.json`.
The release tag identifies the separate packaging revision. The initial source is
`d9f6fcd224938bbcb7472306946d2a947c3ae5e6` and the source path is `API/amazon-pay`.
No source repository dependencies, lifecycle scripts or frontend build are run.

With Python 3.11.11 and Git, prepare and check a release locally:

```sh
python scripts/test-package-release.py
python scripts/package-release.py --output /tmp/amazon-pay-package --tag packages-37220-v1
(cd /tmp/amazon-pay-package && sha256sum -c SHA256SUMS)
```

The output is `amazon-pay.tgz`, `release-manifest.json`, and `SHA256SUMS`.

Every push to the maintained `optimuspro` branch automatically publishes a
non-prerelease release with tag and title `optimuspro_<first-seven-push-SHA>`.
Amazon Pay sources come from that exact triggering commit, independently of the
historical pin in `package-release.json`. The checkout, packaging revision and release tag must
agree with that commit. Check the Actions run, manifest and `SHA256SUMS`
before selecting this URL in a consumer. An identical rerun reuses assets;
conflicting assets or a tag at a different full commit fail without replacement,
including when commits share the same seven-character prefix. The manifest
records the full source and packaging SHA. Older stable, explicit-tag and
preview releases retain their existing names and assets.
Publication does not update consumers or deploy applications.
For feature testing, pushes to non-maintained branches containing the branch
preview workflow publish a public prerelease named `<branch>_<first-seven-SHA>`
from the exact pushed commit. Find the URL and checksums in the workflow summary;
URL-encode `/` in branch names when constructing asset URLs. The default,
maintained and `preview-cleanup/` branches are excluded. Existing branches must
first include the workflow, for example by merging `optimuspro`. Publication
does not change consumers or deploy applications.
Pushes made with a workflow's `GITHUB_TOKEN` do not trigger push workflows.

For an on-demand preview, first check out and push the committed publishing tools,
and push the source branch or commit to this repository's `origin`.
With Python 3.11+, Git, authenticated `gh` and repository write access, run
`python3 scripts/preview-packages.py --source-ref <feature-branch-or-full-sha>`.
The JSON contains the package URL, source and packaging SHAs, Python/zlib
versions and manifest/checksum URLs. Verify those before updating the API
dependency and lock. Rerun against the advanced branch and pass the actual
merged SHA after merge. No config/test edits or manual tag are needed; preview
releases are public and immutable.

New branch previews are tracked outside their immutable assets. A
scheduled workflow checks every recorded branch; only after all are observed
deleted for 30 days may it delete the prerelease and its assets. The Git tag
is retained, but the preview download URL stops working. Reusing a preview
adds the selected feature branch to its associations. An explicitly selected
commit, tag, maintained branch, or protected branch permanently pins
the preview. Older previews whose association history is unknown are never
adopted or deleted. The registry is stored on the `preview-cleanup/registry`
branch, with no changes to release assets. The scheduler lives on the repository
default branch and checks out `optimuspro`; manual dispatch is a read-only dry run.
Any non-maintained, non-internal branch qualifies; protected branches remain
pinned. A branch already absent at publication is pinned because its protection
cannot be checked. Existing pinned previews remain pinned when these rules change.

The 30-day clock starts when deletion is detected, not when a preview is made.
An observed reappearance resets that branch's clock. The final branch check is
immediately before deletion, but a brief reappearance between checks or a
branch created after the final check may be missed. GitHub schedules can be
delayed or disabled; they never shorten the retention interval.

Publication and cleanup share a repository-wide Git ref lock. Concurrent work
fails rather than stealing the lock. A failed or interrupted operation leaves
the lock in place: inspect the workflow/publisher and registry, confirm no
operation is active and that any partially published preview is safe, then
resolve the lock with an authorized maintainer. Never automatically clear it.
The branch publication and default-branch scheduler workflows also share an
Actions concurrency group with `queue: max`. Update the scheduler workflow on
the default branch before enabling branch previews, because scheduled workflows
run from that branch. Branch previews are skipped until cleanup support reaches
`optimuspro`; the old cleanup cannot read their registry entries.
GitHub queues at most 100 pending runs in a concurrency group; additional runs
are canceled and must be rerun. The local preview command is outside that queue
and still fails on lock contention rather than taking over an active lock.

For the separate explicit-release path, update the source SHA and baseline
assertions, commit the change, and run the tests. After authorization, create
and push a new, unused `packages-*` tag pointing at that packaging commit. The
tag workflow publishes all three assets. Do not move a tag or delete historical
releases: old application revisions may still consume them. A rerun reuses
matching assets and fills missing assets; a conflict fails without replacement.
Resolve a conflict by investigating it and publishing under a new tag, not by
clobbering an existing asset.

Check the manifest's source and packaging revisions and download the assets
anonymously from `https://github.com/BudsiesApp/vsf-amazon-pay/releases/download/<tag>/`;
run `sha256sum -c SHA256SUMS` on the download. Set the API's
`@vue-storefront-api/amazon-pay` dependency to the corresponding `amazon-pay.tgz`
URL, regenerate its Yarn Classic lock in its Node 14 container, and verify a
frozen install and the maintained checks. Keep prior GitPkg and release URLs
available for historical consumers.
