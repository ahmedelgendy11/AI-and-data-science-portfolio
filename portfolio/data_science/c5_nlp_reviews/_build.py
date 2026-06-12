# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 💬 ذكاء مراجعات العملاء — تصنيف المشاعر ونمذجة المواضيع (Review Intelligence: Sentiment + Topics)
### مشروع C5 — مسار علم البيانات (Data Science Track) ⭐

---
## 🎯 المشكلة التجارية (Business Problem)
شركة بتستقبل آلاف المراجعات يومياً ومش قادرة تقراها كلها. عايزين نظام:
1. **يصنّف مشاعر كل مراجعة** تلقائياً (إيجابي / سلبي / محايد) — عشان يرصدوا المشاكل بسرعة.
2. **يكتشف المواضيع المتكررة** (Topics) في المراجعات — عشان يعرفوا الناس بتشتكي/تمدح في إيه.

**نوعا المشكلة:** تصنيف نصوص (Text Classification) + نمذجة مواضيع غير موجّهة (Topic Modeling).

## 📦 ما الذي يثبته المشروع
تنظيف النصوص · TF-IDF · مقارنة مصنّفات نصوص · التعامل مع عدم التوازن ·
تمثيلات دلالية (LSA Embeddings) · **نمذجة المواضيع (LDA)** · التقييم بمصفوفة اللخبطة.
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| تنظيف النص (lowercasing, stopwords, tokenization) | Jurafsky — *Speech & Language Processing* (ch.2) | كل مهمة NLP بتبدأ بالتنظيف |
| **TF-IDF** | Jurafsky (ch.6) / Géron | تحويل النص لأرقام يفهمها الموديل |
| Naive Bayes للنصوص | Jurafsky (ch.4) | خط الأساس الكلاسيكي لتصنيف النص |
| Linear SVM / Logistic للنصوص | ISLR (ch.9) / Géron | الأقوى عادةً مع TF-IDF |
| عدم التوازن (class_weight, macro-F1) | Géron (ch.3) | المراجعات السلبية قليلة لكنها الأهم |
| تمثيلات دلالية (LSA / Embeddings) | Jurafsky (ch.6) | فهم المعنى لا الكلمات فقط |
| **نمذجة المواضيع (LDA)** | Blei et al. / Jurafsky | اكتشاف الثيمات المخفية بدون تسميات |

> 🎯 **بيُستخدم في الواقع:** مراقبة سمعة العلامة التجارية، تحليل تذاكر الدعم، تصنيف بريد، تحليل السوشيال ميديا.
> 🛠️ **ملاحظة إنتاجية:** للنصوص الحقيقية المعقّدة تُستخدم Embeddings من `sentence-transformers` أو BERT — هنا نستخدم LSA (خفيف ويشتغل بدون GPU).
""")

md("## 0️⃣ المكتبات")
code("""import numpy as np, pandas as pd, re
import matplotlib.pyplot as plt, seaborn as sns
sns.set_style('whitegrid'); np.random.seed(42)
print('ready ✓')""")

md("## 1️⃣ تحميل واستكشاف البيانات (EDA)")
code("""df = pd.read_csv('data/product_reviews_data.csv')
print('Shape:', df.shape)
print(df['sentiment'].value_counts())
df['text_len'] = df['review_text'].str.len()
fig, ax = plt.subplots(1,2, figsize=(13,4))
df['sentiment'].value_counts().plot(kind='bar', ax=ax[0], title='Sentiment distribution')
sns.boxplot(data=df, x='sentiment', y='text_len', ax=ax[1]); ax[1].set_title('Review length by sentiment')
plt.tight_layout(); plt.show()
df.head(3)""",
stub="""df = pd.read_csv('data/product_reviews_data.csv')
# TODO: اطبع shape وتوزيع sentiment، وارسم توزيع المشاعر وطول النص
print(df['sentiment'].value_counts())
df.head(3)""")

md(r"""> 📌 لاحظ: المراجعات الإيجابية أكتر بكتير → **بيانات غير متوازنة**. لذلك هنستخدم `macro-F1` و `class_weight`.""")

md("## 2️⃣ تنظيف النصوص (Text Preprocessing)")
code("""STOP = set('the a an and or but is are was were be been to of in on for with this that it i you my we'.split())
def clean(t):
    t = str(t).lower()
    t = re.sub(r'[^a-z\\s]', ' ', t)          # شيل الأرقام والرموز
    tokens = [w for w in t.split() if w not in STOP and len(w) > 2]
    return ' '.join(tokens)
df['clean'] = df['review_text'].apply(clean)
print('BEFORE:', df['review_text'].iloc[0])
print('AFTER :', df['clean'].iloc[0])""",
stub="""STOP = set('the a an and or but is are was were be to of in on for with this that it'.split())
def clean(t):
    # TODO: lowercase + شيل غير الحروف + شيل stopwords والكلمات القصيرة
    ...
