# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 🔬 خط أنابيب ML كامل مع تتبع التجارب (Full ML Pipeline + Experiment Tracking)
### مشروع C1 — مسار علم البيانات (Data Science Track)

---
## 🎯 المشكلة التجارية (Business Problem)
فريق بيبني موديل للتنبؤ بأسعار العقارات، وبيجرّب موديلات وإعدادات كتير. المشكلة:
**"أنهي تجربة كانت الأحسن؟ وبأي إعدادات؟"** — لو مش متسجّل، النتائج بتضيع وما ينفعش تكرّرها.

**الحل:** خط أنابيب (Pipeline) منظّم + **تتبّع التجارب (Experiment Tracking) بـ MLflow** —
كل تجربة بتتسجّل: الإعدادات (params) + المقاييس (metrics) + الموديل نفسه (artifact).

## 📦 ما الذي يثبته المشروع
**Pipeline** (معالجة + موديل) · **Cross-Validation** · **MLflow** (params/metrics/model logging) ·
المقارنة واختيار الأفضل (Model Selection) · استرجاع الموديل المسجّل وتقييمه.
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| Pipeline + ColumnTransformer | Géron — *Hands-On ML* (ch.2) | يمنع تسريب المعالجة ويبسّط الكود |
| Cross-Validation | ISLR (ch.5) / Géron | تقدير أمين لأداء الموديل |
| **تتبّع التجارب (MLflow)** | Huyen — *Designing ML Systems* (ch.6) | تسجيل/مقارنة/تكرار التجارب |
| Model Registry | وثائق MLflow | حفظ الموديل كـ artifact واسترجاعه |
| مقاييس الانحدار (RMSE/MAE/R²) | ISLR (ch.3) | تقييم دقّة التنبؤ |

> 🎯 **بيُستخدم في الواقع:** أي فريق ML جاد بيستخدم تتبّع تجارب (MLflow / Weights & Biases) —
> ده جوهر **MLOps**: تكرارية، مقارنة، وحَوكمة الموديلات.
""")

md("## 0️⃣ المكتبات والبيانات")
code("""import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
import mlflow, mlflow.sklearn
sns.set_style('whitegrid'); np.random.seed(42)

df = pd.read_csv('data/house_prices_data.csv')
print('Shape:', df.shape, '| MLflow version:', mlflow.__version__)
df.head(3)""",
stub="""import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
import mlflow, mlflow.sklearn
df = pd.read_csv('data/house_prices_data.csv')
print(df.shape)""")

md(r"""## 1️⃣ استكشاف سريع + هندسة ميزة (Feature Engineering)
نضيف **عمر المنزل (house_age)** بدل سنة البناء — أكثر دلالة للموديل.""")
code("""df['house_age'] = 2025 - df['year_built']
target = 'sale_price'
print(df[['square_footage','bedrooms','bathrooms','house_age','garage_spaces',target]].describe().round(0).T[['mean','min','max']])
print('\\nالحي (neighborhood):', df['neighborhood'].unique())""",
stub="""# TODO: أضف house_age = 2025 - year_built، وحدّد عمود الهدف target='sale_price'
df['house_age'] = ...
target = 'sale_price'
print(df.describe())""")

md("## 2️⃣ التقسيم وخط المعالجة (Train/Test Split + Preprocessing Pipeline)")
code("""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

X = df.drop(columns=['house_id', target, 'year_built'])
y = df[target]
num = X.select_dtypes('number').columns.tolist()
cat = X.select_dtypes('object').columns.tolist()
print('قيم ناقصة في التدريب:', int(X[num].isna().sum().sum()), '→ نعالجها بالـ median داخل الـ Pipeline')

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
pre = ColumnTransformer([
    ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('sc', StandardScaler())]), num),
    ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')),
                      ('oh', OneHotEncoder(handle_unknown='ignore'))]), cat)])
print('num:', num, '| cat:', cat, '| train/test:', X_tr.shape[0], '/', X_te.shape[0])""",
stub="""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
# TODO: حدّد X و y، الأعمدة الرقمية/الفئوية، split، و ColumnTransformer
#       (انتبه: square_footage فيها قيم ناقصة → استخدم SimpleImputer داخل الـ Pipeline)
...""")

md(r"""## 3️⃣ إعداد MLflow (تتبّع محلي)
نخلّي MLflow يسجّل في قاعدة بيانات محلية `sqlite:///mlflow.db` (مش محتاج سيرفر)، ونعمل
**تجربة (experiment)** باسم محدّد. *(ملاحظة: من MLflow 3 الـ file-store اتحوّل لوضع صيانة،
فالموصى به backend قاعدة بيانات زي sqlite.)*""")
code("""mlflow.set_tracking_uri('sqlite:///mlflow.db')
mlflow.set_experiment('house-prices-regression')
print('Tracking URI:', mlflow.get_tracking_uri())""",
stub="""# TODO: عيّن tracking_uri محلي (sqlite:///mlflow.db) و set_experiment باسم
mlflow.set_tracking_uri('sqlite:///mlflow.db')
mlflow.set_experiment('house-prices-regression')""")

md(r"""## 4️⃣ تدريب ومقارنة الموديلات — كل تجربة في MLflow Run
لكل موديل: نحسب **CV-RMSE**، ندرّب، نقيّم على الاختبار (RMSE/MAE/R²)، ونسجّل **الإعدادات + المقاييس +
الموديل** في run منفصل.""")
code("""from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

