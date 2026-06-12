# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 🕵️ كشف الاحتيال في المعاملات (Fraud Detection — Anomaly + Imbalanced ML)
### مشروع B4 — مسار تعلم الآلة (Machine Learning Track)

---
## 🎯 المشكلة التجارية (Business Problem)
شركة مدفوعات عايزة **تكتشف المعاملات الاحتيالية** لحظياً. التحدي: الاحتيال **نادر جداً** (أقل من 4%)،
وفريق المراجعة يقدر يراجع **عدد محدود** من المعاملات يومياً — فلازم نرتّبهم بالأخطر.

**نوع المشكلة:** تصنيف ثنائي **غير متوازن بشدة** + كشف شذوذ (Anomaly Detection).

## 📦 ما الذي يثبته المشروع (يختلف عن مخاطر الائتمان)
**كشف الشذوذ غير الموجّه (Isolation Forest)** · التعامل مع عدم التوازن الشديد ·
**PR-AUC** بدل ROC-AUC · **الدقة عند حدّ المراجعة (Precision@k)** · مقارنة موجّه vs غير موجّه.
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| عدم التوازن الشديد (Rare events) | Géron — *Hands-On ML* (ch.3) | الاحتيال < 4% — accuracy عديمة الفائدة |
| **كشف الشذوذ (Isolation Forest)** | Géron (ch.9) / Liu et al. | اكتشاف الغريب **بدون labels** |
| **PR-AUC vs ROC-AUC** | Davis & Goadrich | PR-AUC أصدق مع الأحداث النادرة |
| **Precision@k** | أدبيات استرجاع المعلومات | "لو راجعنا أعلى 100، كام منهم احتيال؟" — مقياس عملي |
| scale_pos_weight / class_weight | Thakur / Géron | موازنة الموديل الموجّه |

> 🎯 **بيُستخدم في الواقع:** البنوك، بطاقات الائتمان، التأمين، كشف الحسابات الوهمية، أمن الشبكات.
""")

md("## 0️⃣ المكتبات")
code("""import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
sns.set_style('whitegrid'); np.random.seed(42)
print('ready ✓')""")

md("## 1️⃣ تحميل واستكشاف البيانات (EDA)")
code("""df = pd.read_csv('data/fraud_data.csv')
print('Shape:', df.shape, '| Fraud rate: {:.2%}'.format(df['is_fraud'].mean()))
fig, ax = plt.subplots(1,2, figsize=(13,4))
sns.boxplot(data=df, x='is_fraud', y='amount_ratio', ax=ax[0]); ax[0].set_title('Amount ratio vs Fraud'); ax[0].set_ylim(0,15)
sns.barplot(data=df, x='is_foreign', y='is_fraud', ax=ax[1]); ax[1].set_title('Fraud rate by foreign flag')
plt.tight_layout(); plt.show()""",
stub="""df = pd.read_csv('data/fraud_data.csv')
# TODO: اطبع shape ومعدل الاحتيال، وارسم العلاقات
print(df['is_fraud'].mean())""")

md(r"""> 📌 الاحتيال نادر جداً → موديل يقول "كله سليم" هيحقّق دقة 96%+ لكنه **عديم الفائدة**. لذلك نستخدم PR-AUC و Precision@k.""")

md("## 2️⃣ المعالجة والتقسيم")
code("""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
X = df.drop(columns=['is_fraud','transaction_id']); y = df['is_fraud']
num = X.select_dtypes('number').columns.tolist(); cat = ['merchant_category']
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
pre = ColumnTransformer([('num', StandardScaler(), num),
                         ('cat', OneHotEncoder(handle_unknown='ignore'), cat)])
