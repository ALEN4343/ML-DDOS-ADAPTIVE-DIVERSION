import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

# -----------------------------
# 1. Load dataset
# -----------------------------
data = pd.read_csv("dataset.csv")

X = data.drop("label", axis=1)
y = data["label"]

print("Label distribution:")
print(y.value_counts())

# -----------------------------
# 2. Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# -----------------------------
# 3. Anomaly Detection (Isolation Forest)
# -----------------------------
iso = IsolationForest(contamination=0.1, random_state=42)
iso.fit(X_train)

anomaly_scores = iso.decision_function(X_test)

# -----------------------------
# 4. Supervised Classification (Random Forest)
# -----------------------------
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

# Handle single-class / multi-class safely
proba = rf.predict_proba(X_test)

if proba.shape[1] == 2:
    attack_prob = proba[:, 1]   # probability of attack
else:
    attack_prob = proba[:, 0]   # only one class present

print("Classes detected:", rf.classes_)

# -----------------------------
# 5. Evaluation Metrics
# -----------------------------
print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, zero_division=0))
print("Recall   :", recall_score(y_test, y_pred, zero_division=0))

# -----------------------------
# 6. Save outputs for next steps
# -----------------------------
results = pd.DataFrame({
    "anomaly_score": anomaly_scores,
    "attack_probability": attack_prob
})

results.to_csv("ml_outputs.csv", index=False)

print("✅ ML Step-2 completed. Output saved as ml_outputs.csv")

