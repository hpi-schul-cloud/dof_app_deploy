# A place for resources for all other namespaces: sc-common

all those are one time operations

## ldap
we use a central ldap in the dev cluster
```commandline
kubectl apply -f sc-common.yml -f sc-openldap-deployment.yml -f sc-openldap-svc.yml
```
an additionally ldap server for testing of the single school ldap implementation
```commandline
kubectl apply -f sc-common.yml -f sc-openldap-single-deployment.yml -f sc-openldap-single-svc.yml
```

## namespace activator
to deploy the namespace activator for each dev-cluster kustomize is used
```commandline
kubectl --kubeconfig <config> apply -k namespace-activator/overlays/<tennant>
```

## DB cleanup cronjob
This CronJob deletes MongoDB databases when the namespace doesn't exist anymore.
To deploy it for each dev-cluster kustomize is used:
```commandline
kubectl --kubeconfig <config> apply -k db-cleanup/overlays/<tennant>
```