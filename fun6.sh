#!/bin/bash

set -euo pipefail

# Extract repo mappings from git_repos.yml
GIT_REPOS_FILE="ansible/group_vars/all/git_repos.yml"
declare -A REPO_MAPPING
while IFS=: read -r key value; do
    key_trimmed=$(echo "$key" | xargs)
    value_trimmed=$(echo "$value" | xargs)
    if [[ "$key_trimmed" != "DOF_APP_DEPLOY_REPO_NAME" ]]; then
        REPO_MAPPING[$key_trimmed]="$value_trimmed"
    fi
done < "$GIT_REPOS_FILE"

# Find all version.yml files
VERSION_FILES=(./ansible/host_vars/*/version.yml)

instances_list="[]"

for file in "${VERSION_FILES[@]}"; do
    instance=$(basename "$(dirname "$file")")
    repos_list="[]"

    while IFS=: read -r key value; do
        key_trimmed=$(echo "$key" | xargs)
        value_trimmed=$(echo "$value" | xargs)

        repo_key=${key_trimmed%_IMAGE_TAG}_REPO_NAME
        if [[ -n "${REPO_MAPPING[$repo_key]}" ]]; then
            repo_name="hpi-schul-cloud/${REPO_MAPPING[$repo_key]}:$value_trimmed"
            repos_list=$(echo "$repos_list" | jq --arg repo "$repo_name" '. + [$repo]')
        fi
    done < "$file"

    instances_list=$(echo "$instances_list" | jq --arg instance "$instance" --argjson repos "$repos_list" '. + [{"name": $instance, "repos": $repos}]')
done

instances_json=$(echo "{}" | jq --argjson instances "$instances_list" '.instances = $instances')

echo "$instances_json" | jq '.'