# 🕵️ Fraud Detection — Anomaly Detection + Imbalanced ML

> Flag fraudulent transactions when fraud is rare (~3%) and the review team can only inspect a few per day.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange) ![XGBoost](https://img.shields.io/badge/XGBoost-boosting-red)

## 📌 Problem
Fraud is a rare event, so accuracy is useless (always-"legit" scores 96%+). The goal is to **rank**
transactions by risk so analysts review the riskiest first, within a limited daily budget.

## 🧠 What makes this different from credit risk
- **Unsupervised anomaly detection** (`IsolationForest`) — find the odd-one-out *without labels*.
- **PR-AUC instead of ROC-AUC** — honest for rare events.
- **Precision@k** — the operational metric: "of the top-k flagged, how many are fraud?"

## 🧠 Pipeline
EDA (extreme imbalance) → preprocessing → **Isolation Forest** (no labels) →
supervised models (LogReg + XGBoost with `scale_pos_weight`) → **PR-AUC** comparison →
**Precision@k** under a review budget → PR curves.

## 📈 Results (this dataset, fraud ≈ 3.4%)
| Model | PR-AUC |
|---|---|
| Isolation Forest (unsupervised) | 0.22 |
| LogReg | 0.31 |
| **XGBoost** | **0.32** |

Baseline PR-AUC ≈ 0.034 → ~**9× lift**. **Precision@50 = 58%** (17× better than random);
reviewing the top 500 catches **55%** of all fraud.

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook b4_fraud_detection_solution.ipynb
```

## 🛠️ Skills demonstrated
`Extreme imbalance` · `Isolation Forest` · `PR-AUC` · `Precision@k` · `Supervised vs unsupervised`
