# ⚡ Energy Demand Forecasting — Time Series

> Forecast hourly electricity consumption so a utility can balance supply and demand.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![statsmodels](https://img.shields.io/badge/statsmodels-SARIMA-orange) ![TimeSeries](https://img.shields.io/badge/Time%20Series-forecasting-blueviolet)

## 📌 Problem
Under-producing power causes outages; over-producing wastes money. This project forecasts the next
48 hours of demand (kWh) from a clean hourly series with strong daily seasonality.

## 🧠 Pipeline
1. **Datetime index** with explicit hourly frequency.
2. **Seasonal decomposition** — trend + 24-hour seasonality + residual.
3. **Stationarity** — ADF test; **ACF/PACF** to guide ARIMA orders.
4. **Time-based split** — test on the *last* 48 hours only (no shuffling!).
5. **Models** — Seasonal-Naive baseline → **Holt-Winters** → **SARIMA** (+ optional Prophet).
6. **Evaluation** — RMSE comparison + forecast plot.

## 📈 Results (this dataset)
| Model | RMSE (kWh) |
|---|---|
| Seasonal-Naive (baseline) | 37.8 |
| **Holt-Winters** | **28.4** |
| SARIMA | 29.7 |

Both real models clearly beat the naive baseline; the 24-hour cycle is the dominant signal.

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook c2_timeseries_forecast_solution.ipynb
# optional: pip install prophet  (to enable the Prophet cell)
```

## 🛠️ Skills demonstrated
`Seasonal decomposition` · `ADF stationarity` · `ACF/PACF` · `Time-based validation` ·
`Holt-Winters` · `SARIMA` · `Forecast evaluation`
