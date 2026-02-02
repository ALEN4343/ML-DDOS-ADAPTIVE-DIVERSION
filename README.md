# Role 1 – ML + Controller Engineer

## Overview
This module implements a hybrid ML-based DDoS detection and controller system.

## Files
- ml_model.py – ML detection pipeline
- trust_score_logic.py – Trust score computation (0–100)
- controller.py – Traffic decision logic
- rule_templates.txt – Mitigation rule templates

## How to Run
1. Run ML pipeline:
   python3 ml_model.py

2. Generate trust scores:
   python3 trust_score_logic.py

3. Apply controller logic:
   python3 controller.py

## Outputs
- ml_outputs.csv
- trust_scores.csv
- controller_output.csv

