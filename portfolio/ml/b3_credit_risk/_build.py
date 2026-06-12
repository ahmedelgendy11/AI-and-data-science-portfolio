# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 💳 تقييم مخاطر الائتمان وقرار الإقراض (Credit Risk — Default Prediction)
### مشروع B3 — مسار تعلم الآلة (Machine Learning Track)

---
## 🎯 المشكلة التجارية (Business Problem)
بنك بيستقبل طلبات قروض ومحتاج يقرّر: **نوافق ولا نرفض؟** الموديل بيتنبأ **احتمال تعثّر العميل (Default)**.
بس القرار مش مجرد "هيتعثّر ولا لأ" — لازم نوازن بين **خسارة قرض متعثّر** و**خسارة عميل كويس رفضناه**.

**نوع المشكلة:** تصنيف ثنائي غير متوازن + **قرار حسّاس للتكلفة (Cost-Sensitive)**.

## 📦 ما الذي يثبته المشروع (يختلف عن مشروع الـ Churn)
التعامل مع عدم التوازن · **معايرة الاحتمالات (Probability Calibration)** ·
**عتبة القرار حسب التكلفة (Cost-Based Threshold)** · منحنى الربح · مقاييس البنوك (KS, Gini).
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| التصنيف غير المتوازن (class_weight) | Géron — *Hands-On ML* (ch.3) | المتعثّرون أقلية لكنهم الأهم |
| ROC-AUC vs PR-AUC | ISLR (ch.4) / Géron | تقييم سليم مع عدم التوازن |
| **معايرة الاحتمالات (Calibration)** | Géron (ch.3) / Niculescu-Mizil | لو هتاخد قرار بفلوس، لازم الاحتمال يكون "صادق" |
| Brier Score & Calibration Curve | sklearn docs | قياس جودة معايرة الاحتمال |
| **العتبة حسب التكلفة (Cost-Sensitive)** | Provost & Fawcett — *Data Science for Business* | 0.5 مش دايماً الأمثل — التكلفة بتحدّد العتبة |
| KS statistic / Gini | أدبيات الـ credit scoring | المقاييس القياسية في البنوك |

> 🎯 **بيُستخدم في الواقع:** البنوك، شركات التمويل، بطاقات الائتمان، الإقراض الرقمي (BNPL) — قرارات بمليارات.
""")

md("## 0️⃣ المكتبات")
code("""import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
sns.set_style('whitegrid'); np.random.seed(42)
print('ready ✓')""")

md("## 1️⃣ تحميل واستكشاف البيانات (EDA)")
code("""df = pd.read_csv('data/credit_risk_data.csv')
print('Shape:', df.shape, '| Default rate: {:.1%}'.format(df['default'].mean()))
print('Missing:', df.isna().sum()[df.isna().sum()>0].to_dict())
fig, ax = plt.subplots(1,3, figsize=(15,3.5))
sns.boxplot(data=df, x='default', y='credit_score', ax=ax[0]); ax[0].set_title('Credit Score vs Default')
sns.boxplot(data=df, x='default', y='debt_to_income', ax=ax[1]); ax[1].set_title('DTI vs Default')
sns.barplot(data=df, x='num_prior_defaults', y='default', ax=ax[2]); ax[2].set_title('Prior Defaults vs Default rate')
plt.tight_layout(); plt.show()""",
stub="""df = pd.read_csv('data/credit_risk_data.csv')
# TODO: اطبع shape ومعدل التعثّر والقيم المفقودة، وارسم العلاقات
print(df['default'].mean())""")

md("## 2️⃣ المعالجة والتقسيم (Pipeline + Stratified Split)")
code("""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

X = df.drop(columns=['default','applicant_id']); y = df['default']
num = X.select_dtypes('number').columns.tolist()
cat = X.select_dtypes('object').columns.tolist()
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
pre = ColumnTransformer([
    ('num', Pipeline([('i', SimpleImputer(strategy='median')), ('s', StandardScaler())]), num),
    ('cat', Pipeline([('i', SimpleImputer(strategy='most_frequent')),
                      ('o', OneHotEncoder(handle_unknown='ignore'))]), cat)])
print('num:', num, '\\ncat:', cat)""",
stub="""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
# TODO: افصل X/y، حدّد الأعمدة الرقمية والفئوية، split stratified، ColumnTransformer
X = ...; y = ...
pre = ColumnTransformer([...])""")

md("## 3️⃣ مقارنة الموديلات (ROC-AUC + PR-AUC) مع معالجة عدم التوازن")
code("""from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
spw = (y_tr==0).sum()/(y_tr==1).sum()
models = {
 'LogReg': LogisticRegression(max_iter=1000, class_weight='balanced'),
 'RandomForest': RandomForestClassifier(n_estimators=300, class_weight='balanced', random_state=42),
 'XGBoost': XGBClassifier(n_estimators=400, learning_rate=0.05, max_depth=4,
                          scale_pos_weight=spw, eval_metric='logloss', random_state=42)}
