# OpenID Connect Identity Provider Mock Role

This role is used to deploy OpenID Connect (OIDC) based Identity Provider (IdP) mock server.
It serves testing purposes for login brokering based on OIDC.

The settings are adjusted to work in accordance with ErWIn-IDM (acts as IdP-broker) and schulcloud-server (acts ad Relying Party, RP).

## Configuration variables

Following configuration group or host variables are used for internal purpose:

| Variable            | Description                             |
| ------------------- | --------------------------------------- |
| OIDCMOCK_IMAGE_NAME | The URL to the ErWIn-IDM docker image   |
| OIDCMOCK_IMAGE_TAG  | The ErWin-IDM docker image tag to use   |
| OIDCMOCK_PORT       | Internally user HTTP port for ErWin-IDM |
| OIDCMOCK_PREFIX     | The ErWin-IDM base url prefix           |

Following configuration variables are used for internal and external (instance specific) purpose:

| Variable             | Description                       |
| -------------------- | --------------------------------- |
| OIDCMOCK\_\_BASE_URL | The external base URI of Keycloak |

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
