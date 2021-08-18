# A place for resources for all other namespaces: sc-common

all those are one time operations

## rabbitmq
full Tutorial here: https://www.rabbitmq.com/kubernetes/operator/quickstart-operator.html

This will create a new namespace: rabbitmq-system, thats where the cluster operator ... operates
```
kubectl apply -f "https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml"
```

## ldap
we use a central ldap in the dev cluster
```
kubectl apply -f sc-common.yml
kubectl apply -f sc-openldap-deployment.yml
kubectl apply -f sc-openldap-svc.yml
```