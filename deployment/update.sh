#!/usr/bin/env bash
set -euo pipefail

DEST_DIR="/opt/cridergpt-engine"
sudo git -C "$DEST_DIR" pull --ff-only
sudo "$DEST_DIR/venv/bin/pip" install -r "$DEST_DIR/requirements.txt"
sudo chown -R cridergpt:cridergpt "$DEST_DIR"
sudo chmod 600 "$DEST_DIR/.env"
sudo systemctl restart cridergpt-engine.service
curl --fail --silent http://127.0.0.1:8000/health