Xtr = pre.fit_transform(X_tr); Xte = pre.transform(X_te)
print('Train fraud:', y_tr.sum(), '| Test fraud:', y_te.sum())""",
stub="""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
# TODO: افصل X/y، split stratified، ColumnTransformer (scale + onehot)، حوّل البيانات
...""")

md(r"""## 3️⃣ كشف الشذوذ غير الموجّه (Isolation Forest) 🌲
**بدون استخدام الـ labels** — الموديل بيتعلّم "الطبيعي" ويعزل الغريب. نقيّم بعدين مقابل الحقيقة.""")
code("""from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score, roc_auc_score
iso = IsolationForest(contamination=0.04, random_state=42).fit(Xtr)   # لا نمرّر y!
anomaly_score = -iso.score_samples(Xte)        # أعلى = أكثر شذوذاً
print(f'IsolationForest  PR-AUC = {average_precision_score(y_te, anomaly_score):.3f}'
      f' | ROC-AUC = {roc_auc_score(y_te, anomaly_score):.3f}')""",
stub="""from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score, roc_auc_score
# TODO: درّب IsolationForest بدون y، احسب anomaly_score = -score_samples، وقيّمه بـ PR-AUC
iso = ...
anomaly_score = ...""")

md("## 4️⃣ النماذج الموجّهة (Supervised) — مقارنة بالـ PR-AUC")
code("""from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
spw = (y_tr==0).sum()/(y_tr==1).sum()
results = {}
for name, m in {
    'LogReg': LogisticRegression(max_iter=1000, class_weight='balanced'),
    'XGBoost': XGBClassifier(n_estimators=400, learning_rate=0.05, max_depth=4,
                             scale_pos_weight=spw, eval_metric='aucpr', random_state=42),
}.items():
    m.fit(Xtr, y_tr)
    proba = m.predict_proba(Xte)[:,1]
    results[name] = proba
    print(f'{name:10} PR-AUC = {average_precision_score(y_te, proba):.3f}')""",
stub="""from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
# TODO: احسب scale_pos_weight، درّب LogReg + XGBoost، قارن بالـ PR-AUC
...""")

md(r"""## 5️⃣ الدقة عند حدّ المراجعة (Precision@k) 💼
فريق المراجعة يقدر يراجع **أعلى k معاملة مشبوهة يومياً**. السؤال العملي: **كام منهم احتيال فعلاً؟**""")
code("""best = results['XGBoost']
order = np.argsort(best)[::-1]
y_sorted = y_te.values[order]
for k in [50, 100, 200, 500]:
    prec = y_sorted[:k].mean()
    recall = y_sorted[:k].sum() / y_te.sum()
    print(f'Top {k:4}: Precision@k = {prec:.1%} | يمسك {recall:.1%} من إجمالي الاحتيال')""",
stub="""best = results['XGBoost']
# TODO: رتّب المعاملات بالاحتمال تنازلياً، واحسب Precision@k و recall لأعلى k
...""")

md("## 6️⃣ منحنى Precision-Recall (المقياس الصح للأحداث النادرة)")
code("""from sklearn.metrics import PrecisionRecallDisplay
fig, ax = plt.subplots(figsize=(7,5))
PrecisionRecallDisplay.from_predictions(y_te, results['XGBoost'], name='XGBoost', ax=ax)
PrecisionRecallDisplay.from_predictions(y_te, results['LogReg'], name='LogReg', ax=ax)
PrecisionRecallDisplay.from_predictions(y_te, anomaly_score, name='IsolationForest', ax=ax)
ax.set_title('Precision-Recall Curves'); plt.show()""")

md(r"""## 7️⃣ الخلاصة والتوصيات (Conclusion)
- **الموجّه أفضل من غير الموجّه:** XGBoost حقّق أعلى PR-AUC، لكن Isolation Forest مفيد لما **مفيش labels**.
- **Precision@k:** مراجعة أعلى ~100 معاملة بتمسك نسبة كبيرة من الاحتيال بأقل جهد — ده اللي يهمّ العمليات.
- **PR-AUC مش ROC-AUC:** مع 4% احتيال، ROC-AUC بيبالغ في التفاؤل؛ PR-AUC أصدق.
- **التوصية:** نظام هجين — XGBoost للترتيب اليومي + Isolation Forest لرصد أنماط جديدة، مع حدّ مراجعة حسب طاقة الفريق.
- **الخطوة القادمة:** ميزات زمنية (سرعة المعاملات)، وتحديث الموديل باستمرار لأن أنماط الاحتيال بتتغيّر.

> ✅ **اللي اتعلمته:** عدم التوازن الشديد، Isolation Forest، PR-AUC، و Precision@k.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "b4_fraud_detection")
