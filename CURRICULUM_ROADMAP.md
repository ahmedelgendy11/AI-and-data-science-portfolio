# 🗺️ خريطة منهج Data Science & Machine Learning الكاملة
### (Curriculum Roadmap — بالترتيب المنطقي ومبنية على أقوى الكتب المرجعية)

> **القاعدة:** لا تنتقل لوحدة قبل ما تخلّص اللي قبلها. كل وحدة بتبني على اللي فاتت.
> **لغة المحتوى:** عربي + المصطلحات التقنية بالإنجليزي بين قوسين.
> **رمز الحالة:** ✅ موجود عندك | 🔧 موجود بس يتعمّق | 🆕 جديد بالكامل (ناقص)

---

## 🧱 المرحلة 0 — الأساسيات والأدوات (Foundations & Tooling)

### الوحدة 1 — Python للبيانات + NumPy + Pandas
- **📕 الكتاب المعتمد:** *Python for Data Analysis* — Wes McKinney (مؤلف pandas نفسه)
- **ليه هنا:** ده لسان الشغل. مينفعش تحلل بيانات قبل ما تتقن الأداة.
- **المواضيع:** NumPy (vectorization, broadcasting) · Pandas (indexing, groupby, merge/join types, pivot/melt, multi-index, apply) · قراءة/كتابة الملفات.
- **بيُستخدم في:** كل سطر هتكتبه بعد كده.
- **الحالة:** 🔧 عندك Pandas أساسي — ناقص: merge types, pivot, melt, multi-index, apply المتقدم.

---

## 📊 المرحلة 1 — الرياضيات والإحصاء (Math & Statistics)

### الوحدة 2 — رياضيات التعلم الآلي
- **📘 الكتاب المعتمد:** *Mathematics for Machine Learning* — Deisenroth, Faisal, Ong (مجاني)
- **ليه هنا:** كل خوارزمية ML تحتها جبر خطي وتفاضل. لازم تفهم الأساس قبل الخوارزمية.
- **المواضيع:** الجبر الخطي (vectors, matrices, dot product, determinant, inverse, eigenvalues) · التفاضل (derivatives, gradients, chain rule) · Gradient Descent من الصفر.
- **بيُستخدم في:** PCA, Gradient Descent, Neural Networks, كل التحسين (optimization).
- **الحالة:** 🔧 عندك أساسي (matrix product, GD step) — ناقص: eigenvalues, chain rule كاملة.

### الوحدة 3 — الإحصاء الوصفي والاحتمالات
- **📗 الكتاب المعتمد:** *Practical Statistics for Data Scientists* — Bruce & Bruce
- **ليه هنا:** البيانات لغتها الإحصاء. لازم تفهم التوزيعات قبل ما تستنتج أي حاجة.
- **المواضيع:** مقاييس النزعة المركزية والتشتت · التوزيعات (Normal, Binomial, Poisson) · Bayes Theorem · Central Limit Theorem · Bootstrap & Resampling.
- **بيُستخدم في:** فهم البيانات، Naive Bayes، فترات الثقة، أي استنتاج.
- **الحالة:** 🆕 ناقص بالكامل تقريباً (التوزيعات، Bayes، Bootstrap, CLT).

### الوحدة 4 — الإحصاء الاستدلالي و A/B Testing
- **📗 الكتاب المعتمد:** *Practical Statistics for Data Scientists* — Bruce & Bruce
- **ليه هنا:** ده اللي بيحوّلك من حد بيرسم رسومات لحد بياخد قرارات. أهم مهارة لمحلل بيانات في شركة.
- **المواضيع:** فترات الثقة (Confidence Intervals) · اختبار الفرضيات (t-test, ANOVA, Chi-Square) · **A/B Testing** · p-value pitfalls & Multiple Testing · Effect Size & Statistical Power · Correlation vs Causation.
- **بيُستخدم في:** قرارات المنتج، تجارب التسويق، تقييم أي تغيير في شركة.
- **الحالة:** 🔧 عندك t-test, ANOVA, Chi-Square — ناقص: **A/B Testing**, الـ power, الـ multiple testing (وده الأهم).

