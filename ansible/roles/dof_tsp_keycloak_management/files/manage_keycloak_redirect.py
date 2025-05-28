#!/usr/bin/env python3
import os, sys, json, urllib.request, urllib.parse

BASE = os.environ["KEYCLOAK_URL"]
AUTH_REALM = os.environ.get("KEYCLOAK_AUTH_REALM", "master")
TARGET_REALM = os.environ["KEYCLOAK_TARGET_REALM"]
USERNAME = os.environ["KEYCLOAK_USER"]
PASSWORD = os.environ["KEYCLOAK_PASSWORD"]
CLIENT_ID = os.environ["TARGET_CLIENT_ID"]

if len(sys.argv) < 2 or sys.argv[1] not in {"--add", "--remove", "--list"}:
    print("Usage: python manage_redirect.py [--add|--remove <redirect_uri>|--list]", file=sys.stderr)
    sys.exit(1)

action = sys.argv[1]
REDIRECT_URI = sys.argv[2] if len(sys.argv) == 3 else None

# Helper functions
def post_form(url, data):
    req = urllib.request.Request(url, urllib.parse.urlencode(data).encode())
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    return json.load(urllib.request.urlopen(req))

def get_json(url, auth_token):
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {auth_token}")
    return json.load(urllib.request.urlopen(req))

def put_json(url, auth_token, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="PUT")
    req.add_header("Authorization", f"Bearer {auth_token}")
    req.add_header("Content-Type", "application/json")
    return urllib.request.urlopen(req).status

def revoke_token(base_url, realm, token):
    data = {
        "client_id": "admin-cli",
        "token": token
    }
    url = f"{base_url}/realms/{realm}/protocol/openid-connect/logout"
    req = urllib.request.Request(url, urllib.parse.urlencode(data).encode())
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        urllib.request.urlopen(req)
        print("Token revoked.")
    except Exception as e:
        print("Warning: Failed to revoke token:", e, file=sys.stderr)

try:
    token_response = post_form(f"{BASE}/realms/{AUTH_REALM}/protocol/openid-connect/token", {
        "grant_type": "password", "client_id": "admin-cli",
        "username": USERNAME, "password": PASSWORD
    })
    token = token_response["access_token"]
except Exception as e:
    print("Authentication failed:", e, file=sys.stderr)
    sys.exit(1)

clients = get_json(f"{BASE}/admin/realms/{TARGET_REALM}/clients?clientId={CLIENT_ID}", token)
if not clients:
    print("Client not found", file=sys.stderr)
    sys.exit(1)

client_id = clients[0]["id"]

client = get_json(f"{BASE}/admin/realms/{TARGET_REALM}/clients/{client_id}", token)
redirects = client.get("redirectUris", [])
# we need to preserve that field, as when it is absent, client will lose the service account role mappings,
# essentially a necessary workaround until keycloak is updated
# https://github.com/keycloak/keycloak/discussions/16810#discussioncomment-8878792
service_account_enabled = client.get("serviceAccountsEnabled", False)

if action == "--add":
    if not REDIRECT_URI:
        print("Missing redirect URI for --add", file=sys.stderr)
        sys.exit(1)
    if REDIRECT_URI in redirects:
        print("Redirect URI already present.")
    else:
        redirects.append(REDIRECT_URI)
        update_payload = {
            "redirectUris": redirects,
            "serviceAccountsEnabled": service_account_enabled
        }
        status = put_json(f"{BASE}/admin/realms/{TARGET_REALM}/clients/{client_id}", token, update_payload)
        if status == 204:
            print("Redirect URI added.")
        else:
            print(f"Failed to add, status {status}")
elif action == "--remove":
    if not REDIRECT_URI:
        print("Missing redirect URI for --remove", file=sys.stderr)
        sys.exit(1)
    if REDIRECT_URI not in redirects:
        print("Redirect URI not found.")
    else:
        redirects.remove(REDIRECT_URI)
        update_payload = {
            "redirectUris": redirects,
            "serviceAccountsEnabled": service_account_enabled
        }
        status = put_json(f"{BASE}/admin/realms/{TARGET_REALM}/clients/{client_id}", token, update_payload)
        if status == 204:
            print("Redirect URI removed.")
        else:
            print(f"Failed to remove, status {status}")
elif action == "--list":
    print("Redirect URIs:")
    for uri in redirects:
        print(f"- {uri}")

revoke_token(BASE, AUTH_REALM, token)
