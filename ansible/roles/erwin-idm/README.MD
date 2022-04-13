# Identity Management Role

This role is used to deploy ErWIn Identity Management (ErWIn-IDM), which is a customized Keycloak docker image. The role is used to deployed to all development instances. In the future this role is intend to serve instances for testing (staging) and production as well.

This role will setup ErWIn-IDM and all of its environment. This includes an admin user. No client specific configuration is handled by this role. Please note that this includes the client specific admin user. The configured admin is a global admin. It is not meant to be forwarded to any client application but can be used to create client specific credentials by means of the auto deployment.

In develop environnement, this role depends on the 'dof_postgresql' role providing persistence. In 'dof_postgresql', a custom 'erwinidm' schema is created during startup. The PostgreSQL role is shared with 'schulcloud-calendar' and 'hydra'.

All stateful data of this role is subject to the persistance provider, i.e. the given PostgreSQL. Hence, an existing deployment of this role can safely be removed and re-deployed when needed.

## Configuration variables

Following configuration group or host variables are used:

| Variable                 | Description                                  |
| ------------------------ | -------------------------------------------- |
| ERWINIDM_IMAGE_NAME      | The URL to the ErWIn-IDM docker image        |
| ERWINIDM_IMAGE_TAG       | The ErWin-IDM docker image tag to use        |
| ERWINIDM_PORT            | Internally user HTTP port for ErWin-IDM      |
| ERWINIDM_PREFIX          | The ErWin-IDM base url prefix                |
| ERWINIDM_REPLICAS        | Deployment maximum amount of replica Pods    |
| ERWINIDM_CPU_LIMITS      | Deployment CPU upper bound                   |
| ERWINIDM_CPU_REQUESTS    | Deployment CPU lower bound                   |
| ERWINIDM_MEMORY_LIMITS   | Deployment memory upper bound                |
| ERWINIDM_MEMORY_REQUESTS | Deployment memory lower bound                |

## Secrets

Secrets are configured via OnePassword. See `secret.yml` for secret configuration examples

| Variable                 | Description                                  |
| ------------------------ | -------------------------------------------- |
| ERWINIDM_ADMIN_USER      | The Keycloak super admin                     |
| ERWINIDM_ADMIN_PASSWORD  | The Keycloak super admin's password          |
| ERWINIDM_DB_URL          | Connection string to PostgreSQL in JDBC Format, e.g. 'jdbc:postgresql://postgres:5432/postgres?currentSchema=\<schema\>'. This must include the used schema, see: <https://github.com/keycloak/ keycloak/issues/10235> |
| ERWINIDM_DB_USER         | The PostgreSQL user                          |
| ERWINIDM_DB_PASSWORD     | The PostgreSQL user's passsword              |

## Additional information

More information can be found here:

- Base image: <https://github.com/hpi-schul-cloud/erwin-idm/>
- Keycloak specific configuration: <https://www.keycloak.org/server/all-config?options-filter=all#_proxy>
