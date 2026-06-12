# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 🛍️ لوحة أداء مبيعات التجارة الإلكترونية (Sales Performance Dashboard)
### مشروع A1 — مسار تحليل البيانات (Data Analysis Track)

---
## 🎯 المشكلة التجارية (Business Problem)
إدارة متجر إلكتروني عايزة تعرف **صحّة البيزنس في لمحة**: إيرادات، عدد الطلبات، متوسط قيمة الطلب،
أكتر منتجات/دول بتبيع، والاتجاه الشهري — عشان تاخد قرارات (مخزون، تسويق، توسّع).

**نوع المشكلة:** تحليل وصفي (Descriptive Analytics) + بناء **مؤشرات أداء (KPIs)** ولوحة متابعة.

## 📦 ما الذي يثبته المشروع
**SQL** (تجميع واستعلام) · **Pandas** · حساب **KPIs** · التصوير (Visualization) ·
ولوحة تفاعلية للإنتاج بـ **Streamlit + Plotly** (في `src/app.py`).
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| SQL (GROUP BY, تجميع) | Kleppmann / أي مرجع SQL · McKinney (ch.) | لغة استخراج المؤشرات من البيانات |
| Pandas للتجميع | McKinney — *Python for Data Analysis* (ch.10) | groupby/pivot كبديل/مكمّل لـ SQL |
| **مؤشرات الأداء (KPIs)** | أي مرجع Business Analytics | Revenue · AOV · Repeat-rate · إلخ |
| التصوير الفعّال | Knaflic — *Storytelling with Data* | اللوحة لازم توصّل القصة بسرعة |
| لوحات تفاعلية | وثائق Streamlit / Plotly | نشر اللوحة لغير التقنيين |

> 🎯 **بيُستخدم في الواقع:** لوحات الإدارة (Executive dashboards)، تقارير المبيعات الأسبوعية، أدوات BI.
> 🛠️ **هنا:** نستخرج المؤشرات بـ **SQL حقيقي** (sqlite داخل الذاكرة) ونرسمها — والنسخة التفاعلية في `src/app.py`.
""")

md("## 0️⃣ المكتبات وتحميل البيانات")
code("""import sqlite3
import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
sns.set_style('whitegrid'); plt.rcParams['figure.dpi'] = 110

df = pd.read_csv('data/ecommerce_transactions.csv', parse_dates=['order_date'])
print('Shape:', df.shape, '| من', df['order_date'].min().date(), 'إلى', df['order_date'].max().date())
df.head(3)""",
stub="""import sqlite3
import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
# TODO: حمّل data/ecommerce_transactions.csv مع parse_dates لعمود order_date
df = ...
print(df.shape)""")

md(r"""## 1️⃣ تحميل البيانات في قاعدة SQL (sqlite في الذاكرة)
بدل ما نعمل كل حاجة بـ pandas، هنحمّل الجدول في **sqlite** ونكتب **SQL حقيقي** — ده اللي بيحصل في
الشغل الفعلي (البيانات في قاعدة بيانات، والمحلل بيكتب استعلامات).""")
code("""conn = sqlite3.connect(':memory:')
df.to_sql('sales', conn, index=False, if_exists='replace')

def q(sql):
    return pd.read_sql(sql, conn)

print(q("SELECT COUNT(*) AS rows, COUNT(DISTINCT customer_id) AS customers FROM sales"))""",
stub="""conn = sqlite3.connect(':memory:')
# TODO: حمّل df في جدول اسمه sales، وعرّف دالة q(sql) ترجّع pd.read_sql
df.to_sql('sales', conn, index=False, if_exists='replace')
def q(sql): ...
print(q("SELECT COUNT(*) AS rows FROM sales"))""")

md(r"""## 2️⃣ مؤشرات الأداء الرئيسية (KPIs) — بـ SQL
- **Revenue:** إجمالي الإيرادات · **Orders:** عدد الطلبات · **AOV:** متوسط قيمة الطلب (Average Order Value)
- **Customers:** عدد العملاء · **Repeat-rate:** نسبة العملاء اللي طلبوا أكتر من مرة""")
code("""kpi = q('''
    SELECT
        ROUND(SUM(total_amount), 0)                    AS revenue,
        COUNT(*)                                       AS orders,
        ROUND(SUM(total_amount) * 1.0 / COUNT(*), 2)   AS aov,
        COUNT(DISTINCT customer_id)                    AS customers
    FROM sales
''').iloc[0]

repeat = q('''
    WITH per_customer AS (
        SELECT customer_id, COUNT(*) AS n FROM sales GROUP BY customer_id
    )
    SELECT ROUND(AVG(n > 1) * 100, 1) AS repeat_rate_pct FROM per_customer
''').iloc[0, 0]

