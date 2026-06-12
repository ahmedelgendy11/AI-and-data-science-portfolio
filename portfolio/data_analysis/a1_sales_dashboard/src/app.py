# -*- coding: utf-8 -*-
"""
🛍️ Sales Performance Dashboard — Streamlit + Plotly (production app).

تشغيل:
    pip install streamlit plotly pandas
    streamlit run src/app.py

ملاحظة: ده كود إنتاجي تفاعلي — مش بيتنفّذ داخل النوتبوك. النوتبوك بيعمل نفس التحليل
        ثابتاً بـ SQL + matplotlib؛ هنا بنحوّله للوحة تفاعلية فيها فلاتر.
"""
import os
import pandas as pd
import streamlit as st
import plotly.express as px

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "ecommerce_transactions.csv")

st.set_page_config(page_title="Sales Dashboard", page_icon="🛍️", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA, parse_dates=["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


df = load_data()

# ---- الفلاتر (Sidebar) ----
st.sidebar.header("⚙️ الفلاتر")
countries = st.sidebar.multiselect("الدولة", sorted(df["country"].unique()))
categories = st.sidebar.multiselect("الفئة", sorted(df["category"].unique()))
dmin, dmax = df["order_date"].min().date(), df["order_date"].max().date()
date_range = st.sidebar.date_input("الفترة", (dmin, dmax), min_value=dmin, max_value=dmax)

f = df.copy()
if countries:
    f = f[f["country"].isin(countries)]
if categories:
    f = f[f["category"].isin(categories)]
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    f = f[(f["order_date"] >= start) & (f["order_date"] <= end)]

# ---- بطاقات الـ KPIs ----
st.title("🛍️ لوحة أداء المبيعات")
revenue = f["total_amount"].sum()
orders = len(f)
aov = revenue / orders if orders else 0
repeat = (f.groupby("customer_id").size() > 1).mean() * 100 if orders else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💰 الإيرادات", f"${revenue:,.0f}")
c2.metric("🧾 الطلبات", f"{orders:,}")
c3.metric("📊 متوسط الطلب", f"${aov:,.2f}")
c4.metric("👥 العملاء", f"{f['customer_id'].nunique():,}")
c5.metric("🔁 معدل التكرار", f"{repeat:.1f}%")

st.divider()

# ---- الرسوم التفاعلية ----
left, right = st.columns(2)

monthly = f.groupby("month", as_index=False)["total_amount"].sum().sort_values("month")
left.plotly_chart(
    px.line(monthly, x="month", y="total_amount", markers=True, title="الإيراد الشهري"),
    use_container_width=True,
)

by_cat = f.groupby("category", as_index=False)["total_amount"].sum().sort_values("total_amount")
right.plotly_chart(
    px.bar(by_cat, x="total_amount", y="category", orientation="h", title="الإيراد حسب الفئة"),
    use_container_width=True,
)

top_prod = (
    f.groupby("product_name", as_index=False)["total_amount"].sum()
    .sort_values("total_amount", ascending=False).head(10)
)
left.plotly_chart(
    px.bar(top_prod, x="total_amount", y="product_name", orientation="h", title="أعلى 10 منتجات"),
    use_container_width=True,
)

by_country = (
    f.groupby("country", as_index=False)["total_amount"].sum()
    .sort_values("total_amount", ascending=False).head(10)
)
right.plotly_chart(
    px.bar(by_country, x="country", y="total_amount", title="أعلى الدول إيراداً"),
    use_container_width=True,
)

st.caption("مشروع A1 — Sales Performance Dashboard · البيانات: ecommerce_transactions.csv")
