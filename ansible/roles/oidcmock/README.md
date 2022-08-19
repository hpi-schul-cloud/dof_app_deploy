# OpenID Connect Identity Provider Mock Role

This role is used to deploy an OpenID Connect (OIDC) based Identity Provider (IdP) mock server.
It serves testing of login-brokering functionality based on OIDC.

The mock server's settings are adjusted to work in accordance with ErWIn-IDM (acts as IdP-broker) and schulcloud-server (acts as Relying Party, RP).

## Configuration variables

Following configuration group or host variables are used for internal purpose:

| Variable            | Description                           |
| ------------------- | ------------------------------------- |
| OIDCMOCK_IMAGE_NAME | The URL to the OIDC mock docker image |
| OIDCMOCK_IMAGE_TAG  | The OIDC mock docker image tag to use |
| OIDCMOCK_PORT       | Internally used HTTP port             |
| OIDCMOCK_PREFIX     | The OIDC mock base url prefix         |

Following configuration variables are used for internal and external (instance specific) purpose:

| Variable             | Description                         |
| -------------------- | ----------------------------------- |
| OIDCMOCK\_\_BASE_URL | The external base URI the OIDC mock |

## Secrets

Secrets are configured via OnePassword. See `secret.yml` for secret configuration examples. Following secretes are defined:

| Variable                  | Description                      |
| ------------------------- | -------------------------------- |
| OIDCMOCK\_\_CLIENT_ID     | The OIDC client ID               |
| OIDCMOCK\_\_CLIENT_SECRET | The OIDC client secret           |
| OIDCMOCK\_\_USER          | The mock user's username (login) |
| OIDCMOCK\_\_PASSWORD      | The mock user's password         |

## Additional information

More information can be found here:

- Base image: <https://github.com/Soluto/oidc-server-mock>
