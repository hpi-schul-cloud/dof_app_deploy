# sc-common

This directory contains common Kubernetes manifests for shared services used across different development clusters.

## Deployment

Deployment of these manifests is managed by [Skaffold](https://skaffold.dev/). We are using Skaffold here as a test balloon to evaluate a more cloud-native approach for Kubernetes manifest management as an alternative to our traditional Ansible-based workflows.

### Basic Commands

The following commands can be used to interact with the deployments. These operations are intended for use within our development clusters.

You need to specify a profile for the target environment. The available profiles are `brb`, `dbc`, `nbc`, and `thr`.

**Render the manifests:**

```shell
skaffold render -p <profile_name>
```
*Example:*
```shell
skaffold render -p nbc
```

**Deploy the manifests:**

```shell
skaffold deploy -p <profile_name>
```
*Example:*
```shell
skaffold deploy -p nbc
```

**Diagnose the deployment:**

```shell
skaffold diagnose -p <profile_name>
```
*Example:*
```shell
skaffold diagnose -p nbc
```

## Deployed Services

The following services are deployed by this configuration:

* **sc-common namespace:** The base namespace for all shared services.
* **OpenLDAP:** An OpenLDAP server for user authentication. This includes a deployment and a service. There are single and HA deployments.
* **Telepresence Traffic Manager:** Manages traffic for Telepresence.
* **Database Cleanup CronJob:** A cronjob for cleaning up databases.
* **Namespace Activator:** A service to help save resources in development clusters by deactivating namespaces after a certain period of inactivity. The repository can be found [here](https://github.com/hpi-schul-cloud/devcluster-namespace-activator) and a more detailed explanation of the deactivation process is available [here](https://github.com/hpi-schul-cloud/dof_app_deploy?tab=readme-ov-file#dev-namespace-deactivation).

For more detailed information on Skaffold and its capabilities, please refer to the [official Skaffold documentation](httpss://skaffold.dev/docs/).