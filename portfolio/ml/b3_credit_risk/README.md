# 💳 Credit Risk — Loan Default Prediction with Cost-Sensitive Decisions

> Predict loan defaults, **calibrate** the probabilities, and pick the decision threshold that minimizes business cost — not accuracy.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange) ![XGBoost](https://img.shields.io/badge/XGBoost-boosting-red)

## 📌 Problem
A bank must decide whether to approve each loan. The model predicts default probability, but the real
decision balances **the cost of approving a defaulter** (lose the loan) against **rejecting a good
customer** (lose only the profit) — an asymmetric, cost-sensitive problem.

## 🧠 What makes this different from the churn project
- **Probability calibration** (`CalibratedClassifierCV`, isotonic) — money decisions need *honest* probabilities.
- **Cost-based threshold** — minimize `FN·cost_FN + FP·cost_FP` instead of using 0.5.
- **Banking metrics** — KS statistic and Gini, the credit-scoring standards.

## 🧠 Pipeline
EDA → leakage-free preprocessing pipeline → imbalance handling (`class_weight`/`scale_pos_weight`) →
model comparison (ROC-AUC + **PR-AUC**) → **calibration** (Brier + calibration curve) →
**cost-based threshold** (profit/cost curve) → final eval (KS, Gini).

## 📈 Results (this dataset)
| Metric | Value |
|---|---|
| ROC-AUC | ~0.82 |
| Brier (uncalibrated → calibrated) | 0.167 → **0.143** |
| Optimal threshold | **0.15** (vs 0.50) |
| Gini / KS | 0.63 / 0.51 |

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook b3_credit_risk_solution.ipynb
```

## 🛠️ Skills demonstrated
`Imbalanced classification` · `PR-AUC` · `Probability calibration` · `Brier score` ·
`Cost-sensitive thresholding` · `KS / Gini` · `sklearn Pipelines`
