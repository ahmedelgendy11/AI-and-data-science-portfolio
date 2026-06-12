# 🛍️ Sales Performance Dashboard

> Turn raw e-commerce transactions into an executive view of business health — built with **real SQL**, then shipped as an interactive **Streamlit + Plotly** app.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![SQL](https://img.shields.io/badge/SQL-sqlite-003B57) ![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-FF4B4B)

## 📌 Problem
Store management wants business health **at a glance**: revenue, orders, average order value, top
products/countries, and the monthly trend — to drive decisions on inventory, marketing, and expansion.

## 🧠 Approach
Load transactions into an in-memory **SQLite** database and write **real SQL** for every KPI (revenue,
orders, AOV, customers, repeat-rate), then aggregate monthly/category/product/country breakdowns and
render a 4-panel static dashboard. The same analysis is shipped as an interactive app in `src/app.py`.

## 📊 KPIs computed
`Revenue` · `Orders` · `AOV (Average Order Value)` · `Unique customers` · `Repeat-purchase rate` ·
monthly trend · revenue by category / top products / top countries.

## ▶️ Run
**Notebook (static analysis):**
```bash
conda run -n dsportfolio jupyter notebook a1_sales_dashboard_solution.ipynb
```
**Interactive dashboard (Streamlit + Plotly):**
```bash
pip install streamlit plotly
streamlit run src/app.py
```

## 🗂️ Files
- `a1_sales_dashboard_exercise.ipynb` — TODOs to solve
- `a1_sales_dashboard_solution.ipynb` — full working solution
- `src/app.py` — production Streamlit dashboard with country/category/date filters
- `data/ecommerce_transactions.csv` — ~15K transactions

## 🛠️ Skills demonstrated
`SQL aggregation` · `Pandas` · `KPI design` · `Data visualization` · `Streamlit` · `Plotly`

> 📈 The SQL-in-SQLite approach mirrors real analyst work, where data lives in a database and you query it — not just `df.groupby`.
