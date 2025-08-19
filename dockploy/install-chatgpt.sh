#!/bin/bash

install_dokploy() {
    if [ "$(id -u)" != "0" ]; then
        echo "This script must be run as root" >&2
        exit 1
    fi

    if [ "$(uname)" = "Darwin" ]; then
        echo "This script must be run on Linux" >&2
        exit 1
    fi

    if [ -f /.dockerenv ]; then
        echo "This script must be run on Linux" >&2
        exit 1
    fi

    command_exists() {
        command -v "$@" > /dev/null 2>&1
    }

    if command_exists docker; then
        echo "Docker already installed"
    else
        curl -sSL https://get.docker.com | sh
    fi

    if command_exists docker compose; then
        echo "Docker Compose already installed"
    else
        echo "Installing Docker Compose..."
        curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi

    mkdir -p /etc/dokploy
    chmod 777 /etc/dokploy

    cat <<EOF > /etc/dokploy/docker-compose.yml
services:
  postgres:
    image: postgres:16
    container_name: dokploy-postgres
    environment:
      POSTGRES_USER: dokploy
      POSTGRES_DB: dokploy
      POSTGRES_PASSWORD: amukds4wi9001583845717ad2
    volumes:
      - dokploy-postgres-database:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7
    container_name: dokploy-redis
    volumes:
      - redis-data-volume:/data
    restart: unless-stopped

  dokploy:
    image: dokploy/dokploy:latest
    container_name: dokploy
    ports:
      - "3000:3000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /etc/dokploy:/etc/dokploy
      - dokploy-docker-config:/root/.docker
    environment:
      - ADVERTISE_ADDR=\${ADVERTISE_ADDR}
    restart: unless-stopped

volumes:
  dokploy-postgres-database:
  redis-data-volume:
  dokploy-docker-config:
EOF

    export ADVERTISE_ADDR=$(hostname -I | awk '{print $1}')
    echo "Using advertise address: $ADVERTISE_ADDR"

    cd /etc/dokploy
    docker compose up -d

    GREEN="\033[0;32m"
    YELLOW="\033[1;33m"
    BLUE="\033[0;34m"
    NC="\033[0m"

    echo ""
    printf "${GREEN}Congratulations, Dokploy is installed using Docker Compose!${NC}\n"
    printf "${YELLOW}Please go to http://localhost:3000 or http://<your-server-ip>:3000${NC}\n\n"
}

update_dokploy() {
    echo "Updating Dokploy..."
    cd /etc/dokploy
    docker compose pull dokploy
    docker compose up -d
    echo "Dokploy has been updated to the latest version."
}

if [ "$1" = "update" ]; then
    update_dokploy
else
    install_dokploy
fi
