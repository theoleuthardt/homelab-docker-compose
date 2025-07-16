# 🧪 Homelab Docker Compose Files
Welcome to my Homelab! This repository contains all my `docker-compose.yml` files used to manage various self-hosted services running in my local environment.

## 📁 Structure
Each service is organized into its own subdirectory with its own `docker-compose.yml` file and any required configuration files.
```
/
├── portainer/
├── immich/
└── ...
```

## ▶️ Usage
To start any service, navigate into its directory and use `docker compose`:

```bash
cd <service-name>
docker compose up -d
```

> **Note:** Make sure Docker and Docker Compose are installed on your system.

## ⚙️ Configuration
Most services use `.env` files for sensitive values like passwords, ports, or volume paths. These files are **not** included in the repo. If available, you’ll find an `.env.example` to help you get started.

## 📦 Requirements
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

## 🔐 Security
- This repo contains **no secrets or passwords**.
- `.env` files and other sensitive configs are excluded via `.gitignore`.
---

> 📬 Questions or feedback? Open an issue or reach out!