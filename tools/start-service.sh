#!/bin/bash

APPPLICATION_NAME="loggedme"

REPOSITORY_DIRECTORY=$(dirname "$(dirname $(realpath $0))")
HOSTNAME=$(curl http://169.254.169.254/latest/meta-data/public-hostname)
SERVICE_DIRECTORY=/etc/systemd/system
SERVICE_FILE=$SERVICE_DIRECTORY/$APPPLICATION_NAME.service

echo "[Unit]
Description=Django Project Daemon
After=network.target

[Service]
Type=simple
ExecStart=bash tools/deploy.sh
WorkingDirectory=$REPOSITORY_DIRECTORY

[Install]
WantedBy=multi-user.target" > $SERVICE_FILE

systemctl stop $APPPLICATION_NAME
systemctl daemon-reload

echo ""
echo "Listening to ${HOSTNAME}"
echo ""

systemctl start $APPPLICATION_NAME

echo ""
echo "======== STATUS ========"
echo ""
systemctl status $APPPLICATION_NAME
