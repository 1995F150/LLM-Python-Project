#!/bin/bash
set -e

REPO_URL="https://github.com/1995F150/cridergpt-engine.git"
DEST_DIR="/opt/cridergpt-engine"

echo "Cloning repository..."
sudo git clone $REPO_URL $DEST_DIR || (cd $DEST_DIR && sudo git pull)

echo "Setting up virtual environment..."
cd $DEST_DIR
sudo python3 -m venv venv
sudo ./venv/bin/pip install --upgrade pip
sudo ./venv/bin/pip install -r requirements.txt

echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo "Configuring cridergpt-engine.service..."
sudo cp deployment/cridergpt-engine.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cridergpt-engine.service
sudo systemctl start cridergpt-engine.service

echo "Installation complete."
