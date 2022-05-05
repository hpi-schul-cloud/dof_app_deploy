# Identity Management Role

This role is used to deploy ErWIn Identity Management (ErWIn-IDM), which is a customized Keycloak docker image. The role is used to deployed to all development instances. In the future this role is intend to serve instances for testing (staging) and production as well.

This role will setup ErWIn-IDM and all of its environment. This includes a global admin, which is not meant to be forwarded to any client application but is used to create client specific credentials by means of the auto deployment.

This role will setup a dBildungscloud specific realm, client, and corresponding admin user. It does not support partial updates. If the target realm already exists, all further initialization steps are skipped.

In develop environment, this role depends on the 'dof_postgresql' role providing persistence. In 'dof_postgresql', a custom 'erwinidm' schema is created during startup. The PostgreSQL role is shared with 'schulcloud-calendar' and 'hydra'.

All stateful data of this role is subject to the persistance provider, i.e. the given PostgreSQL. Hence, an existing deployment of this role can safely be removed and re-deployed when needed.

## Configuration variables

Following configuration group or host variables are used for internal purpose:

| Variable                 | Description                               |
| ------------------------ | ----------------------------------------- |
| ERWINIDM_IMAGE_NAME      | The URL to the ErWIn-IDM docker image     |
| ERWINIDM_IMAGE_TAG       | The ErWin-IDM docker image tag to use     |
| ERWINIDM_PORT            | Internally user HTTP port for ErWin-IDM   |
| ERWINIDM_PREFIX          | The ErWin-IDM base url prefix             |
| ERWINIDM_REPLICAS        | Deployment maximum amount of replica Pods |
| ERWINIDM_CPU_LIMITS      | Deployment CPU upper bound                |
| ERWINIDM_CPU_REQUESTS    | Deployment CPU lower bound                |
| ERWINIDM_MEMORY_LIMITS   | Deployment memory upper bound             |
| ERWINIDM_MEMORY_REQUESTS | Deployment memory lower bound             |

Following configuration variables are used for internal and external (dBildungscloud) purpose:

| Variable                        | Description                                                   |
| ------------------------------- | ------------------------------------------------------------- |
| IDENTITY_MANAGEMENT\_\_URI      | The internal base URI of Keycloak                             |
| IDENTITY_MANAGEMENT\_\_TENANT   | The realm (tenant) name for dBildungscloud                    |
| IDENTITY_MANAGEMENT\_\_CLIENTID | The default OpenID Connect client of the dBildungscloud realm |

## Secrets

Secrets are configured via OnePassword. See `secret.yml` for secret configuration examples. Following secretes are defined:

| Variable                              | Description                                                |
| ------------------------------------- | ---------------------------------------------------------- |
| KEYCLOAK_ADMIN                        | The Keycloak super admin                                   |
| KEYCLOAK_ADMIN_PASSWORD               | The Keycloak super admin's password                        |
| KC_DB_URL                             | Connection string to PostgreSQL in JDBC Format [^psqlnote] |
| KC_DB_USERNAME                        | The PostgreSQL user                                        |
| KC_DB_PASSWORD                        | The PostgreSQL user's password                             |
| IDENTITY_MANAGEMENT\_\_ADMIN_USER     | dBildungscloud realm admin                                 |
| IDENTITY_MANAGEMENT\_\_ADMIN_PASSWORD | dBildungscloud realm admin's password                      |
| IDENTITY_MANAGEMENT\_\_ADMIN_CLIENTID | dBildungscloud realm admin defined client                  |

[^psqlnote]: The connection string has to be given in JDBC Format, e.g. 'jdbc:postgresql://postgres:5432/postgres?currentSchema=\<schema\>'. This must include the used schema, see: <https://github.com/keycloak/keycloak/issues/10235>

## Additional information

More information can be found here:

- Base image: <https://github.com/hpi-schul-cloud/erwin-idm/>
- Keycloak specific configuration: <https://www.keycloak.org/server/all-config?options-filter=all#_proxy>
- Keycloak Admin API: <https://www.keycloak.org/docs-api/17.0/rest-api/index.html>