df['clean'] = df['review_text'].apply(clean)
print(df['clean'].iloc[0])""")

md("## 3️⃣ تحويل TF-IDF + تقسيم البيانات")
code("""from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    df['clean'], df['sentiment'], test_size=0.25, stratify=df['sentiment'], random_state=42)
tfidf = TfidfVectorizer(ngram_range=(1,2), min_df=2, max_features=3000)
Xtr = tfidf.fit_transform(X_train); Xte = tfidf.transform(X_test)
print('TF-IDF matrix:', Xtr.shape, '| vocab:', len(tfidf.vocabulary_))""",
stub="""from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
# TODO: قسّم البيانات (stratify) ثم درّب TfidfVectorizer مع ngram_range=(1,2)
X_train, X_test, y_train, y_test = ...
tfidf = ...
Xtr, Xte = ...
print('shape:', Xtr.shape)""")

md("## 4️⃣ مقارنة مصنّفات النصوص (Model Battle)")
code("""from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score, classification_report, confusion_matrix
models = {
    'MultinomialNB': MultinomialNB(),
    'LogReg':        LogisticRegression(max_iter=1000, class_weight='balanced'),
    'LinearSVC':     LinearSVC(class_weight='balanced'),
}
best_name, best_f1, best_model = None, -1, None
for name, m in models.items():
    m.fit(Xtr, y_train)
    f1 = f1_score(y_test, m.predict(Xte), average='macro')
    print(f'{name:14} macro-F1 = {f1:.3f}')
    if f1 > best_f1: best_name, best_f1, best_model = name, f1, m
print('\\nBest:', best_name)""",
stub="""from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score, classification_report, confusion_matrix
# TODO: درّب وقارن الـ 3 موديلات بمقياس macro-F1 واختر الأفضل
models = {...}
# ...
best_model = ...""")

md("## 5️⃣ تقييم أفضل موديل")
code("""pred = best_model.predict(Xte)
print(classification_report(y_test, pred))
cm = confusion_matrix(y_test, pred, labels=best_model.classes_)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=best_model.classes_, yticklabels=best_model.classes_)
plt.xlabel('Predicted'); plt.ylabel('Actual'); plt.title(f'{best_name} — Confusion Matrix'); plt.show()""",
stub="""# TODO: classification_report + confusion matrix لأفضل موديل
pred = best_model.predict(Xte)
print(classification_report(y_test, pred))""")

md(r"""## 6️⃣ التمثيلات الدلالية (LSA Embeddings) + تصوير
نختزل آلاف أبعاد TF-IDF لبُعدين باستخدام **Truncated SVD (LSA)** ونرسم المراجعات ملوّنة بالمشاعر.""")
code("""from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=2, random_state=42)
emb = svd.fit_transform(tfidf.transform(df['clean']))
plt.figure(figsize=(7,5))
for s, c in [('positive','green'),('negative','red'),('neutral','gray')]:
    m = df['sentiment']==s
    plt.scatter(emb[m,0], emb[m,1], s=8, alpha=.4, label=s, color=c)
plt.legend(); plt.title('Reviews in 2D semantic space (LSA)'); plt.show()""",
stub="""from sklearn.decomposition import TruncatedSVD
# TODO: TruncatedSVD(n_components=2) على مصفوفة TF-IDF كاملة، ثم ارسمها ملوّنة بالمشاعر
svd = ...
emb = ...""")

md(r"""## 7️⃣ نمذجة المواضيع (Topic Modeling — LDA) 🔍
LDA بيكتشف "مواضيع" مخفية بدون أي تسميات. كل موضوع = مجموعة كلمات بتظهر مع بعض.""")
code("""from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
cv = CountVectorizer(max_features=1000, min_df=3)
dtm = cv.fit_transform(df['clean'])
lda = LatentDirichletAllocation(n_components=4, random_state=42)
lda.fit(dtm)
words = cv.get_feature_names_out()
for i, topic in enumerate(lda.components_):
    top = [words[j] for j in topic.argsort()[-8:][::-1]]
    print(f'Topic {i+1}: ' + ', '.join(top))""",
stub="""from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
# TODO: CountVectorizer ثم LDA بـ 4 مواضيع، واطبع أهم 8 كلمات لكل موضوع
cv = ...
lda = ...""")

md(r"""## 8️⃣ الخلاصة والتوصيات (Conclusion)
- **التصنيف:** LinearSVC/LogReg مع TF-IDF حقّقوا أعلى macro-F1 — يقدروا يصنّفوا المراجعات تلقائياً.
- **عدم التوازن:** استخدمنا `class_weight='balanced'` و `macro-F1` عشان الفئة السلبية المهمة ما تضيعش.
- **المواضيع (LDA):** كشفت ثيمات زي الجودة، التوصيل، السعر — معلومة قيّمة لفريق المنتج.
- **التوصية:** أتمتة تصنيف المراجعات الواردة + لوحة متابعة للمواضيع السلبية الصاعدة.
- **الخطوة القادمة:** استبدال TF-IDF بـ embeddings من `sentence-transformers` لرفع الدقة على النصوص المعقّدة.

> ✅ **اللي اتعلمته:** تنظيف النص، TF-IDF، مقارنة مصنّفات، عدم التوازن، LSA، و LDA.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "c5_nlp_reviews")
