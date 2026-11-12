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
For a later package, update the source SHA and the baseline assertions in the
focused test, commit the change, and run the tests. After authorization, create
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
