# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 🏠 التنبؤ بأسعار العقارات (House Price Prediction — Regression)
### مشروع B2 — مسار تعلم الآلة (Machine Learning Track)

---
## 🎯 المشكلة التجارية (Business Problem)
منصة عقارات عايزة **أداة تقدير تلقائي لسعر البيت** (زي Zillow's Zestimate) عشان تساعد البائعين
والمشترين يحطّوا سعر عادل، وتسرّع التقييم بدل المثمّن البشري.

**نوع المشكلة:** انحدار (Regression) — التنبؤ بقيمة رقمية مستمرة (السعر).

## 📦 ما الذي يثبته المشروع
معالجة القيم المفقودة · **تصحيح الالتواء (Skewness) باللوغاريتم** · Pipeline احترافي ·
**الانحدار المنتظم (Ridge/Lasso)** · Gradient Boosting · **تحليل البواقي (Residual Analysis)** · تفسير المعاملات.
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| الانحدار الخطي وافتراضاته | ISLR (ch.3) | الأساس — لازم تفهم قبل أي حاجة |
| **التواء الهدف + Log transform** | Feature Eng. for ML (Zheng) | الأسعار ملتوية يمين → اللوغاريتم بيحسّن النموذج |
| القيم المفقودة (Imputation) | Géron (ch.2) | بيانات الواقع دايماً ناقصة |
| **الانتظام (Ridge / Lasso)** | ISLR (ch.6) | منع الـ overfitting + اختيار الميزات |
| Pipeline & ColumnTransformer | Géron (ch.2) | منع التسريب وتنظيم المعالجة |
| مقاييس الانحدار (RMSE, MAE, R²) | ISLR (ch.3) | تقييم الخطأ بوحدات السعر الحقيقية |
| **تحليل البواقي (Residuals)** | ISLR (ch.3) | كشف هل النموذج متحيّز أو ناقص ميزات |

> 🎯 **بيُستخدم في الواقع:** تقييم العقارات، تسعير السيارات المستعملة، تقدير قيمة الأصول، التأمين.
""")

md("## 0️⃣ المكتبات")
code("""import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
sns.set_style('whitegrid'); np.random.seed(42)
print('ready ✓')""")

md("## 1️⃣ تحميل واستكشاف البيانات (EDA)")
code("""df = pd.read_csv('data/house_prices_data.csv')
print('Shape:', df.shape)
print('Missing:\\n', df.isna().sum()[df.isna().sum() > 0])
df.describe().T[['mean','std','min','max']]""",
stub="""df = pd.read_csv('data/house_prices_data.csv')
# TODO: اطبع shape والقيم المفقودة، واستعرض describe()
print(df.shape)""")

code("""corr = df.corr(numeric_only=True)['sale_price'].sort_values(ascending=False)
print('Correlation with price:\\n', corr.round(2))
fig, ax = plt.subplots(1,2, figsize=(13,4))
sns.scatterplot(data=df, x='square_footage', y='sale_price', ax=ax[0], alpha=.4)
ax[0].set_title('Price vs Square Footage')
sns.boxplot(data=df, x='neighborhood', y='sale_price', ax=ax[1]); ax[1].set_title('Price by Neighborhood')
plt.tight_layout(); plt.show()""")

md(r"""## 2️⃣ تصحيح التواء الهدف (Target Skewness → Log) 📐
أسعار العقارات **ملتوية لليمين** (قليل من البيوت غالية جداً). الانحدار الخطي بيفترض توزيع متماثل،
فبنطبّق `log1p` على السعر — ده بيحسّن الأداء بشكل ملحوظ. (نرجّع بـ `expm1` عند التقييم).""")
code("""fig, ax = plt.subplots(1,2, figsize=(12,3.5))
sns.histplot(df['sale_price'], kde=True, ax=ax[0]); ax[0].set_title(f"Original (skew={df['sale_price'].skew():.2f})")
sns.histplot(np.log1p(df['sale_price']), kde=True, ax=ax[1], color='green')
ax[1].set_title(f"Log (skew={np.log1p(df['sale_price']).skew():.2f})")
plt.tight_layout(); plt.show()""",
stub="""# TODO: قارن توزيع السعر قبل وبعد log1p (اطبع الـ skew)
...""")

md("## 3️⃣ هندسة الميزات والمعالجة (Pipeline)")
code("""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

df['house_age'] = 2024 - df['year_built']                 # ميزة جديدة أوضح من سنة البناء
X = df.drop(columns=['sale_price', 'house_id', 'year_built'])
y = np.log1p(df['sale_price'])                            # الهدف باللوغاريتم

num = ['square_footage','bedrooms','bathrooms','garage_spaces','house_age']
cat = ['neighborhood']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pre = ColumnTransformer([
    ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('sc', StandardScaler())]), num),
    ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')),
                      ('oh', OneHotEncoder(handle_unknown='ignore'))]), cat),
])
print('Train:', X_train.shape, '| Test:', X_test.shape)""",
stub="""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
# TODO: اعمل ميزة house_age، خُد y = log1p(sale_price)
# TODO: ColumnTransformer = imputer+scaler للأرقام، imputer+onehot للفئات
df['house_age'] = ...
X = ...; y = ...
pre = ColumnTransformer([...])""")

md("## 4️⃣ مقارنة الموديلات بالـ Cross-Validation (RMSE بوحدات السعر)")
code("""from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_predict

