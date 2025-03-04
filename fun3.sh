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

instances_json="[]"

for file in "${VERSION_FILES[@]}"; do
    instance=$(basename "$(dirname "$file")")
    repos_json="[]"
    
    while IFS=: read -r key value; do
        key_trimmed=$(echo "$key" | xargs)
        value_trimmed=$(echo "$value" | xargs)
        
        repo_key=${key_trimmed%_IMAGE_TAG}_REPO_NAME
        if [[ -n "${REPO_MAPPING[$repo_key]}" ]]; then
            repo_name="hpi-schul-cloud/${REPO_MAPPING[$repo_key]}"
            repos_json=$(echo "$repos_json" | jq --arg repo "$repo_name" --arg version "$value_trimmed" '. + [{"repo": $repo, "version": $version}]')
        fi
    done < "$file"
    
    instances_json=$(echo "$instances_json" | jq --arg instance "$instance" --argjson repos "$repos_json" '. + [{"instance": $instance, "repos": $repos}]')
done

echo "$instances_json" | jq '.'
