# -*- coding: utf-8 -*-
"""
Generator for B1 - Customer Churn Prediction.
Builds two notebooks from one shared cell list:
  - b1_churn_prediction_exercise.ipynb  (TODOs to solve)
  - b1_churn_prediction_solution.ipynb  (full working solution)
Pure standard-library (json) — no external deps needed to GENERATE.
"""
import json, os

CELLS = []  # each: ("md", text) | ("code", solution_src, stub_or_None)

def md(t): CELLS.append(("md", t))
def code(sol, stub=None): CELLS.append(("code", sol, stub))

# ──────────────────────────────────────────────────────────────────
md(r"""# 🛒 التنبؤ برحيل العملاء ونشر الموديل (Customer Churn Prediction + Deployment)
### مشروع B1 — مسار تعلم الآلة (Machine Learning Track) ⭐

---
## 🎯 المشكلة التجارية (Business Problem)
شركة تجارة إلكترونية بتخسر عملاء بصمت. **اكتساب عميل جديد بيكلّف 5–7 أضعاف** الحفاظ على عميل حالي.
المطلوب: نموذج يتنبأ **مين العملاء اللي قرّبوا يرحلوا (Churn)** قبل ما يرحلوا فعلاً، عشان فريق
التسويق يستهدفهم بعروض احتفاظ (Retention) — وده بيوفّر فلوس حقيقية.

**نوع المشكلة:** تصنيف ثنائي (Binary Classification) — هل العميل هيرحل (1) أو لا (0)؟

## 📦 ما الذي يثبته هذا المشروع في بورتفوليوك
- بناء **هدف بدون تسريب بيانات (No Data Leakage)** عبر نافذة زمنية
- خط أنابيب احترافي (`Pipeline` + `ColumnTransformer`)
- التعامل مع **البيانات غير المتوازنة (Imbalanced Data)**
- مقارنة موديلات وصولاً لـ **XGBoost**
- تقييم عميق (**ROC-AUC, PR-AUC, Threshold Tuning**) + **تفسير بـ SHAP**
- **نشر الموديل (Deployment)** كـ API بـ FastAPI (في مجلد `src/`)
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| RFM & Customer Aggregation | McKinney — *Python for Data Analysis* (ch.10 groupby) | بناء ميزات على مستوى العميل |
| **Data Leakage & زمن المراقبة** | Géron — *Hands-On ML* (ch.2) / Huyen | أخطر غلطة في ML — لازم تفهمها كويس |
| Train/Test Split & Stratify | ISLR (ch.5) | تقييم عادل للموديل |
| Pipeline & ColumnTransformer | Géron (ch.2) | منع التسريب وتنظيم المعالجة |
| Imbalanced Data (class_weight, SMOTE) | Géron (ch.3) / Thakur | بيانات الـ churn دايماً غير متوازنة |
| مقاييس التصنيف (Precision/Recall/F1/ROC-AUC/PR-AUC) | ISLR (ch.4) / Géron | accuracy لوحدها بتكدب في البيانات غير المتوازنة |
| XGBoost | Thakur — *Approaching Almost Any ML Problem* | الموديل القياسي للبيانات الجدولية |
| SHAP (تفسير الموديل) | Molnar — *Interpretable ML* | شرح "ليه" الموديل قال كده — مطلوب في الشركات |

> 🎯 **بيُستخدم في الواقع:** البنوك (هجر العملاء)، شركات الاتصالات (Telco churn)، الاشتراكات (Netflix/Spotify)،
> أي بيزنس قائم على عملاء متكررين.
""")

# ── Setup ──
md("## 0️⃣ تجهيز المكتبات")
code(
"""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
sns.set_style('whitegrid')
RANDOM_STATE = 42
print('Libraries ready ✓')"""
)

# ── Load & EDA ──
md(r"""## 1️⃣ تحميل البيانات والاستكشاف (EDA)
البيانات على مستوى **المعاملة (transaction)** — كل صف عملية شراء. هنحوّلها لمستوى **العميل** بعد شوية.""")
code(
"""df = pd.read_csv('data/ecommerce_transactions.csv')
# التواريخ بصيغ مختلطة → تحويل صريح آمن (errors='coerce' يحوّل التالف لـ NaT)
df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')
df = df.dropna(subset=['order_date']).drop_duplicates()
print('Shape after cleaning:', df.shape)
print('Date range:', df['order_date'].min().date(), '→', df['order_date'].max().date())
print('Unique customers:', df['customer_id'].nunique())
df.head()"""
)
code(
"""# نظرة على القيم المفقودة والأنواع
print(df.dtypes)
print('\\nMissing values:\\n', df.isna().sum())"""
)

