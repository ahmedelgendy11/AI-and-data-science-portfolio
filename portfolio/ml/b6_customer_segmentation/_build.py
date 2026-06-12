# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 👥 تقسيم العملاء غير الموجّه (Customer Segmentation — Clustering)
### مشروع B6 — مسار تعلم الآلة (Machine Learning Track)

---
## 🎯 المشكلة التجارية (Business Problem)
فريق التسويق عايز يقسّم العملاء لـ **مجموعات متشابهة (Segments)** عشان يعمل لكل مجموعة حملة مخصّصة
بدل رسالة واحدة للكل. مفيش "إجابة صح" مسبقة → ده **تعلّم غير موجّه (Unsupervised)**.

**نوع المشكلة:** تجميع (Clustering) — اكتشاف بنية مخفية في البيانات بدون labels.

## 📦 ما الذي يثبته المشروع
**K-Means** + اختيار k (Elbow + **Silhouette**) · **DBSCAN** · **PCA** للتصوير ·
تحليل الشخصيات (Cluster Profiling) وتحويلها لتوصيات تسويقية.
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| التعلّم غير الموجّه | ISLR (ch.12) / Géron (ch.9) | لا توجد labels — نكتشف البنية |
| **K-Means + Inertia** | Géron (ch.9) | أشهر خوارزمية تجميع |
| اختيار k (Elbow + **Silhouette**) | Géron (ch.9) | كام مجموعة؟ السؤال الأصعب |
| التحجيم (Scaling) قبل التجميع | Géron (ch.9) | المسافات تتأثر بوحدات القياس |
| **DBSCAN** | Géron (ch.9) | تجميع حسب الكثافة + كشف الشواذ |
| **PCA** للتصوير | ISLR (ch.12) | رسم البيانات متعددة الأبعاد في 2D |

> 🎯 **بيُستخدم في الواقع:** تقسيم العملاء، التسويق المستهدف، أنظمة التوصية، ضغط الصور، اكتشاف المجتمعات.
""")

md("## 0️⃣ المكتبات")
code("""import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
sns.set_style('whitegrid'); np.random.seed(42)
print('ready ✓')""")

md("## 1️⃣ تحميل واستكشاف البيانات (EDA)")
code("""df = pd.read_csv('data/customer_segmentation_data.csv')
print('Shape:', df.shape)
features = ['age','annual_income_k','spending_score_1_100']
sns.pairplot(df[features]); plt.suptitle('Feature relationships', y=1.02); plt.show()
df[features].describe().T[['mean','std','min','max']]""",
stub="""df = pd.read_csv('data/customer_segmentation_data.csv')
features = ['age','annual_income_k','spending_score_1_100']
# TODO: استكشف الميزات (pairplot / describe)
print(df.shape)""")

md("## 2️⃣ التحجيم (Scaling)")
code("""from sklearn.preprocessing import StandardScaler
X = StandardScaler().fit_transform(df[features])
print('Scaled shape:', X.shape)""",
stub="""from sklearn.preprocessing import StandardScaler
# TODO: حجّم الميزات بـ StandardScaler
X = ...""")

md(r"""## 3️⃣ اختيار عدد المجموعات (Elbow + Silhouette)
- **Elbow:** نرسم الـ Inertia لكل k ونلاقي "الكوع".
- **Silhouette:** أعلى قيمة = أوضح فصل بين المجموعات.""")
code("""from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
inertias, sils = [], []
Ks = range(2, 11)
for k in Ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    inertias.append(km.inertia_); sils.append(silhouette_score(X, km.labels_))
fig, ax = plt.subplots(1,2, figsize=(13,4))
ax[0].plot(list(Ks), inertias, 'o-'); ax[0].set_title('Elbow (Inertia)'); ax[0].set_xlabel('k')
ax[1].plot(list(Ks), sils, 'o-', color='green'); ax[1].set_title('Silhouette score'); ax[1].set_xlabel('k')
plt.show()
best_k = list(Ks)[int(np.argmax(sils))]
print('Best k by silhouette =', best_k)""",
stub="""from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
# TODO: لكل k من 2 لـ 10 احسب inertia و silhouette، وارسمهم، واختر أفضل k
...
best_k = ...""")

md("## 4️⃣ تدريب K-Means وتحليل الشخصيات (Cluster Profiling)")
code("""km = KMeans(n_clusters=best_k, n_init=10, random_state=42).fit(X)
df['cluster'] = km.labels_
profile = df.groupby('cluster')[features].mean().round(1)
profile['size'] = df['cluster'].value_counts().sort_index()
print(profile)""",
stub="""# TODO: درّب KMeans بأفضل k، أضف عمود cluster، واحسب متوسط الميزات لكل مجموعة
km = ...
profile = ...""")

md(r"""## 5️⃣ المقارنة بـ DBSCAN (تجميع بالكثافة)
DBSCAN مش محتاج تحدّد عدد المجموعات، وبيكتشف الشواذ (نقطة فئتها -1).""")
code("""from sklearn.cluster import DBSCAN
db = DBSCAN(eps=0.4, min_samples=8).fit(X)
n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
print(f'DBSCAN found {n_clusters} clusters + {(db.labels_==-1).sum()} outliers')""",
stub="""from sklearn.cluster import DBSCAN
# TODO: طبّق DBSCAN واطبع عدد المجموعات وعدد الشواذ (-1)
db = ...""")

md("## 6️⃣ تصوير المجموعات بـ PCA (2D)")
code("""from sklearn.decomposition import PCA
emb = PCA(n_components=2).fit_transform(X)
plt.figure(figsize=(8,6))
sns.scatterplot(x=emb[:,0], y=emb[:,1], hue=df['cluster'], palette='tab10', s=30)
plt.title('Customer Segments (PCA projection)'); plt.xlabel('PC1'); plt.ylabel('PC2'); plt.show()""")

md(r"""## 7️⃣ الخلاصة والتوصيات (Conclusion)
- **النتيجة:** قسّمنا العملاء لـ مجموعات واضحة (k المختار بالـ Silhouette)، وكل مجموعة لها بروفايل مميّز.
- **أمثلة شخصيات (حسب البروفايل):** "دخل عالي/إنفاق عالي" = عملاء VIP · "دخل عالي/إنفاق منخفض" = فرصة ضائعة · "دخل منخفض/إنفاق عالي" = حسّاسون للعروض.
- **DBSCAN:** أعطى رؤية مختلفة + رصد شواذ ممكن يكونوا حالات خاصة.
- **التوصية:** حملة تسويقية مخصّصة لكل مجموعة (عروض VIP، تحفيز الإنفاق، برامج ولاء).
- **الخطوة القادمة:** إضافة ميزات سلوكية (تكرار الشراء)، وربط المجموعات بمعدّل التحويل.

> ✅ **اللي اتعلمته:** Scaling، K-Means، Elbow/Silhouette، DBSCAN، PCA، وتحليل الشخصيات.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "b6_customer_segmentation")
