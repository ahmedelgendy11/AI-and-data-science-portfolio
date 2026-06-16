# ⚡ التنبؤ بالطلب على الطاقة باستخدام ML

## المشكلة
شركة كهرباء محتاجة تتنبأ بالاستهلاك كل ساعة عشان تخطط الإنتاج وتتجنب الانقطاعات.

## الحل
- هندسة ميزات زمنية: **lag features** (1-24 ساعة)، **rolling statistics**، **calendar features**
- تقسيم زمني (temporal split) — الأقدم للتدريب والأحدث للاختبار
- مقارنة 3 نماذج: Ridge, Random Forest, XGBoost
- تحقق بـ **TimeSeriesSplit** (5-fold)

## النتائج
| Model | R² | RMSE | MAPE |
|---|---|---|---|
| XGBoost | ~0.96 | ~12 kWh | ~6% |
| Random Forest | ~0.94 | ~15 kWh | ~8% |
| Ridge | ~0.85 | ~25 kWh | ~13% |

أهم الميزات: lag_1 > lag_24 > hour > rolling_mean > temperature.

## المهارات
`Time Series ML` · `Lag Features` · `Rolling Stats` · `XGBoost` · `Temporal Split` · `TimeSeriesSplit CV`

## التشغيل
```bash
conda activate dsportfolio
jupyter notebook b8_demand_forecast_solution.ipynb
```
