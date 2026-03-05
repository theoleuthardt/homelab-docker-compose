# Setup & Installation

## Voraussetzungen

- Docker & Docker Compose
- Domain mit DNS-Eintrag auf deinen Homelab-Server (hier: `matrix.theocloud.dev`)

## Erstes Setup

### 1. Repository klonen / Dateien kopieren

```bash
cd /pfad/zum/projekt
cp .env.example .env
```

### 2. `.env` befüllen

```bash
# Zufälligen Secret generieren
openssl rand -hex 32
```

Dann in `.env` eintragen:

```env
REGISTRATION_SHARED_SECRET=hier_den_generierten_wert_eintragen
```

### 3. Container starten

```bash
docker compose -f docker-compose.yml up -d
```

Beim ersten Start wird automatisch eine `homeserver.yaml` generiert und konfiguriert:
- `enable_registration: true`
- `registration_requires_token: true` (nur per Einladungstoken)
- `registration_shared_secret` (aus `.env`)
- `enable_registration_without_verification: true` (kein SMTP nötig)

### 4. Ersten Admin-User anlegen

Einmalig nach dem ersten Start:

```bash
docker exec -it synapse register_new_matrix_user \
  -u admin \
  -p SICHERESPASSWORT \
  --admin \
  http://localhost:8008
```

> Danach kann dieser Admin-Account über die Admin-API weitere User und Tokens verwalten.

## Container verwalten

```bash
# Logs ansehen
docker compose -f docker-compose.yml logs -f

# Neustart
docker compose -f docker-compose.yml restart

# Stoppen
docker compose -f docker-compose.yml down
```

## Konfiguration anpassen

Die generierte Synapse-Konfiguration liegt im Docker Volume `synapse_data`.
Direkter Zugriff auf die Datei:

```bash
docker exec -it synapse cat /data/homeserver.yaml
```

Änderungen erfordern einen Neustart des Containers.
