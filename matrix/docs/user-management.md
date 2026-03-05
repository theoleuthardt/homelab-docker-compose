# User & Token Verwaltung

Registrierung ist nicht offen – neue User können nur über Einladungstokens beitreten.

## Access Token holen

Für alle Admin-API-Aufrufe wird ein Access Token benötigt.
Nach dem Login mit dem Admin-Account:

```bash
curl -X POST 'http://localhost:8008/_matrix/client/v3/login' \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "m.login.password",
    "user": "admin",
    "password": "DEINPASSWORT"
  }'
```

Den `access_token` aus der Antwort für alle weiteren Befehle verwenden.

---

## Einladungstokens

### Token erstellen (Einmalnutzung)

```bash
curl -X POST 'http://localhost:8008/_synapse/admin/v1/registration_tokens/new' \
  -H 'Authorization: Bearer DEIN_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"uses_allowed": 1}'
```

### Token mit Ablaufdatum erstellen

```bash
curl -X POST 'http://localhost:8008/_synapse/admin/v1/registration_tokens/new' \
  -H 'Authorization: Bearer DEIN_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "uses_allowed": 1,
    "expiry_time": 1800000
  }'
```

> `expiry_time` ist ein Unix-Timestamp in Millisekunden.

### Alle aktiven Tokens anzeigen

```bash
curl 'http://localhost:8008/_synapse/admin/v1/registration_tokens' \
  -H 'Authorization: Bearer DEIN_ACCESS_TOKEN'
```

### Token löschen

```bash
curl -X DELETE \
  'http://localhost:8008/_synapse/admin/v1/registration_tokens/TOKEN_HIER' \
  -H 'Authorization: Bearer DEIN_ACCESS_TOKEN'
```

### Einladungslink an Freund schicken

```
https://matrix.theocloud.dev/#/register?token=TOKEN_AUS_DEM_ERSTELL-BEFEHL
```

Der Freund öffnet den Link in einem Matrix-Client (z.B. Element Web) und kann sich damit registrieren.

---

## User direkt per CLI anlegen

Ohne Einladungstoken – direkt über den Container (braucht `registration_shared_secret` in `.env`):

```bash
docker exec -it synapse register_new_matrix_user \
  -u BENUTZERNAME \
  -p INITIALPASSWORT \
  http://localhost:8008
```

Mit Admin-Rechten:

```bash
docker exec -it synapse register_new_matrix_user \
  -u BENUTZERNAME \
  -p INITIALPASSWORT \
  --admin \
  http://localhost:8008
```

---

## User über Admin-API verwalten

### User anlegen oder Passwort setzen

```bash
curl -X PUT \
  'http://localhost:8008/_synapse/admin/v2/users/@BENUTZERNAME:matrix.theocloud.dev' \
  -H 'Authorization: Bearer DEIN_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "password": "NEUESPASSWORT",
    "admin": false
  }'
```

### User deaktivieren

```bash
curl -X POST \
  'http://localhost:8008/_synapse/admin/v1/deactivate/@BENUTZERNAME:matrix.theocloud.dev' \
  -H 'Authorization: Bearer DEIN_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"erase": false}'
```

### Alle User auflisten

```bash
curl 'http://localhost:8008/_synapse/admin/v2/users?from=0&limit=100' \
  -H 'Authorization: Bearer DEIN_ACCESS_TOKEN'
```