models = {
    'Ridge':        Ridge(alpha=1.0),
    'RandomForest': RandomForestRegressor(n_estimators=200, random_state=42),
    'XGBoost':      XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=4, random_state=42),
}

for name, model in models.items():
    with mlflow.start_run(run_name=name):
        pipe = Pipeline([('pre', pre), ('model', model)])
        cv_rmse = -cross_val_score(pipe, X_tr, y_tr, cv=5,
                                   scoring='neg_root_mean_squared_error').mean()
        pipe.fit(X_tr, y_tr)
        pred = pipe.predict(X_te)
        rmse, mae, r2 = root_mean_squared_error(y_te, pred), mean_absolute_error(y_te, pred), r2_score(y_te, pred)

        mlflow.log_param('model_type', name)
        mlflow.log_params(model.get_params())
        mlflow.log_metrics({'cv_rmse': cv_rmse, 'test_rmse': rmse, 'test_mae': mae, 'test_r2': r2})
        mlflow.sklearn.log_model(pipe, name='model', input_example=X_te.head(2))
        print(f'{name:14} CV-RMSE={cv_rmse:,.0f} | test-RMSE={rmse:,.0f} | R²={r2:.3f}')""",
stub="""from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
models = {'Ridge': Ridge(), 'RandomForest': RandomForestRegressor(random_state=42), 'XGBoost': XGBRegressor(random_state=42)}
# TODO: لكل موديل افتح mlflow run، احسب CV-RMSE، درّب، قيّم، وسجّل params+metrics+model
for name, model in models.items():
    with mlflow.start_run(run_name=name):
        ...""")

md(r"""## 5️⃣ مقارنة التجارب واختيار الأفضل (Query Runs)
نسأل MLflow عن كل الـ runs مرتّبة بـ test-RMSE — أقل قيمة = أفضل موديل.""")
code("""runs = mlflow.search_runs(order_by=['metrics.test_rmse ASC'])
cols = ['tags.mlflow.runName', 'metrics.cv_rmse', 'metrics.test_rmse', 'metrics.test_r2']
print(runs[cols].round(3).to_string(index=False))

best = runs.iloc[0]
best_id = best['run_id']
print(f"\\n🏆 الأفضل: {best['tags.mlflow.runName']} | test-RMSE={best['metrics.test_rmse']:,.0f} | run_id={best_id[:8]}")""",
stub="""# TODO: استخدم mlflow.search_runs مرتّبة بـ test_rmse، واطبع المقارنة، وحدّد أفضل run
runs = mlflow.search_runs(order_by=['metrics.test_rmse ASC'])
best_id = runs.iloc[0]['run_id']
print(runs)""")

md(r"""## 6️⃣ استرجاع الموديل المسجّل والتقييم (Load + Residuals)
نحمّل الموديل الأفضل من MLflow (زي ما هيحصل في الإنتاج) ونرسم البواقي (Residuals).""")
code("""loaded = mlflow.sklearn.load_model(f'runs:/{best_id}/model')
pred = loaded.predict(X_te)
resid = y_te - pred

fig, ax = plt.subplots(1, 2, figsize=(13, 4))
ax[0].scatter(pred, y_te, alpha=0.4);
lims = [y_te.min(), y_te.max()]; ax[0].plot(lims, lims, 'r--')
ax[0].set_xlabel('Predicted'); ax[0].set_ylabel('Actual'); ax[0].set_title('Predicted vs Actual')
ax[1].scatter(pred, resid, alpha=0.4); ax[1].axhline(0, color='r', ls='--')
ax[1].set_xlabel('Predicted'); ax[1].set_ylabel('Residual'); ax[1].set_title('Residuals')
plt.tight_layout(); plt.show()
print('الموديل اتحمّل من MLflow registry بنجاح ✓')""",
stub="""# TODO: حمّل أفضل موديل من mlflow (runs:/{best_id}/model)، تنبّأ، وارسم البواقي
loaded = mlflow.sklearn.load_model(f'runs:/{best_id}/model')
...""")

md(r"""## 7️⃣ الخلاصة والتوصيات (Conclusion)
- **الـ Pipeline** ضمن إن المعالجة (scaling/encoding) تتعلّم من بيانات التدريب بس — لا تسريب.
- **MLflow** سجّل كل تجربة (params + metrics + model) → نقدر نقارن ونكرّر ونرجع لأي تجربة.
- **اختيار الموديل** اتعمل بمقياس موضوعي (test-RMSE) على الـ runs المسجّلة، مش بالحدس.
- **الاسترجاع:** حمّلنا الموديل الأفضل من الـ registry — نفس آلية النشر في الإنتاج.

> 🖥️ **شوف لوحة MLflow:**
> ```bash
> mlflow ui --backend-store-uri sqlite:///mlflow.db      # ثم افتح http://localhost:5000
> ```
> ✅ **اللي اتعلمته:** Pipeline، Cross-Validation، تتبّع التجارب بـ MLflow، المقارنة، واسترجاع الموديل.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "c1_mlflow_pipeline")
