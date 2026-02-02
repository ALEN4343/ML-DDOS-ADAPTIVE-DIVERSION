import pandas as pd

def compute_trust_score(anomaly_score, attack_probability):
    """
    Trust Score scaled from 0 to 100
    Higher score = safer traffic
    """
    # Normalize anomaly score (-1 to 1 → 0 to 1)
    norm_anomaly = (anomaly_score + 1) / 2

    # Trust formula
    trust = (0.6 * (1 - attack_probability)) + (0.4 * norm_anomaly)

    # Scale to 0–100
    return trust * 100


if __name__ == "__main__":
    data = pd.read_csv("ml_outputs.csv")

    data["trust_score"] = data.apply(
        lambda row: compute_trust_score(
            row["anomaly_score"], row["attack_probability"]
        ),
        axis=1
    )

    data.to_csv("trust_scores.csv", index=False)
    print("✅ Trust scores generated (0–100). Saved as trust_scores.csv")

