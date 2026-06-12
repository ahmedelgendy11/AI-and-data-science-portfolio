# 🏠 House Price Prediction — Regression

> Estimate property prices from their features — a "Zestimate"-style automated valuation model.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange) ![XGBoost](https://img.shields.io/badge/XGBoost-regression-red)

## 📌 Problem
A real-estate platform wants an automated tool to estimate a fair listing price from a property's
attributes (size, bedrooms, neighborhood, age…), speeding up valuation.

## 🧠 Pipeline
1. **EDA** — correlations, missing values, price-vs-feature plots.
2. **Target transform** — `log1p` to fix right-skewed prices (metrics reported back in $).
3. **Preprocessing pipeline** — median/most-frequent imputation + scaling + one-hot, leakage-free.
4. **Feature engineering** — `house_age` from `year_built`.
5. **Model comparison (5-fold CV)** — Linear / Ridge / Lasso / Random Forest / **XGBoost**, scored in RMSE dollars.
6. **Evaluation** — RMSE, MAE, R² on the test set.
7. **Residual analysis** — check for bias / missing structure.
8. **Feature importance**.

## 📈 Results (this dataset)
| Model | CV RMSE |
|---|---|
| Linear / Ridge / Lasso | ~$28k |
| **XGBoost** | **$23.6k** |

Test set: RMSE ≈ **$20.8k**, MAE ≈ $16.3k, **R² ≈ 0.985**. Top drivers: square footage, neighborhood, bathrooms.

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook b2_house_prices_solution.ipynb
```

## 🛠️ Skills demonstrated
`EDA` · `Skewness correction` · `Imputation` · `sklearn Pipelines` · `Ridge/Lasso regularization` ·
`Gradient Boosting` · `Residual analysis` · `Feature importance`
