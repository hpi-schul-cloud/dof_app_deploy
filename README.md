# dof_app_deploy

## the name
dof: **D**ev**O**ps**F**uture - this was a working title that stuck to this repository

## why
goal is to enabled a push based deployment (contary to pull in [gitops speech](https://www.gitops.tech/#push-based-deployments))
this repository would be the environment repository for that matter

## how
if in any ["autodeployment" enabled repositories](https://github.com/hpi-schul-cloud/dof_app_deploy/blob/b65488fbc5ecceca8e743327bc66c9092ee30d4e/.github/workflows/deploy.yml#L36) a push happend the [dev deployment workflow](https://github.com/hpi-schul-cloud/dof_app_deploy/files/10235495/dev-deployment.pdf) to our dev system gets executed

