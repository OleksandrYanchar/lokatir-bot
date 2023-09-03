#!/bin/bash

VPS_USER="NAME"
VPS_IP="YOUR IP"
VPS_PORT="PORT"
FOLDER_LOCATION="bots/lokatir-bot/"

ssh -t -t $VPS_USER@$VPS_IP -p $VPS_PORT << EOF
sleep 10
cd $FOLDER_LOCATION
sleep 10
git pull
sleep 10
reboot
EOF

