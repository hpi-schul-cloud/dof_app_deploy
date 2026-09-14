# Test object storage

This role runs `docker.io/chrislusf/seaweedfs:4.47` in single-node mode with
one replica. The existing `WITH_STORAGE` inventory flag controls deployment.
The S3 endpoint remains `storage-svc:9000` and the existing storage ingress
hostname is unchanged. The former MinIO console port is removed.

Run the full role for the initial replacement: it deletes `storage-deployment`
and waits for its pods to terminate, then creates `storage-seaweedfs-pvc` and
`storage-seaweedfs-deployment`. The configured StorageClass dynamically provisions
a new PV for the new claim. There is a storage outage during replacement.
Subsequent rollouts reuse the SeaweedFS claim. The old `storage-pvc` is not mounted
or migrated; it can be deleted separately when no longer needed.

The existing `storage-secret` and 1Password item are reused. The container maps
`MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` (or the older `MINIO_ACCESS_KEY` /
`MINIO_SECRET_KEY`) to SeaweedFS's `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`.
Missing or empty credentials prevent startup. No application endpoint or
credential changes are needed. The legacy server creates school buckets through S3.

Storage starts empty. Existing database file references will not have backing
objects; recreate any test files that are needed. After deployment, verify school
bucket creation, browser upload/download through the ingress (including CORS),
file deletion, and persistence after restarting the pod. The TCP startup and
readiness probes only check whether the S3 listener is available.
