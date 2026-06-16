# -*- coding: utf-8 -*-
"""A3 — تقسيم العملاء وتحليل RFM (Customer Segmentation & RFM Analysis)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "_datagen"))
from nbtools import NB

nb = NB()
DIR = os.path.dirname(__file__)
SLUG = "a3_rfm_segmentation"
PROJECT = "data_analysis/a3_rfm_segmentation"

# ── Title ──
nb.md(f"# 🛒 تقسيم العملاء وتحليل RFM\n**Customer Segmentation & RFM Analysis**")

nb.cloud_setup(PROJECT)

# ── prereqs ──
nb.md("""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| الموضوع | المصدر المقترح |
|---|---|
| RFM Analysis (Recency, Frequency, Monetary) | أي مقال تسويق رقمي + McKinney Ch.10 |
| KMeans Clustering | ISLR Ch.12 / Géron Ch.9 |
| Pandas groupby + aggregation | McKinney Ch.10 |
| Business segmentation strategies | Case studies أونلاين |

## 🎯 بيُستخدم في إيه (استخدام واقعي)
- **فرق التسويق** بتستخدم RFM عشان تقسّم العملاء (VIP / at-risk / lost) وتوجّه الحملات.
- **فرق الـ CRM** بتحدد مين يستاهل خصم ومين محتاج retention campaign.
- **الشركات الكبيرة** بتستخدم RFM + clustering لتخصيص الرسائل والعروض.""")

# ── imports ──
nb.code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['figure.dpi'] = 100""",
stub="""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['figure.dpi'] = 100""")

# ── 1. Load data ──
nb.md("## 1️⃣ تحميل البيانات واستكشافها")
nb.code("""df = pd.read_csv("data/ecommerce_transactions.csv", parse_dates=["order_date"])
print("Shape:", df.shape)
print("\\nColumns:", list(df.columns))
print("\\nDate range:", df["order_date"].min().date(), "->", df["order_date"].max().date())
print("\\nUnique customers:", df["customer_id"].nunique())
df.head()""",
stub="""# TODO: حمّل البيانات من data/ecommerce_transactions.csv
# حوّل order_date لنوع datetime
# اطبع: الشكل، الأعمدة، نطاق التواريخ، عدد العملاء الفريدين
df = pd.read_csv(_____)
print("Shape:", df.shape)""")

# ── 2. RFM calculation ──
nb.md("""## 2️⃣ حساب مقاييس RFM
| المقياس | المعنى | الحساب |
|---|---|---|
| **Recency (R)** | قد إيه العميل اشترى من قريب | عدد الأيام من آخر طلب لتاريخ التحليل |
| **Frequency (F)** | عدد مرات الشراء | عدد الطلبات الفريدة |
| **Monetary (M)** | إجمالي الإنفاق | مجموع total_amount |""")

nb.code("""analysis_date = df["order_date"].max() + pd.Timedelta(days=1)
print("Analysis date:", analysis_date.date())

rfm = df.groupby("customer_id").agg(
    recency=("order_date", lambda x: (analysis_date - x.max()).days),
    frequency=("order_id", "nunique"),
    monetary=("total_amount", "sum")
).reset_index()

rfm["monetary"] = rfm["monetary"].round(2)
print("\\nRFM table shape:", rfm.shape)
print(rfm.describe().round(1))
rfm.head(10)""",
stub="""# TODO: حدد تاريخ التحليل (يوم بعد آخر طلب)
analysis_date = df["order_date"].max() + pd.Timedelta(days=1)

# TODO: احسب RFM لكل عميل باستخدام groupby + agg
# recency = عدد الأيام من آخر طلب لتاريخ التحليل
# frequency = عدد الطلبات الفريدة (nunique)
# monetary = مجموع total_amount
rfm = df.groupby("customer_id").agg(
    recency=_____,
    frequency=_____,
    monetary=_____
).reset_index()
rfm.head()""")

# ── 3. RFM scoring ──
nb.md("""## 3️⃣ تقييم RFM (RFM Scoring)
بنقسّم كل مقياس لـ 4 مستويات (quartiles):
- **Recency**: الأقل أحسن (اشترى من قريب) → score عالي
- **Frequency**: الأكتر أحسن → score عالي
- **Monetary**: الأكتر أحسن → score عالي""")

