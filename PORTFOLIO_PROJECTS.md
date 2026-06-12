# 💼 كتالوج مشاريع البورتفوليو الكامل (Portfolio Projects Catalog)

> **44 مشروع** موزّعين على 5 مسارات (شامل Computer Vision). كل مشروع بنسختين: `_exercise` (فيه TODOs تحلّها) + `_solution` (الحل الكامل) + `README.md` احترافي.
> **رمز الحالة:** ⬜ لسه | 🏗️ بنشتغل عليه | ✅ خلص (تمرين + حل + README)
> كل مشروع له فولدر في `portfolio/<track>/<project>/`.

---

## 🅰️ المسار 1 — تحليل البيانات (Data Analysis) — 6 مشاريع

| # | المشروع | الداتا | المهارات الأساسية | الحالة |
|---|---|---|---|---|
| A1 | **لوحة أداء مبيعات التجارة الإلكترونية** (Sales Performance Dashboard) | ecommerce_transactions | SQL · Pandas · KPIs · Plotly · Streamlit | ✅ |
| A2 | **تحليل اختبار A/B لتجربة تحويل** (A/B Test Analysis) | يُولَّد | Power analysis · z-test · Bootstrap · Bayesian | ✅ |
| A3 | **تقسيم العملاء وتحليل RFM** (Customer Segmentation & RFM) | ecommerce + segmentation | RFM · KMeans · Business profiling | ⬜ |
| A4 | **تحليل القمع والاحتفاظ بالعملاء** (Funnel & Cohort Retention) | ecommerce_transactions | Cohort analysis · Retention curves · Funnel | ⬜ |
| A5 | **تقرير تحليل وتنبؤ المبيعات للمخزون** (Sales & Inventory Report) | excel_sales | Time aggregation · Trends · Reporting | ⬜ |
| A6 | **تحليل استنزاف الموظفين (HR Analytics)** | يُولَّد | EDA · Driver analysis · Dashboards | ⬜ |

**ليه المسار ده مهم:** بيثبت إنك بتحوّل البيانات لقرارات وتقارير — جوهر شغل المحلل.

---

## 🅱️ المسار 2 — تعلم الآلة (Machine Learning) — 10 مشاريع

| # | المشروع | الداتا | المهارات الأساسية | الحالة |
|---|---|---|---|---|
| B1 | **التنبؤ برحيل العملاء + نشر الموديل** ⭐ | ecommerce_transactions | Pipeline · SMOTE · **XGBoost · SHAP** · **FastAPI (MLOps)** | ✅ |
| B2 | **التنبؤ بأسعار العقارات** | house_prices | Feature Eng · Ridge/Lasso · GBM · Residuals | ✅ |
| B3 | **تقييم مخاطر الائتمان (Credit Risk)** | يُولَّد | Imbalanced · Calibration · Cost-sensitive | ✅ |
| B4 | **كشف الاحتيال / الشذوذ (Fraud Detection)** | يُولَّد | Isolation Forest · Imbalanced · PR-AUC | ✅ |
| B5 | **مصنّف مخاطر أمراض القلب** | health_risk | Classification · ROC-AUC · Interpretability · Leakage | ✅ |
| B6 | **تقسيم العملاء غير الموجَّه** | segmentation | KMeans · DBSCAN · PCA · Silhouette | ✅ |
| B7 | **نظام توصية (Recommender System)** | يُولَّد | Collaborative Filtering · Matrix Factorization | ⬜ |
| B8 | **التنبؤ بالطلب باستخدام ML** | energy_consumption | TS features · XGBoost · Backtesting | ⬜ |
| B9 | **التنبؤ بتكلفة التأمين** | يُولَّد | Regression · GLM · Feature interactions | ⬜ |
| B10 | **التنبؤ باستنزاف الموظفين + MLflow** | يُولَّد | Full pipeline · **Experiment Tracking (MLflow)** | ⬜ |