def rmse_price(y_log_true, y_log_pred):
    return np.sqrt(np.mean((np.expm1(y_log_true) - np.expm1(y_log_pred))**2))

models = {
    'Linear': LinearRegression(),
    'Ridge':  Ridge(alpha=1.0),
    'Lasso':  Lasso(alpha=0.001),
    'RandomForest': RandomForestRegressor(n_estimators=300, random_state=42),
    'XGBoost': XGBRegressor(n_estimators=400, learning_rate=0.05, max_depth=4, random_state=42),
}
for name, m in models.items():
    pipe = Pipeline([('pre', pre), ('m', m)])
    pred = cross_val_predict(pipe, X_train, y_train, cv=5)
    print(f'{name:14} CV RMSE = ${rmse_price(y_train, pred):,.0f}')""",
stub="""from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_predict
# TODO: عرّف rmse_price ترجع الخطأ بوحدات السعر (expm1)
# TODO: قارن Linear/Ridge/Lasso/RF/XGBoost بـ 5-fold CV
def rmse_price(yt, yp): ...
models = {...}""")

md("## 5️⃣ تدريب أفضل موديل وتقييمه على الاختبار")
code("""from sklearn.metrics import mean_absolute_error, r2_score
best = Pipeline([('pre', pre), ('m', models['XGBoost'])])
best.fit(X_train, y_train)
pred_log = best.predict(X_test)
pred, true = np.expm1(pred_log), np.expm1(y_test)
print(f'Test RMSE = ${rmse_price(y_test, pred_log):,.0f}')
print(f'Test MAE  = ${mean_absolute_error(true, pred):,.0f}')
print(f'Test R²   = {r2_score(true, pred):.3f}')""",
stub="""from sklearn.metrics import mean_absolute_error, r2_score
# TODO: درّب أفضل موديل، تنبّأ، ارجع للسعر بـ expm1، واطبع RMSE/MAE/R²
best = ...""")

md(r"""## 6️⃣ تحليل البواقي (Residual Analysis) 🔍
البواقي = (الحقيقي − المتوقع). المفروض تكون **عشوائية حول الصفر**. أي نمط فيها = الموديل بيفوّت حاجة.""")
code("""resid = true - pred
fig, ax = plt.subplots(1,2, figsize=(13,4))
ax[0].scatter(pred, resid, alpha=.4); ax[0].axhline(0, color='red', ls='--')
ax[0].set_xlabel('Predicted'); ax[0].set_ylabel('Residual'); ax[0].set_title('Residuals vs Predicted')
sns.histplot(resid, kde=True, ax=ax[1]); ax[1].set_title('Residual distribution')
plt.tight_layout(); plt.show()""")

md("## 7️⃣ أهمية الميزات (Feature Importance)")
code("""feat = best.named_steps['pre'].get_feature_names_out()
imp = pd.Series(best.named_steps['m'].feature_importances_, index=feat).sort_values()
imp.plot(kind='barh', figsize=(7,4), title='XGBoost Feature Importance'); plt.tight_layout(); plt.show()""")

md(r"""## 8️⃣ الخلاصة والتوصيات (Conclusion)
- **النتيجة:** XGBoost حقّق أقل RMSE وأعلى R² — يقدر يقدّر السعر بدقة كويسة.
- **أهم العوامل:** المساحة (square footage)، الحي (neighborhood)، عدد الحمامات — متوافق مع منطق السوق.
- **اللوغاريتم:** تحويل الهدف حسّن الأداء وخلّى البواقي أقرب للتوزيع الطبيعي.
- **التوصية:** استخدام الموديل كأداة تقدير أولي + مراجعة بشرية للحالات الشاذة (بواقي كبيرة).
- **الخطوة القادمة:** إضافة ميزات الموقع الدقيق، المسافة للخدمات، وبيانات السوق الزمنية.

> ✅ **اللي اتعلمته:** EDA، تصحيح الالتواء، Imputation، Pipeline، الانتظام، GBM، وتحليل البواقي.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "b2_house_prices")