nb.code("""rfm["r_score"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1]).astype(int)
rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
rfm["m_score"] = pd.qcut(rfm["monetary"], 4, labels=[1, 2, 3, 4]).astype(int)

rfm["rfm_score"] = rfm["r_score"] * 100 + rfm["f_score"] * 10 + rfm["m_score"]
rfm["rfm_total"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]

print("RFM score distribution:")
print(rfm[["r_score", "f_score", "m_score", "rfm_total"]].describe().round(1))
rfm.head(10)""",
stub="""# TODO: قسّم كل مقياس لـ 4 مستويات باستخدام pd.qcut
# Recency: الأقل أحسن (labels=[4,3,2,1])
# Frequency & Monetary: الأكتر أحسن (labels=[1,2,3,4])
rfm["r_score"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1]).astype(int)
rfm["f_score"] = _____
rfm["m_score"] = _____

# TODO: احسب rfm_score (مركّب) و rfm_total (مجموع)
rfm["rfm_score"] = _____
rfm["rfm_total"] = _____
rfm.head()""")

# ── 4. Customer segments ──
nb.md("""## 4️⃣ تصنيف العملاء لشرائح (Business Segments)
بنحوّل الأرقام لشرائح بيزنس مفهومة:""")

nb.code("""def assign_segment(row):
    r, f, m = row["r_score"], row["f_score"], row["m_score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 3:
        return "Loyal Customers"
    elif r >= 4 and f <= 2:
        return "New Customers"
    elif r <= 2 and f >= 3:
        return "At Risk"
    elif r <= 2 and f <= 2 and m >= 3:
        return "Big Spenders (Lost)"
    elif r <= 1 and f <= 1:
        return "Lost"
    else:
        return "Need Attention"

rfm["segment"] = rfm.apply(assign_segment, axis=1)

seg_summary = rfm.groupby("segment").agg(
    count=("customer_id", "count"),
    avg_recency=("recency", "mean"),
    avg_frequency=("frequency", "mean"),
    avg_monetary=("monetary", "mean")
).round(1).sort_values("count", ascending=False)

print("Customer Segments:")
print(seg_summary.to_string())""",
stub="""# TODO: اكتب دالة تصنيف بناءً على r_score, f_score, m_score
# Champions: r>=4 & f>=4 & m>=4
# Loyal: r>=3 & f>=3
# New Customers: r>=4 & f<=2
# At Risk: r<=2 & f>=3
# Lost: r<=1 & f<=1
# Need Attention: الباقي
def assign_segment(row):
    r, f, m = row["r_score"], row["f_score"], row["m_score"]
    # أكمل الشروط...
    pass

rfm["segment"] = rfm.apply(assign_segment, axis=1)
rfm["segment"].value_counts()""")

# ── 5. Visualizations ──
nb.md("## 5️⃣ التصوير البياني (Visualizations)")

nb.code("""fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1 — Segment distribution
seg_counts = rfm["segment"].value_counts()
colors = plt.cm.Set2(range(len(seg_counts)))
axes[0, 0].barh(seg_counts.index, seg_counts.values, color=colors)
axes[0, 0].set_title("عدد العملاء حسب الشريحة", fontsize=13)
axes[0, 0].set_xlabel("عدد العملاء")
for i, v in enumerate(seg_counts.values):
    axes[0, 0].text(v + 5, i, str(v), va="center", fontweight="bold")

# 2 — RFM distributions
for col, ax, color in zip(["recency", "frequency", "monetary"],
                           [axes[0, 1], axes[1, 0], axes[1, 1]],
                           ["#e74c3c", "#2ecc71", "#3498db"]):
    ax.hist(rfm[col], bins=30, color=color, edgecolor="white", alpha=0.8)
    ax.axvline(rfm[col].median(), color="black", linestyle="--", label=f"Median: {rfm[col].median():.0f}")
    ax.set_title(f"توزيع {col.title()}", fontsize=13)
    ax.legend()

plt.tight_layout()
plt.savefig("data/rfm_overview.png", dpi=120, bbox_inches="tight")
plt.show()
print("Saved: data/rfm_overview.png")""",
stub="""# TODO: ارسم 4 رسومات (2x2):
# 1) عدد العملاء حسب الشريحة (barh)
# 2) توزيع Recency (hist)
# 3) توزيع Frequency (hist)
# 4) توزيع Monetary (hist)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
# أكمل الرسم...
plt.tight_layout()
plt.show()""")

# ── 6. KMeans clustering ──
nb.md("""## 6️⃣ تقسيم بـ KMeans (Unsupervised Clustering)
RFM اليدوي حلو للبيزنس، بس نقدر نستخدم KMeans عشان نكتشف مجموعات بشكل تلقائي.""")

