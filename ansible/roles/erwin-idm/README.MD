# Identity Management Role

This role is used to deploy ErWIn Identity Management (ErWIn-IDM), which is a customized Keycloak docker image. The role is used to deployed to all development instances. In the future this role is intend to serve instances for testing (staging) and production as well.

This role will setup ErWIn-IDM and all of its environment. This includes an admin user. No client specific configuration is handled by this role. Please note that this includes the client specific admin user. The configured admin is a global admin. It is not meant to be forwarded to any client application but can be used to create client specific credentials by means of the auto deployment.

This role depends on the 'dof_postgressql' role providing persistence. In 'dof_postgressql', a custom 'erwinidm' schema is created during startup. The PostgreSQL role is shared with 'schulcloud-calendar' and 'hydra'. All stateful data of this role is subject to the persistance provider, i.e. 'dof_postgressql'. Hence, when executing a playbook using this role an existing deployment can and will be overwritten.

## Configuration variables

Following configuration variables are used (see './ansible/group_vars' folder):

| Variable            | Description                             |
| ------------------- | --------------------------------------- |
| ERWINIDM_IMAGE_NAME | The URL to the ErWIn-IDM docker image   |
| ERWINIDM_IMAGE_TAG  | The ErWin-IDM docker image tag to use   |
| ERWINIDM_PORT       | Internally user HTTP port for ErWin-IDM |
| ERWINIDM_PREFIX     | The ErWin-IDM base url prefix           |

## Secrets

Secrets are configured via OnePassword. See `secret.yml` for secret configuration examples or hints.

## Additional information

More information can be found here:

- Base image: <https://github.com/hpi-schul-cloud/erwin-idm/>
- Keycloak specific configuration: <https://www.keycloak.org/server/all-config?options-filter=all#_proxy>
