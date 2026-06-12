# 📊 Data Science & Machine Learning Portfolio

> منهج عملي كامل بالعربي + بورتفوليو مشاريع جاهزة للتشغيل على **Colab · Kaggle · VS Code**.
> A hands-on Arabic Data Science / ML curriculum and a portfolio of runnable projects.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange) ![MLflow](https://img.shields.io/badge/MLflow-tracking-0194E2) ![status](https://img.shields.io/badge/projects-15%20done-success)

كل مشروع له **نسختان**: `*_exercise.ipynb` (فيه TODOs تحلّها) و `*_solution.ipynb` (الحل الكامل المتحقَّق منه) + `README.md`.

---

## ▶️ طرق التشغيل (3 طرق)

### 1) ☁️ Google Colab (الأسهل — من غير تثبيت)
افتح أي نوتبوك من جدول المشاريع تحت بزرّ **Open in Colab**، وشغّل **أول خلية «إعداد التشغيل»** —
هتثبّت المكتبات الناقصة وتجيب الداتا تلقائياً، وبعدها شغّل باقي الخلايا عادي.

### 2) 🟦 Kaggle Notebooks
اعمل *New Notebook* → File → *Import Notebook* → بتبويب **GitHub** حُطّ رابط الريبو واختار النوتبوك.
شغّل خلية «إعداد التشغيل» الأولى زي Colab.

### 3) 💻 VS Code (محلياً)
```bash
git clone https://github.com/Ahmedelgendyyy/data-science-portfolio.git
cd data-science-portfolio
conda env create -f environment.yml      # أو: pip install -r requirements.txt
```
بعدها افتح المجلد في VS Code، ثبّت الإضافات المقترحة (هتظهر تلقائياً)، وافتح أي نوتبوك ثم
اختر الـ kernel **dsportfolio** من أعلى اليمين. (الإعداد بيخلّي مسار التشغيل = مجلد النوتبوك تلقائياً.)

> 🔑 مشاريع GenAI (D1/D3) فيها خلية إنتاج اختيارية بتحتاج `ANTHROPIC_API_KEY` — بتتخطّى بأمان من غيره.

---

## 🗂️ المشاريع (Projects)

> الحالة: ✅ خلص ومتحقَّق · ⬜ قادم

### 🅰️ تحليل البيانات (Data Analysis)
| # | المشروع | المهارات | التشغيل |
|---|---|---|---|
| A1 | لوحة أداء مبيعات (Sales Dashboard) | SQL · KPIs · Plotly · Streamlit | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/data_analysis/a1_sales_dashboard/a1_sales_dashboard_solution.ipynb) |
| A2 | تحليل اختبار A/B | Power · z-test · Bootstrap · Bayesian | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/data_analysis/a2_ab_testing/a2_ab_testing_solution.ipynb) |

### 🅱️ تعلّم الآلة (Machine Learning)
| # | المشروع | المهارات | التشغيل |
|---|---|---|---|
| B1 | التنبؤ بالـ Churn + نشر FastAPI | XGBoost · SHAP · MLOps | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/ml/b1_churn_prediction/b1_churn_prediction_solution.ipynb) |
| B2 | أسعار العقارات | Feature Eng · Ridge/Lasso · GBM | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/ml/b2_house_prices/b2_house_prices_solution.ipynb) |
| B3 | مخاطر الائتمان | Imbalanced · Calibration · Cost | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/ml/b3_credit_risk/b3_credit_risk_solution.ipynb) |
| B4 | كشف الاحتيال | Isolation Forest · PR-AUC · P@k | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/ml/b4_fraud_detection/b4_fraud_detection_solution.ipynb) |
| B5 | مخاطر أمراض القلب | Classification · ROC-AUC · Leakage | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/ml/b5_heart_disease/b5_heart_disease_solution.ipynb) |
| B6 | تقسيم العملاء | KMeans · DBSCAN · PCA | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/ml/b6_customer_segmentation/b6_customer_segmentation_solution.ipynb) |

### 🅲 علم البيانات (Data Science)
| # | المشروع | المهارات | التشغيل |
|---|---|---|---|
| C1 | خط أنابيب ML + MLflow | Pipeline · CV · MLflow · Model selection | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/data_science/c1_mlflow_pipeline/c1_mlflow_pipeline_solution.ipynb) |
| C2 | السلاسل الزمنية (SARIMA) | Decompose · ACF/PACF · SARIMA | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/data_science/c2_timeseries_forecast/c2_timeseries_forecast_solution.ipynb) |
| C5 | تحليل المشاعر + المواضيع (NLP) | Embeddings · LDA · Classification | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/data_science/c5_nlp_reviews/c5_nlp_reviews_solution.ipynb) |
| C9 | دراسة إحصائية واختبار فرضيات | CLT · Bootstrap · t/ANOVA/χ² | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/data_science/c9_statistical_study/c9_statistical_study_solution.ipynb) |

### 🅳 الذكاء الاصطناعي التوليدي (GenAI)
| # | المشروع | المهارات | التشغيل |
|---|---|---|---|
| D1 | نظام أسئلة وأجوبة (RAG) | Embeddings · Vector Search · RAG | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/genai/d1_rag_qa/d1_rag_qa_solution.ipynb) |
| D2 | بحث دلالي (Semantic Search) | Sentence embeddings · Cosine | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/genai/d2_semantic_search/d2_semantic_search_solution.ipynb) |
| D3 | شات بوت بأدوات (Tool Use) | Function calling · Memory | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahmedelgendyyy/data-science-portfolio/blob/main/portfolio/genai/d3_chatbot_tools/d3_chatbot_tools_solution.ipynb) |

> 🗺️ الخريطة الكاملة للمنهج في [CURRICULUM_ROADMAP.md](CURRICULUM_ROADMAP.md) · كتالوج المشاريع في [PORTFOLIO_PROJECTS.md](PORTFOLIO_PROJECTS.md).
> 🚧 **قادم:** A3–A6 · B7–B10 · C4/C6/C7/C8/C10 · D4–D10 · مسار الرؤية الحاسوبية E1–E8 (على Colab/Kaggle للـ GPU).

---

## 🧱 هيكل الريبو
```
portfolio/<track>/<project>/
├── <project>_exercise.ipynb   ← نسخة فيها TODOs
├── <project>_solution.ipynb   ← الحل الكامل المتحقَّق منه
├── README.md                  ← وصف المشروع
├── data/                      ← الداتا (مضمَّنة للتشغيل السحابي)
└── src/                       ← كود إنتاجي (FastAPI / Streamlit) إن وُجد
```