md("### استكشاف بصري سريع")
code(
"""fig, axes = plt.subplots(1, 2, figsize=(14, 4))
df['category'].value_counts().plot(kind='bar', ax=axes[0], title='Orders by Category')
df.groupby(df['order_date'].dt.to_period('M').astype(str))['total_amount'].sum().plot(
    ax=axes[1], title='Monthly Revenue')
plt.tight_layout(); plt.show()"""
)

# ── Feature engineering + churn label (NO LEAKAGE) ──
md(r"""## 2️⃣ بناء الهدف بدون تسريب (Churn Label — No Leakage) ⚠️

**الفخّ الكلاسيكي:** لو عرّفنا "العميل اللي مطلبش من 90 يوم = churn"، وفي نفس الوقت استخدمنا
الـ Recency كميزة → الموديل هيغش (الـ Recency بتحدّد الإجابة مباشرة). ده **تسريب بيانات (Data Leakage)**.

**الحل الصح — نقسم الزمن:**
- `snapshot` = آخر تاريخ في البيانات
- `cutoff` = snapshot − 90 يوم
- **الميزات** تُحسب من المعاملات **قبل** الـ cutoff فقط (التاريخ المعروف)
- **الهدف (churn)** = هل العميل اختفى في آخر 90 يوم (من cutoff لـ snapshot)؟

كده الميزات بتتحسب من "الماضي" والهدف من "المستقبل" — زي الواقع بالظبط.
""")
code(
"""snapshot = df['order_date'].max()
cutoff = snapshot - pd.Timedelta(days=90)
print('Snapshot:', snapshot.date(), '| Cutoff:', cutoff.date())

hist = df[df['order_date'] < cutoff].copy()      # الماضي → للميزات
future = df[df['order_date'] >= cutoff].copy()    # المستقبل → للهدف

active_future = set(future['customer_id'].unique())
print('Customers in history:', hist['customer_id'].nunique())""",
stub="""# TODO: عرّف snapshot = آخر تاريخ، cutoff = snapshot ناقص 90 يوم
# TODO: قسّم df إلى hist (قبل cutoff) و future (بعد/يساوي cutoff)
# TODO: active_future = مجموعة customer_id الموجودين في future
snapshot = ...
cutoff = ...
hist = ...
future = ...
active_future = set(...)
print('Snapshot:', snapshot.date(), '| Cutoff:', cutoff.date())"""
)

md("### هندسة الميزات على مستوى العميل (من الماضي فقط)")
code(
"""def safe_mode(x):
    m = x.mode()
    return m.iat[0] if not m.empty else 'Unknown'   # بعض العملاء عندهم القيمة مفقودة

g = hist.groupby('customer_id')
features = pd.DataFrame({
    'recency':        (cutoff - g['order_date'].max()).dt.days,   # كام يوم من آخر طلب
    'tenure':         (cutoff - g['order_date'].min()).dt.days,   # قِدَم العميل
    'frequency':      g['order_id'].nunique(),                    # عدد الطلبات
    'monetary':       g['total_amount'].sum(),                    # إجمالي الإنفاق
    'avg_order_value':g['total_amount'].mean(),
    'total_items':    g['quantity'].sum(),
    'n_categories':   g['category'].nunique(),
    'main_country':   g['country'].agg(safe_mode),
    'main_payment':   g['payment_method'].agg(safe_mode),
}).reset_index()

# الهدف: 1 لو العميل لم يظهر في نافذة المستقبل
features['churn'] = (~features['customer_id'].isin(active_future)).astype(int)
print('Churn rate: {:.1%}'.format(features['churn'].mean()))
features.head()""",
stub="""# TODO: اعمل groupby على customer_id من hist
# TODO: احسب recency, tenure, frequency, monetary, avg_order_value, total_items, n_categories
#       + main_country و main_payment (mode)
# TODO: features['churn'] = 1 لو customer_id مش في active_future
g = hist.groupby('customer_id')
features = pd.DataFrame({
    # ... املأ الميزات هنا
})
features['churn'] = ...
print('Churn rate: {:.1%}'.format(features['churn'].mean()))"""
)

md(r"""> 📌 **لاحظ:** نسبة الـ churn مش 50/50 → بيانات **غير متوازنة**. ده هيأثر على اختيار المقياس والموديل.""")

# ── Split + preprocessing ──
md(r"""## 3️⃣ التقسيم والمعالجة (Train/Test + Pipeline)
بنستخدم `stratify` عشان نحافظ على نسبة الـ churn في التدريب والاختبار،
و`ColumnTransformer` عشان نعالج الأرقام والفئات كلٌ بطريقته **داخل** الـ Pipeline (يمنع التسريب).""")
code(
"""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

X = features.drop(columns=['customer_id', 'churn'])
y = features['churn']

num_cols = ['recency','tenure','frequency','monetary','avg_order_value','total_items','n_categories']
cat_cols = ['main_country','main_payment']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=RANDOM_STATE)

preprocess = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols),
])
print('Train:', X_train.shape, '| Test:', X_test.shape)""",
stub="""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

X = features.drop(columns=['customer_id', 'churn'])
y = features['churn']
num_cols = [...]   # TODO: أعمدة رقمية
cat_cols = [...]   # TODO: أعمدة فئوية

# TODO: train_test_split مع stratify=y
X_train, X_test, y_train, y_test = ...
# TODO: ColumnTransformer: StandardScaler للأرقام + OneHotEncoder للفئات
preprocess = ColumnTransformer([...])
print('Train:', X_train.shape, '| Test:', X_test.shape)"""
)

