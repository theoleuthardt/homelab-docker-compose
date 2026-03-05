# Matrix Server (Synapse) – Homelab Dokumentation

Selbst gehosteter Matrix/Synapse-Server auf `matrix.theocloud.dev`.
Registrierung ist deaktiviert – neue User werden nur per Einladungstoken angelegt.

## Dateien

| Datei | Beschreibung |
|---|---|
| `docker-compose-without-registration.yml` | Produktiv-Setup: Registrierung nur per Token |
| `docker-compose-with-registration.yml` | Offene Registrierung (nur lokal/Dev verwenden) |
| `.env` | Secrets (nicht committen!) |
| `.env.example` | Vorlage für `.env` |

## Dokumentation

- [Setup & Installation](./setup.md)
- [User & Token Verwaltung](./user-management.md)