print(f"💰 Revenue       = ${kpi.revenue:,.0f}")
print(f"🧾 Orders        = {kpi.orders:,}")
print(f"📊 AOV           = ${kpi.aov:,.2f}")
print(f"👥 Customers     = {kpi.customers:,}")
print(f"🔁 Repeat rate   = {repeat}%")""",
stub="""# TODO: اكتب SQL يحسب revenue, orders, aov, customers + repeat-rate
kpi = q('''SELECT ... FROM sales''').iloc[0]
repeat = ...
print(kpi)""")

md("## 3️⃣ الاتجاه الشهري للإيرادات (Monthly Trend) — SQL + رسم")
code("""monthly = q('''
    SELECT strftime('%Y-%m', order_date) AS month,
           ROUND(SUM(total_amount), 0)   AS revenue,
           COUNT(*)                      AS orders
    FROM sales GROUP BY month ORDER BY month
''')
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(monthly['month'], monthly['revenue'], marker='o')
ax.set_title('Monthly Revenue'); ax.set_ylabel('Revenue ($)')
plt.xticks(rotation=45, ha='right'); plt.tight_layout(); plt.show()
monthly.head()""",
stub="""# TODO: SQL يجمّع الإيرادات حسب الشهر (strftime) وارسمها كخط زمني
monthly = q('''SELECT ... ''')
...""")

md("## 4️⃣ التقسيمات: الفئة · أعلى المنتجات · الدول (Breakdowns)")
code("""by_cat = q("SELECT category, ROUND(SUM(total_amount),0) AS revenue "
            "FROM sales GROUP BY category ORDER BY revenue DESC")
top_prod = q("SELECT product_name, ROUND(SUM(total_amount),0) AS revenue, SUM(quantity) AS units "
             "FROM sales GROUP BY product_name ORDER BY revenue DESC LIMIT 10")
by_country = q("SELECT country, ROUND(SUM(total_amount),0) AS revenue "
               "FROM sales GROUP BY country ORDER BY revenue DESC")
print('الفئات:'); print(by_cat.to_string(index=False))
print('\\nأعلى 5 منتجات:'); print(top_prod.head().to_string(index=False))""",
stub="""# TODO: 3 استعلامات: الإيراد حسب الفئة، أعلى 10 منتجات، الإيراد حسب الدولة
by_cat = q("SELECT ...")
top_prod = q("SELECT ...")
by_country = q("SELECT ...")
print(by_cat)""")

md(r"""## 5️⃣ اللوحة الثابتة (Dashboard) — كل المؤشرات في صورة واحدة
لوحة من 4 لوحات فرعية: الاتجاه الشهري · الإيراد حسب الفئة · أعلى المنتجات · أعلى الدول.""")
code("""fig, ax = plt.subplots(2, 2, figsize=(15, 9))
fig.suptitle('🛍️ E-Commerce Sales Dashboard', fontsize=16, fontweight='bold')

ax[0,0].plot(monthly['month'], monthly['revenue'], marker='o', color='#2563eb')
ax[0,0].set_title('Monthly Revenue'); ax[0,0].tick_params(axis='x', rotation=45)

sns.barplot(data=by_cat, y='category', x='revenue', ax=ax[0,1], color='#10b981')
ax[0,1].set_title('Revenue by Category'); ax[0,1].set_ylabel('')

sns.barplot(data=top_prod, y='product_name', x='revenue', ax=ax[1,0], color='#f59e0b')
ax[1,0].set_title('Top 10 Products'); ax[1,0].set_ylabel('')

sns.barplot(data=by_country.head(8), y='country', x='revenue', ax=ax[1,1], color='#ef4444')
ax[1,1].set_title('Top Countries'); ax[1,1].set_ylabel('')

plt.tight_layout(rect=[0, 0, 1, 0.97]); plt.show()""",
stub="""# TODO: ابنِ شبكة 2x2 من اللوحات الفرعية (trend + category + products + country)
fig, ax = plt.subplots(2, 2, figsize=(15, 9))
...
plt.tight_layout(); plt.show()""")

md(r"""## 6️⃣ الخلاصة والتوصيات (Conclusion)
- **المؤشرات:** استخرجناها بـ **SQL حقيقي** (sqlite) زي ما بيحصل في الشغل، مش بس pandas.
- **اللوحة:** بتوصّل صحّة البيزنس في صورة واحدة — اتجاه + أعلى فئات/منتجات/دول.
- **قرارات مقترحة:** ركّز المخزون على أعلى المنتجات، استهدف الدول الأعلى إيراداً، واشتغل على رفع
  **Repeat-rate** (ولاء العملاء) لأن جذب عميل جديد أغلى من الاحتفاظ بعميل.
- **للإنتاج:** اللوحة التفاعلية في `src/app.py` (Streamlit + Plotly) فيها فلاتر (دولة/فئة/تاريخ).

> ▶️ **شغّل اللوحة التفاعلية:**
> ```bash
> pip install streamlit plotly
> streamlit run src/app.py
> ```
> ✅ **اللي اتعلمته:** SQL للتجميع، حساب KPIs، التصوير كلوحة، وربطها بأداة تفاعلية.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "a1_sales_dashboard")
