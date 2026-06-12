# 🔬 Full ML Pipeline + Experiment Tracking (MLflow)

> A complete, reproducible regression pipeline where **every experiment is tracked** — params, metrics, and the model artifact — with **MLflow**, then the best run is reloaded from the registry.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-pipeline-orange) ![MLflow](https://img.shields.io/badge/MLflow-tracking-0194E2)

## 📌 Problem
A team trains many models with many settings and loses track of *which run was best, and with what config*.
Without tracking, results aren't reproducible. This project wires a proper pipeline to **MLflow experiment
tracking** so every trial is logged, comparable, and reloadable.

## 🧠 Pipeline
Feature engineering (`house_age`) → preprocessing `Pipeline` (scaling + one-hot via `ColumnTransformer`) →
train **Ridge / RandomForest / XGBoost**, each in its own **MLflow run** logging params + CV-RMSE +
test RMSE/MAE/R² + the serialized model → `search_runs` to pick the best by test-RMSE → reload the best
model from the MLflow registry and check residuals.

## 📈 What gets tracked per run
`params` (model type + hyperparameters) · `metrics` (cv_rmse, test_rmse, test_mae, test_r2) ·
`model` artifact (full sklearn pipeline, reloadable via `runs:/<id>/model`).

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook c1_mlflow_pipeline_solution.ipynb
```
View the experiment dashboard:
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db    # open http://localhost:5000
```

## 🛠️ Skills demonstrated
`sklearn Pipeline` · `ColumnTransformer` · `Cross-Validation` · `MLflow tracking` · `Model registry` · `Model selection` · `MLOps`

> 🧩 Tracking is the foundation of MLOps — reproducibility, comparison, and governance of models.