---

## 🧹 المرحلة 2 — معالجة البيانات والتصوير المرئي و SQL

### الوحدة 5 — تنظيف البيانات و EDA
- **📕 الكتاب المعتمد:** *Python for Data Analysis* — McKinney + *Hands-On ML* (ch.2) — Géron
- **المواضيع:** القيم المفقودة (Imputation strategies) · المكررات · التواريخ · القيم الشاذة (Outliers) · توحيد الفئات.
- **بيُستخدم في:** 80% من وقت أي مشروع حقيقي بيروح في التنظيف.
- **الحالة:** ✅ مغطّى كويس (E-commerce, Health projects).

### الوحدة 6 — التصوير المرئي ورواية البيانات (Visualization & Storytelling)
- **📙 الكتاب المعتمد:** *Storytelling with Data* — Cole Nussbaumer Knaflic + *Fundamentals of Data Visualization* — Wilke
- **ليه هنا:** التحليل بلا توصيل = صفر. مهارة جوهرية لمحلل البيانات.
- **المواضيع:** Matplotlib & Seaborn بعمق · اختيار نوع الرسم الصح · مبادئ التصميم · Plotly التفاعلي · لوحات المعلومات (Dashboards بـ Streamlit).
- **بيُستخدم في:** كل تقرير وعرض هتقدّمه لمدير أو عميل.
- **الحالة:** 🆕 ناقص كوحدة مستقلة (بترسم داخل المشاريع بس مفيش تأسيس).

### الوحدة 7 — SQL لتحليل البيانات
- **📓 الكتاب المعتمد:** *SQL for Data Analysis* — Cathy Tanimura
- **ليه هنا:** البيانات في الشركات في قواعد بيانات مش CSV. مهارة لا غنى عنها.
- **المواضيع:** SELECT/WHERE/GROUP BY · JOINs (كل الأنواع) · Subqueries · CTEs · Window Functions · التجميعات المتقدمة.
- **بيُستخدم في:** سحب البيانات من أي شركة، معظم وظائف المحللين بتطلبها.
- **الحالة:** ✅ مغطّى كويس (SQL Mastery project) — ممكن إضافة date functions.

---

## 🤖 المرحلة 3 — التعلم الآلي الكلاسيكي (Classical ML) — قلب المنهج

> **📚 الكتابان المرجعيان لكل هذه المرحلة:**
> - *An Introduction to Statistical Learning (ISLR)* — للنظرية والفهم (مجاني)
> - *Hands-On Machine Learning* — Géron — للتطبيق العملي بـ scikit-learn

### الوحدة 8 — منهجية مشروع ML الكامل (The ML Workflow)
- **ليه هنا أول حاجة في ML:** لازم تتعلّم الإطار الصح قبل أي خوارزمية، عشان متتعلمش عادات غلط.
- **المواضيع:** تقسيم Train/Validation/Test · **Data Leakage** (أخطر غلطة) · **Cross-Validation** (k-fold, stratified) · **sklearn Pipeline & ColumnTransformer** · **Bias-Variance Tradeoff** + Learning Curves.
- **بيُستخدم في:** كل مشروع ML بدون استثناء.
- **الحالة:** 🆕 ناقص (عندك GridSearch بس مفيش فهم CV أو Pipeline أو Leakage).

### الوحدة 9 — الانحدار (Regression)
- **المواضيع:** Linear Regression · Polynomial · **Regularization** (Ridge, Lasso, ElasticNet) · مقاييس (RMSE, MAE, R²) · افتراضات الانحدار.
- **بيُستخدم في:** التنبؤ بالأسعار، الطلب، أي قيمة رقمية مستمرة.
- **الحالة:** 🔧 عندك Regularization + GridSearch + RMSE — يتعمّق بالافتراضات والمقاييس.

