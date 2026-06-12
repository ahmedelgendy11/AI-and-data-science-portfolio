# ❤️ Heart Disease Risk Classifier

> A clinical screening model that predicts heart-disease risk — and a real lesson in catching **data leakage**.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)

## 📌 Problem
A clinic wants a screening tool to flag patients at risk of heart disease from basic vitals, so doctors
prioritize high-risk cases. A medical decision → **interpretability matters**.

## 🧠 Highlight: catching data leakage
The dataset contained a `risk_score` feature correlated **0.80** with the outcome — because it was
*derived from* the diagnosis. Keeping it would inflate accuracy and fail in production. The notebook
**identifies and drops it**, then trains on genuine clinical features.

## 🧠 Pipeline
EDA → **leakage detection & removal** → preprocessing pipeline (median/mode imputation + scaling + one-hot) →
model comparison (LogReg / RF / XGBoost, ROC-AUC) → evaluation (confusion matrix, ROC) → feature importance.

## 📈 Results (this dataset, after removing leakage)
- LogReg **ROC-AUC ≈ 0.91**, accuracy ≈ 0.80.
- Top risk factors: **age, cholesterol, systolic BP** — consistent with medical knowledge (a sanity check that builds trust).

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook b5_heart_disease_solution.ipynb
```

## 🛠️ Skills demonstrated
`Data leakage detection` · `Imputation pipelines` · `Classification` · `ROC-AUC` · `Feature importance` · `Medical interpretability`

> ⚠️ Educational screening aid — not a substitute for a doctor's diagnosis.
