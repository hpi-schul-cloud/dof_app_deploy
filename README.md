# dof_app_deploy

## the name
dof: **D**ev**O**ps**F**uture - this was a working title that stuck to this repository

## why
goal is to enable a push based deployment (contrary to pull in [gitops speech](https://www.gitops.tech/#push-based-deployments))
this repository would be the environment repository for that matter

## how
if in any ["auto-deployment" enabled repositories](https://github.com/hpi-schul-cloud/dof_app_deploy/blob/b65488fbc5ecceca8e743327bc66c9092ee30d4e/.github/workflows/deploy.yml#L36) a push happened the [dev deployment workflow](https://github.com/hpi-schul-cloud/dof_app_deploy/files/10235495/dev-deployment.pdf) to our dev system gets executed

## dev namespace (de)activation

only applies to the dev stage to save resources!

_activation_: deployments in a certain namespace are scaled up to 1
_deactivation_: deployments in a certain namespace are scaled down to 0

namespace _lifecycle_:
1. during a rollout the namespace activator is triggered to activate the namespace for 2 days
2. after 2 days the namespace gets automatically deactivated
3. you might re-activate it again, by visiting `https://activate.[dbc,nbc,brb].dbildungscloud.dev/namespace` for 2 more days


- new pushes to a branch won't re-new the 2 days on purpose
- visiting the activator before the time has run up, you may hit activate to get 2 more days
- you may also get more than 2 days, but don't make that your default action, think about the trees 🌳 
  1. get access to the mongodb in the `sc-common` namespace
  2. in the database called `keda` and the collection `namespaces` it will become obvious what you have to change.