cv = StratifiedKFold(5, shuffle=True, random_state=42)
for n,m in models.items():
    pipe = Pipeline([('p',pre),('m',m)])
    auc = cross_val_score(pipe, X_tr, y_tr, cv=cv, scoring='roc_auc').mean()
    ap  = cross_val_score(pipe, X_tr, y_tr, cv=cv, scoring='average_precision').mean()
    print(f'{n:14} ROC-AUC={auc:.3f} | PR-AUC={ap:.3f}')""",
stub="""from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
# TODO: احسب scale_pos_weight، قارن 3 موديلات بـ ROC-AUC و PR-AUC
...""")

md(r"""## 4️⃣ معايرة الاحتمالات (Probability Calibration) 🎯
موديلات زي RF/XGBoost بتطلّع احتمالات **مش مظبوطة** (لو قال 0.8 مش معناه إن 80% فعلاً بيتعثّروا).
لو هناخد قرار بفلوس، لازم الاحتمال يكون **صادق**. نقيس بـ Brier Score (الأقل أحسن) ومنحنى المعايرة.""")
code("""from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss
base = Pipeline([('p',pre),('m',models['XGBoost'])]).fit(X_tr, y_tr)
cal  = CalibratedClassifierCV(base, method='isotonic', cv=3).fit(X_tr, y_tr)
p_base = base.predict_proba(X_te)[:,1]; p_cal = cal.predict_proba(X_te)[:,1]
print(f'Brier (uncalibrated) = {brier_score_loss(y_te, p_base):.4f}')
print(f'Brier (calibrated)   = {brier_score_loss(y_te, p_cal):.4f}')
for name,p in [('uncalibrated',p_base),('calibrated',p_cal)]:
    x,yv = calibration_curve(y_te, p, n_bins=10); plt.plot(yv,x,'o-',label=name)
plt.plot([0,1],[0,1],'k--'); plt.xlabel('Predicted'); plt.ylabel('Actual'); plt.legend()
plt.title('Calibration Curve'); plt.show()""",
stub="""from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss
# TODO: درّب الموديل، ثم CalibratedClassifierCV (isotonic)، وقارن Brier + منحنى المعايرة
base = ...
cal = ...""")

md(r"""## 5️⃣ عتبة القرار حسب التكلفة (Cost-Based Threshold) 💰
**الفكرة الأهم:** قبول متعثّر (False Negative) بيخسّر البنك القرض كله. رفض عميل كويس (False Positive)
بيخسّر الأرباح المتوقّعة فقط — أرخص بكتير. فالعتبة المثلى **مش 0.5**.
نفترض: تكلفة FN = 1.0 (خسارة القرض)، تكلفة FP = 0.15 (أرباح ضائعة). نختار العتبة اللي بتقلّل التكلفة.""")
code("""COST_FN, COST_FP = 1.0, 0.15
ths = np.linspace(0.05, 0.95, 91)
costs = []
for t in ths:
    pred = (p_cal >= t).astype(int)
    fn = ((pred==0)&(y_te==1)).sum(); fp = ((pred==1)&(y_te==0)).sum()
    costs.append(fn*COST_FN + fp*COST_FP)
best_t = ths[int(np.argmin(costs))]
print(f'Optimal threshold = {best_t:.2f}  (vs default 0.50)')
plt.plot(ths, costs); plt.axvline(best_t, color='red', ls='--', label=f'optimal={best_t:.2f}')
plt.axvline(0.5, color='gray', ls=':', label='0.50'); plt.xlabel('Threshold'); plt.ylabel('Total cost')
plt.legend(); plt.title('Expected Cost vs Decision Threshold'); plt.show()""",
stub="""COST_FN, COST_FP = 1.0, 0.15
# TODO: لكل عتبة احسب التكلفة = FN*COST_FN + FP*COST_FP، واختر العتبة الأقل تكلفة
ths = np.linspace(0.05, 0.95, 91)
best_t = ...
print('Optimal threshold:', best_t)""")

md("## 6️⃣ التقييم النهائي + مقاييس البنوك (KS / Gini)")
code("""from sklearn.metrics import classification_report, roc_auc_score
from scipy.stats import ks_2samp
pred = (p_cal >= best_t).astype(int)
print(classification_report(y_te, pred, target_names=['Good','Default']))
auc = roc_auc_score(y_te, p_cal)
ks = ks_2samp(p_cal[y_te==1], p_cal[y_te==0]).statistic
print(f'ROC-AUC = {auc:.3f} | Gini = {2*auc-1:.3f} | KS = {ks:.3f}')""",
stub="""from sklearn.metrics import classification_report, roc_auc_score
from scipy.stats import ks_2samp
# TODO: قيّم عند العتبة المثلى، واحسب AUC و Gini=2*AUC-1 و KS statistic
...""")

md(r"""## 7️⃣ الخلاصة والتوصيات (Conclusion)
- **النتيجة:** XGBoost المعاير حقّق AUC/Gini كويسين، واحتمالاته صارت **صادقة** بعد المعايرة (Brier أقل).
- **العتبة المثلى أقل من 0.5** — لأن تكلفة قبول متعثّر أعلى بكتير من رفض عميل كويس، فالبنك يميل للتحفّظ.
- **مقاييس البنوك:** KS و Gini ضمن النطاق المقبول في الـ credit scoring.
- **التوصية:** اعتماد الموديل المعاير + العتبة المبنية على التكلفة، مع مراجعة بشرية للحالات الحدّية.
- **الخطوة القادمة:** تحويله لـ scorecard (نقاط)، ومراقبة الانحراف (drift) بعد النشر.

> ✅ **اللي اتعلمته:** عدم التوازن، PR-AUC، **معايرة الاحتمالات**، **العتبة حسب التكلفة**، و KS/Gini.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "b3_credit_risk")
