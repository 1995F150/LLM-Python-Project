#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/1995F150/cridergpt-engine.git"
DEST_DIR="/opt/cridergpt-engine"
SERVICE_USER="cridergpt"

if ! id "$SERVICE_USER" >/dev/null 2>&1; then
  sudo useradd --system --home-dir "$DEST_DIR" --shell /usr/sbin/nologin "$SERVICE_USER"
fi

if [ -d "$DEST_DIR/.git" ]; then
  sudo git -C "$DEST_DIR" pull --ff-only
else
  sudo git clone "$REPO_URL" "$DEST_DIR"
fi

sudo mkdir -p "$DEST_DIR/data"
sudo python3 -m venv "$DEST_DIR/venv"
sudo "$DEST_DIR/venv/bin/pip" install --upgrade pip
sudo "$DEST_DIR/venv/bin/pip" install -r "$DEST_DIR/requirements.txt"

if [ ! -f "$DEST_DIR/.env" ]; then
  sudo cp "$DEST_DIR/.env.example" "$DEST_DIR/.env"
  sudo chmod 600 "$DEST_DIR/.env"
  echo "Created $DEST_DIR/.env. Fill in its values before starting the service."
  exit 1
fi

sudo chown -R "$SERVICE_USER:$SERVICE_USER" "$DEST_DIR"
sudo chmod 600 "$DEST_DIR/.env"
sudo cp "$DEST_DIR/deployment/cridergpt-engine.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now cridergpt-engine.service
sudo systemctl --no-pager status cridergpt-engine.service

