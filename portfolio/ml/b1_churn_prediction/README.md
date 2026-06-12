# 🛒 Customer Churn Prediction + Deployment

> End-to-end machine-learning project: predict which e-commerce customers are about to churn, explain *why*, and serve the model as a REST API.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange) ![XGBoost](https://img.shields.io/badge/XGBoost-gradient%20boosting-red) ![FastAPI](https://img.shields.io/badge/FastAPI-deployment-green)

## 📌 Problem
Acquiring a new customer costs 5–7× more than retaining one. This project builds a model that flags
customers likely to **churn** (stop ordering) so the marketing team can target them with retention
offers *before* they leave.

## 🧠 Approach (highlights)
- **Leakage-free target**: features are computed from transactions *before* a cutoff date; the churn
  label is defined from a *future* 90-day window — mirroring how the model is used in production.
- **Feature engineering**: RFM (Recency / Frequency / Monetary), tenure, basket diversity, payment & country.
- **Pipeline**: `ColumnTransformer` (scaling + one-hot) wrapped in a `Pipeline` to prevent leakage.
- **Imbalanced data**: handled via `class_weight` / `scale_pos_weight`.
- **Models compared** with 5-fold Stratified CV (ROC-AUC): Logistic Regression → Random Forest → **XGBoost**.
- **Deep evaluation**: Confusion Matrix, ROC-AUC, PR-AUC, and **threshold tuning** on a cost basis.
- **Interpretability**: **SHAP** values explain global and per-customer drivers.
- **Deployment**: trained pipeline saved with `joblib` and served via **FastAPI**.

## 📂 Structure
```
b1_churn_prediction/
├── b1_churn_prediction_exercise.ipynb   # version with TODOs (to practice)
├── b1_churn_prediction_solution.ipynb   # full working solution
├── data/ecommerce_transactions.csv
├── src/app.py                           # FastAPI service
└── src/churn_model.joblib               # saved after running the notebook
```

## ▶️ How to run
```bash
# 1) create the environment (one-time)
conda create -n dsportfolio python=3.12 -y
conda run -n dsportfolio pip install scikit-learn matplotlib seaborn xgboost shap imbalanced-learn joblib jupyter

# 2) run the solution notebook end-to-end (this also saves src/churn_model.joblib)

# 3) serve the model
cd src
uvicorn app:app --reload
# open http://127.0.0.1:8000/docs  →  POST /predict
```

## 📈 Results (typical)
- XGBoost reaches the best ROC-AUC among the three models.
- Top churn drivers (SHAP): **recency**, **frequency**, **monetary**.
- Threshold tuned for F1 to balance missed-churners vs. wasted offers.

## 🛠️ Skills demonstrated
`Data Leakage avoidance` · `Feature Engineering` · `sklearn Pipelines` · `Imbalanced learning` ·
`XGBoost` · `ROC/PR-AUC` · `SHAP` · `Model serialization` · `FastAPI / MLOps`
