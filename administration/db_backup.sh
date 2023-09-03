#!/bin/bash

# Directory(VPS)
SOURCE_DIR=

# Directory(local)
DEST_DIR=

# Backup quiz_database.db
rsync -avz -e "ssh -p 22" user@your_vps_ip:${SOURCE_DIR}quiz_database.db ${DEST_DIR}/

# Backup user_data.db
rsync -avz -e "ssh -p 22" user@your_vps_ip:${SOURCE_DIR}user_data.db ${DEST_DIR}/