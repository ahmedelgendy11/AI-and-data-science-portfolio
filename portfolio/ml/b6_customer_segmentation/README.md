# 👥 Customer Segmentation — Unsupervised Clustering

> Group customers into marketing segments with no predefined labels.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-clustering-orange)

## 📌 Problem
Marketing wants distinct customer segments to target each with a tailored campaign. There is no "correct"
answer — this is **unsupervised learning** (clustering).

## 🧠 Pipeline
1. **EDA** — feature relationships (age, income, spending).
2. **Scaling** — clustering uses distances, so features must be standardized.
3. **Choosing k** — Elbow (inertia) + **Silhouette** score.
4. **K-Means** — fit + **cluster profiling** (business personas).
5. **DBSCAN** — density-based clustering + outlier detection.
6. **PCA** — 2-D visualization of the segments.

## 📈 Results (this dataset)
- Best **k = 3** by silhouette; K-Means yields clear, interpretable personas.
- DBSCAN (eps=0.4) finds a consistent structure plus a set of outliers (special cases).
- Personas → tailored actions: VIP retention, spend stimulation, loyalty offers.

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook b6_customer_segmentation_solution.ipynb
```

## 🛠️ Skills demonstrated
`Unsupervised learning` · `K-Means` · `Elbow / Silhouette` · `DBSCAN` · `PCA` · `Cluster profiling`