nb.code("""scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[["recency", "frequency", "monetary"]])

inertias = []
K_range = range(2, 9)
for k in K_range:
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(rfm_scaled)
    inertias.append(km.inertia_)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(K_range, inertias, "bo-", linewidth=2)
ax.set_xlabel("عدد المجموعات (k)")
ax.set_ylabel("Inertia")
ax.set_title("Elbow Method — اختيار عدد المجموعات الأمثل")
plt.tight_layout()
plt.savefig("data/elbow.png", dpi=120, bbox_inches="tight")
plt.show()""",
stub="""# TODO: طبّق StandardScaler على أعمدة recency, frequency, monetary
# ثم اعمل Elbow Method لاختيار أفضل k (من 2 لـ 8)
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[[_____]])
# أكمل الـ Elbow plot...
""")

nb.code("""K_BEST = 4
km = KMeans(n_clusters=K_BEST, n_init=10, random_state=42)
rfm["cluster"] = km.fit_predict(rfm_scaled)

cluster_summary = rfm.groupby("cluster").agg(
    count=("customer_id", "count"),
    avg_recency=("recency", "mean"),
    avg_frequency=("frequency", "mean"),
    avg_monetary=("monetary", "mean")
).round(1)
print("KMeans Clusters (k=%d):" % K_BEST)
print(cluster_summary.to_string())""",
stub="""# TODO: طبّق KMeans بـ k=4 وأضف العمود cluster للجدول
K_BEST = 4
km = KMeans(n_clusters=K_BEST, n_init=10, random_state=42)
rfm["cluster"] = _____
rfm.groupby("cluster").agg(count=("customer_id","count")).reset_index()""")

# ── 7. Cluster visualization ──
nb.md("## 7️⃣ تصوير المجموعات")

nb.code("""from sklearn.decomposition import PCA

pca = PCA(n_components=2, random_state=42)
rfm_2d = pca.fit_transform(rfm_scaled)

fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(rfm_2d[:, 0], rfm_2d[:, 1], c=rfm["cluster"],
                     cmap="Set1", alpha=0.6, s=30, edgecolor="white", linewidth=0.3)
ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.0%} variance)")
ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.0%} variance)")
ax.set_title("KMeans Clusters (PCA projection)", fontsize=14)
plt.colorbar(scatter, label="Cluster")
plt.tight_layout()
plt.savefig("data/clusters_pca.png", dpi=120, bbox_inches="tight")
plt.show()
print(f"PCA explained variance: {pca.explained_variance_ratio_.sum():.1%}")""",
stub="""# TODO: استخدم PCA لتقليل الأبعاد لـ 2 وارسم scatter plot ملوّن بالـ cluster
from sklearn.decomposition import PCA
pca = PCA(n_components=2, random_state=42)
rfm_2d = pca.fit_transform(rfm_scaled)
# أكمل الرسم...
""")

# ── 8. Recommendations ──
nb.md("""## 8️⃣ التوصيات التجارية (Business Recommendations)

| الشريحة | الاستراتيجية |
|---|---|
| **Champions** | برنامج ولاء VIP + عروض حصرية + Referral rewards |
| **Loyal Customers** | Upselling + Early access لمنتجات جديدة |
| **New Customers** | Onboarding emails + خصم على الطلب التاني |
| **At Risk** | Win-back campaign + خصم 20% + استبيان رضا |
| **Big Spenders (Lost)** | حملة شخصية مع عرض قوي — الخسارة كبيرة |
| **Lost** | Re-engagement email ثم إزالة من القوائم النشطة |
| **Need Attention** | تحليل أعمق لمعرفة السبب + عروض مخصصة |""")

nb.code("""print("=== ملخص التحليل ===")
print(f"إجمالي العملاء: {len(rfm):,}")
print(f"\\nتوزيع الشرائح:")
for seg, cnt in rfm["segment"].value_counts().items():
    pct = cnt / len(rfm) * 100
    print(f"  {seg:25s} {cnt:5d}  ({pct:.1f}%)")

champions = rfm[rfm["segment"] == "Champions"]
at_risk = rfm[rfm["segment"] == "At Risk"]
print(f"\\n💎 Champions: {len(champions)} عميل، متوسط إنفاق {champions['monetary'].mean():,.0f}")
print(f"⚠️  At Risk: {len(at_risk)} عميل — محتاجين حملة استرجاع عاجلة")
print(f"\\n📊 عدد المجموعات (KMeans): {K_BEST}")
print("\\n✅ التحليل اكتمل بنجاح!")""",
stub="""# TODO: اطبع ملخص نهائي للتحليل
# عدد العملاء، توزيع الشرائح، وتوصية أساسية
print("=== ملخص التحليل ===")
print(f"إجمالي العملاء: {len(rfm):,}")
# أكمل...
""")

# ── Write ──
nb.write(DIR, SLUG)