### الوحدة 10 — التصنيف (Classification)
- **المواضيع:** Logistic Regression · **kNN** · **Decision Trees** (Gini/Entropy) · Naive Bayes · SVM · **مقاييس التقييم العميقة** (Precision/Recall, F1, **ROC-AUC**, PR-Curve, Confusion Matrix, Calibration) · **Imbalanced Data** (SMOTE, class_weight).
- **بيُستخدم في:** التنبؤ بالـ churn، الموافقة على القروض، التشخيص الطبي، كشف الاحتيال.
- **الحالة:** 🔧 عندك LogReg/RF/GBM/NB/SVM — ناقص: **kNN، Decision Tree لوحده، ROC-AUC، PR-Curve، Imbalanced data** (مهم جداً).

### الوحدة 11 — التجميعات وأشجار القرار المتقدمة (Ensembles)
- **📓 كتاب إضافي:** *Approaching (Almost) Any ML Problem* — Abhishek Thakur
- **المواضيع:** Bagging · Random Forest · Boosting · **XGBoost / LightGBM / CatBoost** · **Feature Importance & SHAP** (تفسير الموديل).
- **بيُستخدم في:** الموديل اللي بيكسب 80% من مسابقات Kaggle على البيانات الجدولية. صناعة قياسية.
- **الحالة:** 🆕 ناقص بالكامل (**XGBoost, SHAP** — وده من أهم النواقص).

### الوحدة 12 — التعلم غير الموجَّه (Unsupervised Learning)
- **المواضيع:** K-Means + Elbow + Silhouette · Hierarchical Clustering · DBSCAN · **PCA** · **Anomaly Detection** (Isolation Forest).
- **بيُستخدم في:** تقسيم العملاء، ضغط البيانات، كشف الشذوذ والاحتيال.
- **الحالة:** 🔧 عندك K-Means + PCA + Silhouette — ناقص: DBSCAN, Hierarchical, **Anomaly Detection**.

### الوحدة 13 — هندسة الميزات (Feature Engineering)
- **📔 الكتاب المعتمد:** *Feature Engineering for Machine Learning* — Zheng & Casari
- **المواضيع:** Encoding (One-Hot, Target, Ordinal) · Scaling · Binning · Interaction features · Feature Selection.
- **بيُستخدم في:** الفرق بين موديل ضعيف وموديل قوي غالباً في الميزات مش الخوارزمية.
- **الحالة:** 🔧 عندك One-Hot + Scaling — ناقص: Target encoding, Binning, Feature Selection.

---

## 🧠 المرحلة 4 — التعلم العميق (Deep Learning)

> **📚 المرجعان:** *Hands-On ML (Part 2)* — Géron (تطبيق) + *Deep Learning* — Goodfellow (نظرية)

### الوحدة 14 — الشبكات العصبية من الأساس
- **المواضيع:** النيورون · Activation Functions · **Backpropagation** · Loss Functions · **Optimizers** (SGD, Momentum, Adam).
- **بيُستخدم في:** أساس كل الـ AI الحديث.
- **الحالة:** 🔧 عندك نيورون + MLP من NumPy (ممتاز للفهم) — ناقص: backprop كاملة، optimizers.

### الوحدة 15 — التطبيق بـ Keras / PyTorch
- **المواضيع:** بناء شبكة بـ Keras/PyTorch · Regularization (Dropout, Batch Norm, Early Stopping) · GPU.
- **بيُستخدم في:** أي مشروع deep learning حقيقي (الـ NumPy مش عملي للإنتاج).
- **الحالة:** 🆕 ناقص بالكامل (إطار عمل حقيقي).

### الوحدة 16 — الشبكات المتخصصة
- **المواضيع:** **CNN** (للصور) · **RNN / LSTM** (للتسلسل) · **Transformers & Attention** (أساس الـ LLMs).
- **بيُستخدم في:** الرؤية الحاسوبية، الترجمة، الـ ChatGPT.
- **الحالة:** 🆕 ناقص بالكامل.

---

## 🎯 المرحلة 5 — التخصصات (Specializations)

