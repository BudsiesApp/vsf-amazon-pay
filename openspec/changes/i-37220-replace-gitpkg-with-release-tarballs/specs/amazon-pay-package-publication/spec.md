# Spec Delta

## Purpose

Distribute the existing Amazon Pay API package as a traceable public release asset, retaining its runtime implementation while removing consumer dependence on GitPkg extraction.

## ADDED Requirements

### Requirement: Explicit package source selection
GitHub Actions in `BudsiesApp/vsf-amazon-pay` SHALL publish `@vue-storefront-api/amazon-pay` from `API/amazon-pay` at an explicitly selected source revision, resolved to a full commit independently of the packaging revision. Initial publication MUST preserve package name, version, runtime dependencies and implementation apart from documented packaging changes.

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
