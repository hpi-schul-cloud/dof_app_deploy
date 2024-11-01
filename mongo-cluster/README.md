# Temporaly MongoDB Clusters for the Dev Clusters
To go forward to an more real setup for all of developer and release staging deployments to the developer clusters we build at each devcluster an replocaset 
This folder contain the Setup data for each of theis Devclusters.

# needed items at 1Password

## Item: devops-mongo-cluster-server 

| Variable                 | Description                                  |
|--------------------------|----------------------------------------------|
| MONGODB_URI              | URL of Local MongoDB for one Pod (localhost) |

## Item: devops-mongo-cluster-server-init

This secrets are for the direct connection to the mongodb PODs from the statefull set.
It's used to check if the PODs are up for adding to the replicaset set

| Variable                 | Description                                   |
|--------------------------|-----------------------------------------------|
| MONGODB_URI              | UIR from the POD 0 for the MongoDB Replicaset |
| MONGODB_1_URI            | UIR from the POD 1 for the MongoDB Replicaset |
| MONGODB_1_URI            | UIR from the POD 1 for the MongoDB Replicaset |