**MLOps مدمج في:** B1 (FastAPI serving + monitoring) و B10 (MLflow tracking + model registry).

---

## 🅲 المسار 3 — علم البيانات (Data Science) — 10 مشاريع

> أعمق: إحصاء متقدم + Deep Learning + استدلال سببي.

| # | المشروع | الداتا | المهارات الأساسية | الحالة |
|---|---|---|---|---|
| C1 | **خط أنابيب ML كامل مع تتبع التجارب** | house_prices | Pipelines · CV · **MLflow** · Model selection | ✅ |
| C2 | **التنبؤ بالسلاسل الزمنية (SARIMA + Prophet)** ⭐ | energy_consumption | Decompose · ACF/PACF · **SARIMA · Prophet** · TS-CV | ✅ |
| C3 | **تصنيف الصور بالتعلم العميق (CNN)** 🌐 | يُحمَّل (Fashion-MNIST) | **CNN · Keras** · Dropout · Augmentation | ⬜ |
| C4 | **شبكة عصبية للبيانات الجدولية** | health_risk | **Keras MLP** · Embeddings · Regularization | ⬜ |
| C5 | **تحليل المشاعر ونمذجة المواضيع (NLP)** ⭐ | product_reviews | Embeddings · **LDA Topic Modeling** · Classification | ✅ |
| C6 | **الاستدلال السببي ونمذجة الرفع (Causal/Uplift)** | يُولَّد | Causal inference · Uplift modeling · DiD | ⬜ |
| C7 | **الإحصاء البايزي (Bayesian A/B بـ PyMC)** 🌐 | يُولَّد | **PyMC** · Posterior · Hierarchical models | ⬜ |
| C8 | **تحليل البقاء (Survival Analysis للـ Churn)** | ecommerce | Kaplan-Meier · Cox PH · Lifelines | ⬜ |
| C9 | **دراسة إحصائية واختبار فرضيات شاملة** | health_risk | Distributions · CLT · Bootstrap · Tests | ✅ |
| C10 | **هندسة الميزات وتفسير الموديل (SHAP/LIME)** | house_prices | **SHAP · LIME · PDP** · Feature selection | ⬜ |

🌐 = يحتاج إنترنت/تحميل مكتبات إضافية.

---

## 🅳 المسار 4 — الذكاء الاصطناعي والـ GenAI — 10 مشاريع

> معظمها يحتاج **API key (OpenAI/Anthropic)** أو مكتبات تحميل (sentence-transformers). هنكتب الكود كامل وجاهز.

| # | المشروع | الأساس | المهارات الأساسية | الحالة |
|---|---|---|---|---|
| D1 | **نظام أسئلة وأجوبة بالـ RAG** ⭐ | knowledge_base.json | **Embeddings · Vector Search · RAG · LLM API** | ✅ |
| D2 | **محرك بحث دلالي (Semantic Search)** | product_reviews | Sentence embeddings · Vector similarity | ✅ |
| D3 | **شات بوت بذاكرة واستدعاء أدوات (Tool Use)** | LLM API | Conversation memory · **Function calling** | ✅ |
| D4 | **تلخيص المستندات الذكي (Summarization)** | نصوص | Chunking · Map-reduce summarization | ⬜ |
| D5 | **استخراج المعلومات المنظّمة من النص (Extraction)** | product_reviews | Structured output · JSON mode · NER | ⬜ |
| D6 | **تصنيف الصور بنماذج جاهزة (CLIP/Vision)** 🌐 | يُحمَّل | Pretrained models · Zero-shot · Embeddings | ⬜ |
| D7 | **ضبط نموذج محوّل صغير (Fine-tuning)** 🌐 | product_reviews | **HuggingFace · Transformers · Fine-tuning** | ⬜ |
| D8 | **سير عمل متعدد الوكلاء (Multi-Agent)** | LLM API | Agent orchestration · Planning · Tools | ⬜ |
| D9 | **إطار تقييم وحماية الـ LLM (Eval & Guardrails)** | LLM API | LLM evaluation · Hallucination checks · Safety | ⬜ |
| D10 | **نشر تطبيق LLM للإنتاج (Production)** ⭐ | الكل | **FastAPI streaming · Caching · Cost tracking** | ⬜ |