# ── Model comparison ──
md(r"""## 4️⃣ مقارنة الموديلات مع Cross-Validation
نقارن 3 موديلات: Logistic Regression (خط أساس) → Random Forest → **XGBoost**.
المقياس **ROC-AUC** (مناسب للبيانات غير المتوازنة، ومش بيتأثر بالـ threshold).
لاحظ `class_weight='balanced'` / `scale_pos_weight` للتعامل مع عدم التوازن.""")
code(
"""from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
models = {
    'LogReg': LogisticRegression(max_iter=1000, class_weight='balanced'),
    'RandomForest': RandomForestClassifier(n_estimators=300, class_weight='balanced',
                                           random_state=RANDOM_STATE),
    'XGBoost': XGBClassifier(n_estimators=400, learning_rate=0.05, max_depth=4,
                             scale_pos_weight=pos_weight, eval_metric='logloss',
                             random_state=RANDOM_STATE),
}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
for name, model in models.items():
    pipe = Pipeline([('prep', preprocess), ('clf', model)])
    scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring='roc_auc')
    print(f'{name:14} ROC-AUC = {scores.mean():.3f} ± {scores.std():.3f}')""",
stub="""from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

# TODO: احسب pos_weight = نسبة السالب للموجب (للتعامل مع عدم التوازن)
pos_weight = ...
models = {
    # TODO: LogReg مع class_weight='balanced'
    # TODO: RandomForest مع class_weight='balanced'
    # TODO: XGBoost مع scale_pos_weight=pos_weight
}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
for name, model in models.items():
    pipe = Pipeline([('prep', preprocess), ('clf', model)])
    scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring='roc_auc')
    print(f'{name:14} ROC-AUC = {scores.mean():.3f} ± {scores.std():.3f}')"""
)

# ── Final model + evaluation ──
md(r"""## 5️⃣ تدريب أفضل موديل وتقييمه بعمق
نختار XGBoost، ندرّبه على كامل التدريب، ونقيّمه على الاختبار بـ:
Confusion Matrix · Classification Report · ROC Curve · Precision-Recall Curve.""")
code(
"""from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, average_precision_score,
                             RocCurveDisplay, PrecisionRecallDisplay)

best = Pipeline([('prep', preprocess), ('clf', models['XGBoost'])])
best.fit(X_train, y_train)
proba = best.predict_proba(X_test)[:, 1]
pred = (proba >= 0.5).astype(int)

print('ROC-AUC :', round(roc_auc_score(y_test, proba), 3))
print('PR-AUC  :', round(average_precision_score(y_test, proba), 3))
print('\\n', classification_report(y_test, pred))

fig, axes = plt.subplots(1, 3, figsize=(16, 4))
sns.heatmap(confusion_matrix(y_test, pred), annot=True, fmt='d', cmap='Blues', ax=axes[0])
axes[0].set_title('Confusion Matrix'); axes[0].set_xlabel('Predicted'); axes[0].set_ylabel('Actual')
RocCurveDisplay.from_predictions(y_test, proba, ax=axes[1]); axes[1].set_title('ROC Curve')
PrecisionRecallDisplay.from_predictions(y_test, proba, ax=axes[2]); axes[2].set_title('PR Curve')
plt.tight_layout(); plt.show()""",
stub="""from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, average_precision_score,
                             RocCurveDisplay, PrecisionRecallDisplay)

# TODO: ابنِ Pipeline بأفضل موديل (XGBoost) ودرّبه على X_train, y_train
best = ...
best.fit(X_train, y_train)
# TODO: احسب الاحتمالات proba والتنبؤ pred عند threshold=0.5
proba = ...
pred = ...
print('ROC-AUC :', round(roc_auc_score(y_test, proba), 3))
print('PR-AUC  :', round(average_precision_score(y_test, proba), 3))
print(classification_report(y_test, pred))
# TODO: ارسم Confusion Matrix + ROC + PR curves"""
)

