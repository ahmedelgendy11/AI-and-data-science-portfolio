# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# ❤️ التنبؤ بمخاطر أمراض القلب (Heart Disease Risk Classifier)
### مشروع B5 — مسار تعلم الآلة (Machine Learning Track)

---
## 🎯 المشكلة التجارية (Business Problem)
عيادة عايزة **أداة فرز (Screening)** تتنبأ باحتمال إصابة المريض بمرض قلب من فحوصاته الأساسية،
عشان توجّه الأطباء للحالات الخطيرة بدري. **قرار طبي حسّاس → التفسير (Interpretability) مهم جداً.**

**نوع المشكلة:** تصنيف ثنائي (مريض / سليم).

## 📦 ما الذي يثبته المشروع
كشف **تسريب البيانات (Data Leakage)** من ميزة مشتقة · Pipeline · مقارنة موديلات ·
تقييم (ROC-AUC) · **تفسير العوامل الطبية (Feature Importance)**.
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| التصنيف (LogReg, RF) | ISLR (ch.4) / Géron | أساس التنبؤ الثنائي |
| **Data Leakage من ميزة مشتقة** | Huyen / Géron | ميزة "مثالية" غالباً غش — لازم تكتشفها |
| ROC-AUC + Confusion Matrix | ISLR (ch.4) | تقييم مع أهمية الحالات الإيجابية |
| Feature Importance | Géron / Molnar | في الطب لازم تعرف "ليه" |

> 🎯 **بيُستخدم في الواقع:** أنظمة الدعم الطبي، فرز المرضى، التأمين الصحي، الطب الوقائي.
> ⚠️ **تنبيه أخلاقي:** أداة فرز مساعِدة فقط — مش بديل عن تشخيص الطبيب.
""")

md("## 0️⃣ المكتبات")
code("""import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
sns.set_style('whitegrid'); np.random.seed(42)
print('ready ✓')""")

md("## 1️⃣ تحميل واستكشاف البيانات (EDA)")
code("""df = pd.read_csv('data/health_risk_data.csv')
print('Shape:', df.shape, '| Disease rate: {:.1%}'.format(df['heart_disease'].mean()))
corr = df.corr(numeric_only=True)['heart_disease'].sort_values(ascending=False)
print(corr.round(2))""",
stub="""df = pd.read_csv('data/health_risk_data.csv')
# TODO: shape + معدل المرض + الارتباط مع الهدف
print(df['heart_disease'].mean())""")

md(r"""## 2️⃣ ⚠️ كشف تسريب البيانات (Data Leakage)
لاحظ إن `risk_score` ارتباطه بالهدف **عالي جداً (~0.80)**. ده مش ميزة حقيقية — ده **درجة خطورة محسوبة
من النتيجة نفسها**. لو سِبناها، الموديل هيغش وهيفشل في الواقع. **نشيلها.**""")
code("""LEAKY = ['risk_score']
X = df.drop(columns=['heart_disease', 'patient_id'] + LEAKY)
y = df['heart_disease']
print('Dropped leaky feature:', LEAKY)
print('Features used:', list(X.columns))""",
stub="""# TODO: شيل العمود المسرّب risk_score + المعرّفات، وحدّد X و y
LEAKY = ['risk_score']
X = ...
y = ...""")

md("## 3️⃣ المعالجة والتقسيم (Pipeline)")
code("""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
num = X.select_dtypes('number').columns.tolist()
cat = X.select_dtypes('object').columns.tolist()
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
pre = ColumnTransformer([
    ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('sc', StandardScaler())]), num),
    ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')),
                      ('oh', OneHotEncoder(handle_unknown='ignore'))]), cat)])
print('num:', num, '| cat:', cat)""",
stub="""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
# TODO: حدّد الأعمدة، split stratified، ColumnTransformer
...""")

md("## 4️⃣ مقارنة الموديلات (Cross-Validation, ROC-AUC)")
code("""from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
cv = StratifiedKFold(5, shuffle=True, random_state=42)
models = {
    'LogReg': LogisticRegression(max_iter=1000),
    'RandomForest': RandomForestClassifier(n_estimators=300, random_state=42),
    'XGBoost': XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=4,
                             eval_metric='logloss', random_state=42)}
for n, m in models.items():
    auc = cross_val_score(Pipeline([('p',pre),('m',m)]), X_tr, y_tr, cv=cv, scoring='roc_auc').mean()
    print(f'{n:14} ROC-AUC = {auc:.3f}')""",
stub="""from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
# TODO: قارن 3 موديلات بـ 5-fold CV على ROC-AUC
...""")

md("## 5️⃣ التقييم النهائي")
code("""from sklearn.metrics import classification_report, confusion_matrix, RocCurveDisplay
best = Pipeline([('p',pre),('m',models['LogReg'])]).fit(X_tr, y_tr)
proba = best.predict_proba(X_te)[:,1]; pred = (proba>=0.5).astype(int)
print(classification_report(y_te, pred, target_names=['Healthy','Disease']))
fig, ax = plt.subplots(1,2, figsize=(12,4))
sns.heatmap(confusion_matrix(y_te, pred), annot=True, fmt='d', cmap='Reds', ax=ax[0],
            xticklabels=['Healthy','Disease'], yticklabels=['Healthy','Disease'])
ax[0].set_title('Confusion Matrix')
RocCurveDisplay.from_predictions(y_te, proba, ax=ax[1]); ax[1].set_title('ROC Curve')
plt.tight_layout(); plt.show()""",
stub="""from sklearn.metrics import classification_report, confusion_matrix, RocCurveDisplay
# TODO: درّب أفضل موديل، قيّم، وارسم confusion matrix + ROC
best = ...""")

md("## 6️⃣ تفسير العوامل الطبية (Feature Importance)")
code("""rf = Pipeline([('p',pre),('m',models['RandomForest'])]).fit(X_tr, y_tr)
names = rf.named_steps['p'].get_feature_names_out()
imp = pd.Series(rf.named_steps['m'].feature_importances_, index=names).sort_values().tail(10)
imp.plot(kind='barh', figsize=(7,4), title='Top risk factors'); plt.tight_layout(); plt.show()""")

md(r"""## 7️⃣ الخلاصة والتوصيات (Conclusion)
- **درس التسريب:** شيلنا `risk_score` لأنها مشتقة من النتيجة — لو سِبناها كانت الدقة "وهمية".
- **النتيجة:** بعد إزالة التسريب، الموديل حقّق ROC-AUC واقعي وكويس بالعوامل الطبية الحقيقية.
- **أهم العوامل:** السن، الكوليسترول، ضغط الدم الانقباضي — متوافقة مع الطب المعروف ✓ (ثقة في الموديل).
- **التوصية:** استخدامه كأداة فرز مساعِدة توجّه الانتباه للحالات عالية الخطورة، مع تأكيد الطبيب دائماً.
- **الخطوة القادمة:** معايرة الاحتمالات + تحليل بـ SHAP لكل مريض على حدة.

> ✅ **اللي اتعلمته:** كشف الـ leakage من ميزة مشتقة، Pipeline، مقارنة موديلات، وتفسير طبي.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "b5_heart_disease")
