# Legacy Files Shared Bucket Notes

Status as of 2026-08-12.

## Goal

Move the legacy file service in `schulcloud-server` to a shared bucket on the same underlying S3 used for newer services, without reusing `file-storage` code.

The legacy service should:
- keep using its own legacy code paths
- use one shared bucket
- isolate objects by cluster and namespace
- allow cluster-wide cleanup of stale namespace prefixes

## Current implementation state

Implemented in this workspace:

### `dof_app_deploy`

- Added deploy config support for:
  - `FEATURE_LEGACY_FILES_SHARED_BUCKET_ENABLED`
  - `LEGACY_FILES_SHARED_BUCKET`
  - `LEGACY_FILES_SHARED_STORAGE_PROVIDER_ID`
  - `LEGACY_FILES_SHARED_BUCKET_PREFIX`
- Dev config currently uses:
  - `FEATURE_MULTIPLE_S3_PROVIDERS_ENABLED: "true"`
  - `FEATURE_LEGACY_FILES_SHARED_BUCKET_ENABLED: "true"`
  - `LEGACY_FILES_SHARED_BUCKET: "sc-dev-cd-txl-bucket-0000"`
  - `LEGACY_FILES_SHARED_STORAGE_PROVIDER_ID: "6899c0000000000000000001"`
  - `LEGACY_FILES_SHARED_BUCKET_PREFIX: "legacy-files/{{ SC_THEME }}/{{ NAMESPACE }}"`
  - `AWS_ENDPOINT_URL: "https://s3-eu-central-2.ionoscloud.com"`

### `schulcloud-server`

- Added `LEGACY_FILES_SHARED_STORAGE_PROVIDER_ID` to config schema.
- Shared-bucket mode now resolves one explicit storage provider by configured ID.
- Shared-bucket mode now uses that provider for runtime S3 access and signed URLs.
- Init script now `upsert`s a deterministic `storageproviders` record with:
  - `_id = LEGACY_FILES_SHARED_STORAGE_PROVIDER_ID`
  - `endpointUrl = AWS_ENDPOINT_URL`
  - `region = AWS_REGION`
  - `accessKeyId = AWS_ACCESS_KEY`
  - `secretAccessKey = encrypted AWS_SECRET_ACCESS_KEY`

### `schulcloud-client`

- Added `https://s3-eu-central-2.ionoscloud.com` to the CSP allowlists that were blocking browser upload access earlier.

### `sc-common`

- Added a new cleanup CronJob for legacy files:
  - image: `quay.io/schulcloudverbund/platform-tooling-job-tools:0.2`
  - uses `kubectl` to list namespaces
  - uses `rclone` to list and purge stale prefixes in S3
- Cleanup is scoped per cluster via overlay patches:
  - `legacy-files/dbc`
  - `legacy-files/brb`
  - `legacy-files/nbc`
  - `legacy-files/thr`
- Runtime object layout is now intended to be:
  - `legacy-files/<cluster>/<namespace>/<schoolId>/<filename>`

## Platform tooling

Created new repo skeleton in this workspace:
- `platform-tooling`
- images:
  - `job-tools`
  - `admin-tools`

Current relevant image:
- `quay.io/schulcloudverbund/platform-tooling-job-tools:0.2`

`job-tools` now includes:
- `sh`
- `curl`
- `jq`
- `kubectl`
- `rclone`
- `ca-certificates`

## Secrets / config sources

### Legacy cleanup job (`sc-common`)

Kubernetes secret name:
- `legacy-files-cleanup-s3-secret`

1Password items currently referenced:
- `vaults/sc-dev-dbc/items/legacy-files-cleanup-s3`
- `vaults/sc-dev-brb/items/legacy-files-cleanup-s3`
- `vaults/sc-dev-nbc/items/legacy-files-cleanup-s3`
- `vaults/sc-dev-thr/items/legacy-files-cleanup-s3`

Expected secret keys:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_ENDPOINT_URL`
- `LEGACY_FILES_SHARED_BUCKET`
- optional `AWS_REGION`

### Legacy file service runtime / init

Relevant namespace secret/config sources:
- `api-secret` from 1Password item `server`
- `api-configmap`

Important runtime/init envs:
- `AWS_ACCESS_KEY`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_ENDPOINT_URL`
- `LEGACY_FILES_SHARED_STORAGE_PROVIDER_ID`
- `LEGACY_FILES_SHARED_BUCKET`
- `LEGACY_FILES_SHARED_BUCKET_PREFIX`

