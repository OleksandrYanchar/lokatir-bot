#!/bin/bash
# Install rsync(VPS AND YOUR PC)!!!
# sudo apt/pacman install/-S rsync
rsync -avz -e "ssh -p 22" user@your_vps_ip:/path/to/results.txt /local/path/on/your/pc/





