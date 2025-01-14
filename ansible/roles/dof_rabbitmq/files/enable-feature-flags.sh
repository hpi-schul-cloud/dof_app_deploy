#!/bin/bash

set -euo pipefail

KUBECONFIG_OPTION=""
NAMESPACE=""
COMPONENT_NAME="rabbitmq"
CONTAINER_NAME="rabbitmq"
COMMAND="cat /etc/issue"

while [[ $# -gt 0 ]]; do
    case $1 in
        --kubeconfig)
            KUBECONFIG_OPTION="--kubeconfig=$2"
            shift 2
            ;;
        --namespace)
            NAMESPACE=$2
            shift 2
            ;;
        --component-name)
            COMPONENT_NAME=$2
            shift 2
            ;;
        --container-name)
            CONTAINER_NAME=$2
            shift 2
            ;;
        --command)
            COMMAND=$2
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: $0 --namespace <namespace> [--kubeconfig <path>] [--component-name <name>] [--container-name <name>] [--command <command>]"
            exit 1
            ;;
    esac
done

if [[ -z "$NAMESPACE" ]]; then
    echo "Error: --namespace is required"
    echo "Usage: $0 --namespace <namespace> [--kubeconfig <path>] [--component-name <name>] [--container-name <name>] [--command <command>]"
    exit 1
fi

PODS=$(kubectl $KUBECONFIG_OPTION get pods -n "$NAMESPACE" -l "app.kubernetes.io/component=$COMPONENT_NAME" -o jsonpath='{.items[*].metadata.name}')

if [[ -z "$PODS" ]]; then
    echo "No pods found matching app.kubernetes.io/component=$COMPONENT_NAME in namespace $NAMESPACE"
    exit 1
fi

for POD in $PODS; do
    echo "Executing command in pod: $POD"
    kubectl $KUBECONFIG_OPTION exec -n "$NAMESPACE" -c "$CONTAINER_NAME" "$POD" -- $COMMAND || {
        echo "Failed to execute command in pod: $POD" >&2
        exit 1
    }
done