## Important design decision taken

We moved away from the short-lived idea of using direct `AWS_*` runtime config as the long-term shared-bucket implementation.

Current direction is provider-centric:
- one deterministic shared `storageprovider` record
- all schools will eventually be migrated to that provider
- runtime shared-bucket mode resolves that provider explicitly by ID

Next step after this setup works:
- create migration scripts to rewrite school `storageProvider` references to the shared provider

## Open issue: upload still failing from browser

Current symptom:
- browser upload `PUT` to S3 returns HTTP 500 with S3 XML `InternalError`

One real example URL showed:
- endpoint host: `s3-eu-central-2.ionoscloud.com`
- signed credential scope region: `eu-central-1`
- signed headers:
  - `host`
  - `x-amz-meta-flat-name`
  - `x-amz-meta-name`
  - `x-amz-meta-thumbnail`

### Strong suspects

1. Region mismatch
- signed URL currently contains `.../eu-central-1/s3/aws4_request`
- endpoint used is `s3-eu-central-2.ionoscloud.com`
- likely source: shared `storageprovider.region` is still `eu-central-1`

2. Signed header mismatch
- server signs `x-amz-meta-thumbnail`
- browser must send that header too
- if omitted by the browser request, the signature does not match
- this backend may answer with generic `InternalError` instead of a clearer auth error

## Immediate next checks

### 1. Verify the shared storage provider document in MongoDB

Check the provider with `_id = 6899c0000000000000000001`.

Relevant fields to inspect:
- `endpointUrl`
- `region`
- `accessKeyId`
- `secretAccessKey`

Most likely needed value:
- `region` should probably be `eu-central-2` if Ionos expects signing region aligned with the endpoint

Note:
- current init code writes `region = AWS_REGION`
- if namespace config still provides `AWS_REGION=eu-central-1`, the provider document will also get `eu-central-1`

### 2. Inspect the actual browser `PUT` request in devtools

Verify whether the upload request really sends all signed headers:
- `Content-Type: image/jpeg`
- `x-amz-meta-name`
- `x-amz-meta-flat-name`
- `x-amz-meta-thumbnail`

Important:
- if `x-amz-meta-thumbnail` is signed but not sent, upload can fail

### 3. Compare signed URL generation vs request headers

Server code signs metadata here:
- `schulcloud-server/src/services/fileStorage/proxy-service.js`
- `schulcloud-server/src/services/fileStorage/strategies/awsS3.js`

At the moment the server signs:
- `name`
- `flat-name`
- `thumbnail`

But the response returned to the browser only visibly includes:
- `Content-Type`
- `x-amz-meta-name`
- `x-amz-meta-flat-name`

That mismatch is suspicious and should be checked carefully before changing anything else.

### 4. If region is wrong, fix config or data first

Do not patch random signing logic first.

First confirm:
- what region Ionos expects for this endpoint
- what `AWS_REGION` is in the dev namespace
- what region was written into the shared provider document

## Cleanup job notes

The cleanup job itself was made more robust:
- switched from raw Kubernetes API calls via `curl` to `kubectl`
- fixed ConfigMap script mount permissions
- changed `rclone` setup to use env-based remote config
- added basic progress logging and final no-op summary

If it fails again, first check:
- secret keys in `legacy-files-cleanup-s3-secret`
- `AWS_ENDPOINT_URL`
- `LEGACY_FILES_SHARED_BUCKET`
- service account permissions for `namespace-management`

## Files touched in this work

Main relevant files:
- `dof_app_deploy/ansible/group_vars/all/config.yml`
- `dof_app_deploy/ansible/group_vars/develop/cfg.yml`
- `dof_app_deploy/sc-common/skaffold.yaml`
- `dof_app_deploy/sc-common/legacy-files-cleanup/...`
- `schulcloud-server/config/default.schema.json`
- `schulcloud-server/src/services/fileStorage/strategies/awsS3.js`
- `schulcloud-server/ansible/roles/schulcloud-server-init/templates/configmap_file_init.yml.j2`
- `schulcloud-client/ansible/roles/schulcloud-client-core/templates/client-configmap-files.yml.j2`
- `schulcloud-client/config/http-headers.js`

## Suggested resume point

Resume with:
1. inspect the shared storageprovider document in MongoDB
2. compare its `region` with the signed URL region
3. inspect actual browser `PUT` headers for the failing upload
4. only then decide whether the next fix is:
   - region correction
   - metadata header alignment
   - both