### الوحدة 17 — معالجة اللغات الطبيعية (NLP)
- **📒 الكتاب المعتمد:** *Speech and Language Processing* — Jurafsky & Martin (مجاني)
- **المواضيع:** Tokenization, Stemming, Lemmatization · n-grams · TF-IDF · **Word Embeddings (Word2Vec, GloVe)** · Text Classification · NER · مقدمة Transformers/BERT.
- **بيُستخدم في:** تحليل المشاعر، الشات بوتس، البحث، تلخيص النصوص.
- **الحالة:** 🔧 عندك TF-IDF + تنظيف نصوص — ناقص: **Embeddings, lemmatization, NER, n-grams**.

### الوحدة 18 — السلاسل الزمنية (Time Series)
- **📔 الكتاب المعتمد:** *Forecasting: Principles and Practice* — Hyndman & Athanasopoulos (مجاني)
- **المواضيع:** Stationarity (ADF) · Decomposition · Autocorrelation (ACF/PACF) · Exponential Smoothing (Holt-Winters) · ARIMA / **SARIMA** · **Prophet** · Time-Series Cross-Validation.
- **بيُستخدم في:** التنبؤ بالمبيعات، الطلب، الأسعار، استهلاك الطاقة.
- **الحالة:** 🔧 عندك ADF + Decompose + Holt-Winters + ARIMA — ناقص: **SARIMA, Prophet, ACF/PACF, TS-CV**.

### الوحدة 19 — أنظمة التوصية (Recommender Systems)
- **المواضيع:** Content-Based · Collaborative Filtering · Matrix Factorization.
- **بيُستخدم في:** Netflix, Amazon, Spotify — مشروع كلاسيكي في البورتفوليو.
- **الحالة:** 🆕 ناقص بالكامل.

### الوحدة 20 — الذكاء الاصطناعي التوليدي والـ LLMs
- **المواضيع:** Prompt Engineering · Embeddings الحقيقية · **RAG** (Vector Search) · استدعاء LLM API فعلي · تقييم المخرجات.
- **بيُستخدم في:** بناء تطبيقات على ChatGPT/Claude، المساعدين الأذكياء.
- **الحالة:** 🔧 عندك محاكاة (mock) + cosine similarity — يتعمّق بـ embeddings حقيقية و vector DB.

---

## 🚀 المرحلة 6 — الإنتاج (Production / MLOps)

### الوحدة 21 — نشر ومراقبة الموديلات
- **📕 الكتاب المعتمد:** *Designing Machine Learning Systems* — Chip Huyen
- **ليه في الآخر:** ده اللي بيحوّل الموديل من نوتبوك لمنتج بيشتغل. آخر حلقة.
- **المواضيع:** حفظ الموديل (joblib/pickle) · نشره بـ **FastAPI** · **Data Drift & Model Monitoring** · Experiment Tracking (MLflow) · مقدمة Docker.
- **بيُستخدم في:** أي وظيفة ML Engineer أو نقل موديل للإنتاج الحقيقي.
- **الحالة:** 🆕 ناقص بالكامل.

---

## 📌 ملخص الأولويات (أهم النواقص اللي تسدّها الأول)
1. 🔴 **A/B Testing** (الوحدة 4)
2. 🔴 **ML Workflow كامل**: CV + Pipeline + Leakage + Bias-Variance (الوحدة 8)
3. 🔴 **مقاييس التقييم + Imbalanced Data** (الوحدة 10)
4. 🔴 **XGBoost + SHAP** (الوحدة 11)
5. 🟠 **التوزيعات + Bootstrap + Bayes** (الوحدة 3)
6. 🟠 **Deep Learning بإطار حقيقي + CNN/RNN/Transformers** (الوحدات 15–16)
7. 🟠 **Word Embeddings** (الوحدة 17)
8. 🟡 **Visualization & Storytelling** كوحدة مستقلة (الوحدة 6)
9. 🟡 **MLOps / النشر** (الوحدة 21)

---

### 🧭 قالب كل تمرين من الآن (كما طلبت)
> **📚 قبل التمرين — محتاج تذاكر:** [المفاهيم + الكتاب والـ chapter]
> **🎯 بيُستخدم في:** [الاستخدام الواقعي في الشركات]
> **✍️ التمرين:** ...
