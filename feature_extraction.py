from scapy.all import rdpcap, IP, TCP, UDP
import pandas as pd
import numpy as np
import math
from collections import defaultdict

# Path to PCAP file
PCAP_PATH = "pcaps/traffic.pcap"

print("Script started")

# Read packets
packets = rdpcap(PCAP_PATH)
print("Number of packets read:", len(packets))

flows = defaultdict(list)

# Group packets into flows
for pkt in packets:
    if IP in pkt:
        proto = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "OTHER"
        sport = pkt[TCP].sport if TCP in pkt else pkt[UDP].sport if UDP in pkt else 0
        dport = pkt[TCP].dport if TCP in pkt else pkt[UDP].dport if UDP in pkt else 0

        key = (
            pkt[IP].src,
            pkt[IP].dst,
            sport,
            dport,
            proto
        )
        flows[key].append(pkt)

# Entropy calculation
def entropy(values):
    probs = [values.count(v) / len(values) for v in set(values)]
    return -sum(p * math.log2(p) for p in probs if p > 0)

rows = []

# Extract features per flow
for flow, pkts in flows.items():
    times = [p.time for p in pkts]
    duration = max(times) - min(times) if len(times) > 1 else 0.0001

    total_packets = len(pkts)
    total_bytes = sum(len(p) for p in pkts)

    pps = total_packets / duration
    bps = total_bytes / duration

    syn_count = 0
    ack_count = 0
    ttl_values = []
    sizes = []

    for p in pkts:
        if TCP in p:
            if p[TCP].flags & 0x02:
                syn_count += 1
            if p[TCP].flags & 0x10:
                ack_count += 1
        if IP in p:
            ttl_values.append(p[IP].ttl)
        sizes.append(len(p))

    syn_rate = syn_count / duration
    ack_ratio = ack_count / (syn_count + 1)
    ttl_dev = np.std(ttl_values) if ttl_values else 0
    size_entropy = entropy(sizes)
    repetition = total_packets / len(set(sizes)) if len(set(sizes)) > 0 else 0

    rows.append([
        pps,
        bps,
        duration,
        syn_rate,
        ack_ratio,
        ttl_dev,
        size_entropy,
        repetition
    ])

# Create dataset
columns = [
    "pps",
    "bps",
    "flow_duration",
    "syn_rate",
    "ack_ratio",
    "ttl_deviation",
    "entropy",
    "repetition"
]

df = pd.DataFrame(rows, columns=columns)
df["label"] = 0  # temporary label

df.to_csv("dataset.csv", index=False)

print("dataset.csv created successfully")
