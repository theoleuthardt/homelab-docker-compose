#!/usr/bin/env python3
"""
Erstellt einen Matrix-Einladungslink für einen neuen User.
Nutzung: python create_invite.py
"""

import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# Nur für den generierten Link – API-Calls gehen direkt über localhost
PUBLIC_URL = "https://matrix.theocloud.dev"
HOMESERVER = "http://192.168.12.151:8008"
ADMIN_USER = "admin"


def login(password: str) -> str:
    data = json.dumps({
        "type": "m.login.password",
        "user": ADMIN_USER,
        "password": password,
    }).encode()

    req = urllib.request.Request(
        f"{HOMESERVER}/_matrix/client/v3/login",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["access_token"]


def create_token(access_token: str, uses: int, expires_in_hours: int | None) -> str:
    payload: dict = {"uses_allowed": uses}

    if expires_in_hours:
        expiry = datetime.now() + timedelta(hours=expires_in_hours)
        payload["expiry_time"] = int(expiry.timestamp() * 1000)

    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{HOMESERVER}/_synapse/admin/v1/registration_tokens/new",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["token"]


def main():
    password = input(f"Admin-Passwort für '{ADMIN_USER}': ")

    uses_input = input("Wie oft soll der Link nutzbar sein? [1]: ").strip()
    uses = int(uses_input) if uses_input else 1

    expires_input = input("Ablauf in Stunden? (leer = kein Ablauf): ").strip()
    expires_in_hours = int(expires_input) if expires_input else None

    print("\nErstelle Token...")
    try:
        access_token = login(password)
        token = create_token(access_token, uses, expires_in_hours)
    except urllib.error.HTTPError as e:
        print(f"Fehler: {e.status} – {e.read().decode()}")
        return

    link = f"{PUBLIC_URL}/#/register?token={token}"
    print(f"\nEinladungslink:\n{link}")
    if expires_in_hours:
        expires_at = datetime.now() + timedelta(hours=expires_in_hours)
        print(f"Gültig bis: {expires_at.strftime('%d.%m.%Y %H:%M')}")
    print(f"Nutzungen: {uses}x")


if __name__ == "__main__":
    main()