---

## 🅴 المسار 5 — الرؤية الحاسوبية (Computer Vision) — 8 مشاريع

> ⚠️ **يُنفَّذ على Kaggle / Google Colab** للاستفادة من الـ GPU المجاني (مش محلياً). يحتاج إطار DL (Keras/PyTorch) + داتاست صور.
> 🗓️ **مرحلة لاحقة:** نبنيه بعد ما نخلّص المشاريع الخفيفة + أساسيات الـ Deep Learning.

| # | المشروع | الداتا | المهارات الأساسية | الحالة |
|---|---|---|---|---|
| E1 | **تصنيف الصور بـ CNN من الصفر** ⭐ | Fashion-MNIST | **CNN · Conv/Pool · Keras** · Softmax | ⬜ |
| E2 | **التحسين: Data Augmentation + Regularization** | Fashion-MNIST/CIFAR | Augmentation · Dropout · BatchNorm · EarlyStopping | ⬜ |
| E3 | **التعلّم بالنقل (Transfer Learning)** ⭐ | CIFAR-10 / صور صغيرة | **Pretrained (MobileNet/ResNet)** · Fine-tuning | ⬜ |
| E4 | **تفسير الـ CNN بـ Grad-CAM** | صور | **Grad-CAM** · Saliency · Interpretability | ⬜ |
| E5 | **البحث البصري بالتشابه (Image Similarity Search)** | صور | **Image embeddings** · Cosine search · KNN | ⬜ |
| E6 | **كشف الأجسام (Object Detection)** 🌐 | صور | **YOLO (pretrained)** · Bounding boxes · IoU | ⬜ |
| E7 | **استخراج النص من الصور (OCR)** 🌐 | صور وثائق | **Tesseract/EasyOCR** · Preprocessing | ⬜ |
| E8 | **توليد الصور (Autoencoder / GAN)** | MNIST | **Autoencoder · GAN** · Latent space | ⬜ |

---

## 🔁 قالب كل مشروع (الهيكل الموحّد)
```
portfolio/<track>/<project>/
├── README.md              ← وصف احترافي للـ GitHub (المشكلة، الحل، النتائج، كيف تشغّله)
├── <project>_exercise.ipynb   ← نسخة فيها TODOs تحلّها
├── <project>_solution.ipynb   ← الحل الكامل الشغّال
├── data/                  ← الداتا (أو سكربت توليدها)
└── src/                   ← أي كود إنتاج (FastAPI, utils) لو موجود
```

### داخل كل notebook (الترتيب الثابت):
1. **🎯 تعريف المشكلة والهدف التجاري** (Business Problem)
2. **📚 قبل ما تبدأ — محتاج تذاكر** (مفاهيم + الكتاب + chapter) و **🎯 بيُستخدم في**
3. تحميل واستكشاف البيانات (EDA)
4. التنظيف وهندسة الميزات
5. النمذجة والمقارنة
6. التقييم والتفسير
7. الخلاصة والتوصيات التجارية + الخطوات القادمة

---

## 📌 ترتيب البناء المقترح (الأقوى للبورتفوليو الأول)
1. **B1** التنبؤ بالـ Churn + النشر (الأكثر إبهاراً)
2. **A2** اختبار A/B (أهم مهارة محلل)
3. **C2** السلاسل الزمنية SARIMA+Prophet
4. **C5** NLP المشاعر والمواضيع
5. **D1** نظام RAG
6. **B2** أسعار العقارات
... ثم الباقي بالترتيب.
