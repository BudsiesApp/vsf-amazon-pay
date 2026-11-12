# amazon-pay-package-publication Specification

## Purpose

Distribute the existing Amazon Pay API package as a traceable public release asset, retaining its runtime implementation while removing consumer dependence on GitPkg extraction.

## Requirements

### Requirement: Automatic stable branch publication
Every push to `optimuspro` SHALL publish a non-prerelease, immutable GitHub release named `stable-packages-<full triggering commit SHA>`. The Amazon Pay source and packaging revision MUST use the exact triggering commit, independently of historical release configuration. Existing tag-based releases and previews MUST remain available and unchanged.

#### Scenario: Stable branch advances
- **WHEN** a push updates `optimuspro`
- **THEN** the workflow publishes the prepared archive with provenance and checksums for that exact commit without changing consumers

#### Scenario: Stable release is repeated or conflicts
- **WHEN** the same stable publication is rerun
- **THEN** identical assets are reused, and an incompatible tag, release or asset fails without replacing existing content

### Requirement: Explicit package source selection
The explicit release-tag path SHALL publish `@vue-storefront-api/amazon-pay` from `API/amazon-pay` through GitHub Actions at a selected source commit independently of the packaging revision. The on-demand path MUST preserve this interface. The initial migration MUST preserve package name, version, runtime dependencies and implementation apart from documented packaging changes.

#### Scenario: Initial migration
- **WHEN** the initial archive is prepared
- **THEN** its package sources come from `d9f6fcd224938bbcb7472306946d2a947c3ae5e6`, with name `@vue-storefront-api/amazon-pay`, version `0.1.0`, unchanged runtime dependencies and unchanged payment logic

#### Scenario: Later publication
- **WHEN** a maintainer selects a source revision in the release configuration and triggers publication with a release tag
- **THEN** packaging uses `API/amazon-pay` from that resolved commit rather than implicitly using the workflow checkout

### Requirement: Prepared API package
The archive SHALL expose the existing `index.js` entry point and all runtime files under the package root. Its manifest MUST contain no GitPkg dependency URL. Consumer installation MUST NOT prepare or install the multi-package source repository.

#### Scenario: Package is extracted and loaded
- **WHEN** the release archive is installed in the VSF API
- **THEN** the existing CommonJS package entry point and runtime dependencies resolve without GitPkg or source-repository preparation

### Requirement: Public traceable release assets
GitHub Releases in the source repository SHALL host the archive at a stable release-specific anonymous-download URL. Release metadata SHALL identify package name, version, source subdirectory and full source commit, the full packaging revision, asset name and SHA-256 archive checksum.

#### Scenario: Published archive is downloaded anonymously
- **WHEN** a consumer downloads the release archive without credentials
- **THEN** it receives a prepared package rather than a repository source archive or expiring Actions artifact, and its SHA-256 matches the release metadata

### Requirement: Existing release assets remain unchanged
Publication MUST NOT overwrite or delete previously published assets or repoint a consumed release URL. A repeat publication SHALL reuse identical existing content and reject conflicting archives or provenance instead of replacing them.

#### Scenario: Identical repeat
- **WHEN** publication targets an existing release whose corresponding assets and provenance are identical
- **THEN** it succeeds by reusing those assets without replacing their bytes

#### Scenario: Conflicting repeat
- **WHEN** publication targets an existing asset name with different archive contents or incompatible provenance
- **THEN** publication fails visibly and preserves all existing assets and their download URLs

### Requirement: Maintainer publication procedure
Maintenance documentation SHALL explain explicit source selection, prepared packaging, release publication, provenance/checksum verification, API dependency/lockfile updates and retention of previously consumed assets.

#### Scenario: Maintainer publishes a later revision
- **WHEN** a maintainer follows the documented procedure
- **THEN** they can publish a new release and update the API dependency without GitPkg, registry adoption or removal of historical assets

### Requirement: On-demand preview source selection
An authorized maintainer SHALL be able to invoke a documented preview command with an Amazon Pay source branch/ref or commit. The selected ref MUST resolve once to a full source commit. Unresolvable selections MUST fail clearly without falling back to another source. Preparation MUST preserve the requested source package rather than silently using the release configuration or workflow checkout.

#### Scenario: Branch and explicit commit selection
- **WHEN** a maintainer requests an unmerged feature branch or an explicit source commit
- **THEN** the preview identifies and packages the corresponding resolved `API/amazon-pay` tree independently of the packaging commit

#### Scenario: Selected branch advances
- **WHEN** a branch moves after one invocation resolves it and a later preview is requested
- **THEN** the original preview and its URLs remain tied to the first resolved commit, while the later request resolves the later commit

#### Scenario: Invalid selected source
- **WHEN** a selected branch/ref or commit cannot be resolved in the source repository
- **THEN** the command exits unsuccessfully with the failed selection identified and publishes no substitute package

### Requirement: Preview invocation without publishing edits
The on-demand command SHALL publish prepared sources without per-iteration tracked configuration changes, source-expectation test edits, packaging-config/test commits or manually created tags. Generic checks MUST validate requested resolved sources independently of dedicated initial-pin regression coverage. The same command MUST accept an explicit final merged source revision.

#### Scenario: Feature iteration and post-merge selection
- **WHEN** a maintainer invokes previews for a feature commit, a later commit and then its merged commit
- **THEN** each invocation needs only source selection, not edits to publishing configuration or tests, and preserves the initial-pin regression assertions

### Requirement: Immutable preview identity and complete handoff
Each preview SHALL identify the repository, resolved source commit and packaging commit. A new source or packaging identity MUST use a distinct public release identity. Success MUST return the exact anonymous package URL and provenance/checksum locations only for a complete verified matching asset set. Existing consumed assets MUST remain unchanged.

#### Scenario: Matching preview is reused
- **WHEN** the same resolved source and complete packaging identity, including the recorded toolchain, is requested again through the same or a different ref spelling
- **THEN** a complete matching preview is reused without replacing its assets, and the same package and provenance/checksum URLs are returned

#### Scenario: Conflict or interrupted publication
- **WHEN** the preview identity already has conflicting or incomplete assets
- **THEN** conflicting existing bytes/provenance are preserved and the command fails rather than overwriting them; an incomplete matching set can be completed without replacement, but no incomplete set is reported as success

#### Scenario: Packaging or merge identity changes
- **WHEN** the selected source or packaging commit differs, including a new merge commit with similar file contents
- **THEN** the command uses a distinct preview identity and retains every previously consumed URL
