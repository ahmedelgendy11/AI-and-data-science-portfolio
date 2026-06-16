# 🏥 التنبؤ بتكلفة التأمين الصحي

## المشكلة
شركة تأمين محتاجة تسعّر البوالص بدقة بناءً على بيانات العميل (العمر، BMI، التدخين، المنطقة، ...).

## الحل
- تحليل استكشافي يكشف إن **التدخين** هو أكبر عامل بفارق كبير
- هندسة ميزات: `bmi_smoker` interaction, `age²`, `overweight` flag
- مقارنة 5 نماذج: Linear, Ridge, Random Forest, GBM, XGBoost
- تقييم بـ RMSE, MAE, R²

## النتائج
| Model | R² | RMSE |
|---|---|---|
| XGBoost | ~0.95 | ~$2,500 |
| GBM | ~0.94 | ~$2,600 |
| Random Forest | ~0.93 | ~$2,800 |
| Ridge | ~0.92 | ~$3,000 |

أهم العوامل: التدخين > العمر > BMI (خصوصاً للمدخنين) > عدد الأولاد.

## المهارات
`Regression` · `XGBoost` · `Feature Interactions` · `Pipeline` · `ColumnTransformer`

## التشغيل
```bash
conda activate dsportfolio
jupyter notebook b9_insurance_cost_solution.ipynb
```