md(r"""## 6️⃣ ضبط عتبة القرار (Threshold Tuning) 🎯
الـ 0.5 مش دايماً الأفضل. في الـ churn، **فقدان عميل (False Negative) أغلى** من إزعاج عميل بعرض (False Positive).
نختار العتبة اللي بتعظّم الـ F1 (أو حسب تكلفة البيزنس).""")
code(
"""from sklearn.metrics import precision_recall_curve, f1_score

prec, rec, thr = precision_recall_curve(y_test, proba)
f1s = 2 * prec[:-1] * rec[:-1] / (prec[:-1] + rec[:-1] + 1e-9)
best_thr = thr[np.argmax(f1s)]
print(f'Best threshold = {best_thr:.2f} | F1 @0.5 = {f1_score(y_test, pred):.3f}'
      f' | F1 @best = {f1_score(y_test, (proba>=best_thr).astype(int)):.3f}')""",
stub="""from sklearn.metrics import precision_recall_curve, f1_score
# TODO: استخدم precision_recall_curve، احسب F1 لكل عتبة، اختر العتبة الأعلى F1
prec, rec, thr = precision_recall_curve(y_test, proba)
f1s = ...
best_thr = ...
print('Best threshold =', round(best_thr, 2))"""
)

md(r"""## 7️⃣ تفسير الموديل بـ SHAP (Interpretability) 🔍
SHAP بيقولنا **كل ميزة ساهمت بكام** في القرار — ده اللي بيقنع المدير/العميل بالموديل.""")
code(
"""import shap
# نحوّل البيانات بالـ preprocessor ثم نفسّر موديل XGBoost
Xt_test = best.named_steps['prep'].transform(X_test)
feat_names = best.named_steps['prep'].get_feature_names_out()
explainer = shap.TreeExplainer(best.named_steps['clf'])
shap_values = explainer.shap_values(Xt_test)
shap.summary_plot(shap_values, Xt_test, feature_names=feat_names, show=True)""",
stub="""import shap
# TODO: حوّل X_test عبر preprocessor، استخرج أسماء الميزات
# TODO: استخدم shap.TreeExplainer على موديل XGBoost وارسم summary_plot
Xt_test = ...
feat_names = ...
explainer = ...
shap_values = ...
shap.summary_plot(shap_values, Xt_test, feature_names=feat_names)"""
)

# ── Save model ──
md(r"""## 8️⃣ حفظ الموديل للنشر (Model Serialization)
نحفظ الـ Pipeline كامل (المعالجة + الموديل) بـ joblib عشان نستخدمه في الـ API.""")
code(
"""import joblib, os
os.makedirs('src', exist_ok=True)
joblib.dump(best, 'src/churn_model.joblib')
print('Saved → src/churn_model.joblib')"""
)

md(r"""## 9️⃣ النشر (Deployment) — FastAPI
الكود الكامل للـ API في `src/app.py`. لتشغيله:
```bash
cd src
uvicorn app:app --reload
# ثم افتح http://127.0.0.1:8000/docs لتجربة الـ endpoint
```
ده بيحوّل الموديل من نوتبوك لـ **خدمة حقيقية** ممكن أي تطبيق يستدعيها — ده الجزء اللي بيفرّق في البورتفوليو.""")

md(r"""## 🔟 الخلاصة والتوصيات التجارية (Conclusion)
- **النتيجة:** XGBoost حقّق أعلى ROC-AUC، ويقدر يحدّد العملاء المعرّضين للرحيل بدقة كويسة.
- **أهم العوامل (من SHAP):** `recency` و `frequency` و `monetary` — العميل اللي بقاله مدة وقلّت طلباته أخطر.
- **التوصية:** فريق الاحتفاظ يستهدف العملاء فوق العتبة المختارة بعروض مخصّصة → توفير تكلفة اكتساب.
- **الخطوات القادمة:** إضافة ميزات سلوكية (زيارات الموقع)، تتبّع الأداء بعد النشر (Data Drift)، وإعادة التدريب دورياً.

> ✅ **اللي اتعلمته هنا:** تجنّب التسريب، Pipeline، عدم التوازن، XGBoost، تقييم عميق، SHAP، والنشر.
""")

# ──────────────────────────────────────────────────────────────────
def to_nb(cells, solution=True):
    out = []
    for idx, c in enumerate(cells):
        cid = f"cell{idx:02d}"
        if c[0] == "md":
            out.append({"cell_type": "markdown", "id": cid, "metadata": {},
                        "source": c[1].splitlines(keepends=True)})
        else:
            src = c[1] if (solution or c[2] is None) else c[2]
            out.append({"cell_type": "code", "id": cid, "metadata": {}, "execution_count": None,
                        "outputs": [], "source": src.splitlines(keepends=True)})
    return {"cells": out,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}

base = os.path.dirname(os.path.abspath(__file__))
for sol, name in [(True, "solution"), (False, "exercise")]:
    path = os.path.join(base, f"b1_churn_prediction_{name}.ipynb")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(to_nb(CELLS, sol), f, ensure_ascii=False, indent=1)
    print("wrote", path)
