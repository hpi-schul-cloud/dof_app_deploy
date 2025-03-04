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
              repos_list=""
              
              while IFS=: read -r key value; do
                  key_trimmed=$(echo "$key" | xargs)
                  value_trimmed=$(echo "$value" | xargs)
                  
                  repo_key=${key_trimmed%_IMAGE_TAG}_REPO_NAME
                  if [[ -n "${REPO_MAPPING[$repo_key]}" ]]; then
                      repo_name="hpi-schul-cloud/${REPO_MAPPING[$repo_key]}:$value_trimmed"
                      repos_list+="$repo_name;"
                  fi
              done < "$file"
              
              # Remove trailing semicolon
              repos_list=${repos_list%;}
              
              instances_json=$(echo "$instances_json" | jq --arg instance "$instance" --arg repos "$repos_list" '. + [{"instance": $instance, "repos": $repos}]')
          done
          echo $instances_json
