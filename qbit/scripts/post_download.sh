#!/bin/bash
# qBittorrent Post-Download Script
# Verschiebt fertige Downloads von /downloads nach /games

TORRENT_NAME="$1"
CONTENT_PATH="$2"
SAVE_PATH="$3"

TARGET_DIR="/games"

# Nur verschieben wenn aus /downloads
if [[ "$SAVE_PATH" == /downloads* ]]; then
    mkdir -p "$TARGET_DIR"

    if [ -d "$CONTENT_PATH" ]; then
        # Ordner verschieben
        mv "$CONTENT_PATH" "$TARGET_DIR/"
    elif [ -f "$CONTENT_PATH" ]; then
        # Datei verschieben
        mv "$CONTENT_PATH" "$TARGET_DIR/"
    fi

    echo "$(date): Moved '$TORRENT_NAME' to $TARGET_DIR" >> /scripts/post_download.log
fi
