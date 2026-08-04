# dof_app_deploy

## the name
dof: **D**ev**O**ps**F**uture - this was a working title that stuck to this repository

## why
goal is to enable a push based deployment (contrary to pull in [gitops speech](https://www.gitops.tech/#push-based-deployments))
this repository would be the environment repository for that matter

## how
if in any ["auto-deployment" enabled repositories](https://github.com/hpi-schul-cloud/dof_app_deploy/blob/b65488fbc5ecceca8e743327bc66c9092ee30d4e/.github/workflows/deploy.yml#L36) a push happened the [dev deployment workflow](https://github.com/hpi-schul-cloud/dof_app_deploy/files/10235495/dev-deployment.pdf) to our dev system gets executed

## adding new secrets
_Note: Consult with DevOps for any uncertainties._

### Appending to an Existing Secret
1. **Update in 1Password**: Modify the secret within development vaults (sc-dev-*) in 1Password.
2. **Notify DevOps**: Inform DevOps for updates across other stages.

### Creating a New Secret

1. **Create in 1Password**: Add a new item in the development vaults (sc-dev-*).
2. **Prepare Manifest**:
   ```yaml
   apiVersion: "onepassword.com/v1"
   kind: OnePasswordItem
   metadata:
     name: <unique-secret-name>
     namespace: {{ NAMESPACE }}
     labels:
       app: "your-app"
   spec:
     itemPath: "vaults/{{ ONEPASSWORD_OPERATOR_VAULT }}/items/<item-name>"
   ```
3. Add to Ansible: Incorporate the manifest into the relevant Ansible task, usually `main.yml`.
4. Inform DevOps: Notify DevOps for deployment to other stages.

## dev namespace (de)activation

only applies to the dev stage to save resources!

_activation_: deployments in a certain namespace are scaled up to 1  
_deactivation_: deployments in a certain namespace are scaled down to 0



namespace _lifecycle_:
1. during a rollout the namespace activator is triggered to activate the namespace for 12 hours (configured in `sc-common/namespace-activator/base/app.yml`)
2. after 12 hours the namespace gets automatically deactivated
3. you might re-activate it again, by visiting `https://activate.[dbc,nbc,brb,thr].dbildungscloud.dev/namespace` for 12 more hours


- new pushes to a branch won't re-new the 12 hours on purpose
- visiting the activator before the time has run up, you may hit activate to get 12 more hours
- you may also get more than 12 hours, but don't make that your default action, think about the trees 🌳

### extend activation time by adding a label to your pr:
⚠️ **Important: The auto-extend-activation-time label should only be used when absolutely necessary, such as when you need to activate the namespace for e2e tests.** Avoid using it as a precautionary measure to prevent unnecessary rollouts and resource consumption.

This method is effective for each unique PR. If you have multiple PRs from the same branch across various repositories, you only need to apply this setting once.
1. Navigate to the PR you wish to automatically extend its namespace's activation time.
2. Apply the `auto-extend-activation-time` label to the PR. This action will also initiate a new rollout.
3. Following this, the activation time for the namespace will be automatically extended with every new push to the branch associated with this PR.

### extend activation time by modifying the database:
Modify the entry in the `keda` database, `namespaces` collection.

## network policies

network traffic is isolated with a namespace-wide default-deny ingress policy. the former namespace-wide default-allow policy is removed during deployment. additional policies select the pods for which they grant traffic.

network policies are additive. if multiple policies select the same pod, the allowed traffic from all of them is combined. an additional policy therefore extends the allowed traffic and does not override existing policies.

there are currently two kinds of workload policies:

- restrictive policies describe the known callers, destinations, protocols and ports of a workload. these are the intended long-term form of network policies.
- generic policies preserve the broad access that existed before network policies were introduced, but select only the pods belonging to a particular workload. these are transitional compatibility policies and should be narrowed as the workload dependencies become known.

### telepresence

telepresence is available only on the dev stage and requires communication with the traffic manager in the `ambassador` namespace. one policy selects all pods in the application namespace and allows ingress from the `ambassador` namespace.

workloads without an egress policy already have unrestricted egress and need no additional rule. workloads with restrictive egress policies are maintained in `telepresence_egress_workloads`. an additional policy is generated for each entry to allow egress to the `ambassador` namespace on TCP port `8081`.

selecting all pods for ingress is intentional because every workload may be intercepted with telepresence. egress must not select all pods because doing so would make every pod egress-isolated. when a workload gains a restrictive egress policy, it must also be added to `telepresence_egress_workloads`. on a cluster without an `ambassador` namespace, the namespace selectors match nothing and grant no traffic.

## how does a branch name get converted into a namespace
To convert a branch name to a Kubernetes namespace by stripping paths, converting to lowercase, and replacing underscores and dots with hyphens. It ensures the namespace is compliant with Kubernetes naming conventions.

Some examples:
```commandline
refs/heads/FEATURE_NAME.1 => feature-name-1
depandabot/npm/jose-5.8.3 => jose-5-8-3
refs/tags/v2.0.1-beta => v2-0-1-beta
feature/ABC_XYZ.2021 => abc-xyz-2021
HUHU-666 => huhu-666
```
