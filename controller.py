import pandas as pd

data = pd.read_csv("trust_scores.csv")

decisions = []

for _, row in data.iterrows():
    T = row["trust_score"]

    if T > 70:
        decision = "ALLOW"
    elif 40 < T <= 70:
        decision = "DIVERT"
    else:
        decision = "BLOCK_RATE_LIMIT"

    decisions.append(decision)

data["decision"] = decisions
data.to_csv("controller_output.csv", index=False)

print("✅ Controller decisions applied and saved.")

