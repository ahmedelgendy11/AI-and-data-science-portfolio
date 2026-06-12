# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 🔎 محرك بحث دلالي (Semantic Search Engine)
### مشروع D2 — مسار الذكاء الاصطناعي التوليدي (GenAI Track)

---
## 🎯 المشكلة التجارية (Business Problem)
البحث التقليدي (Keyword) بيدوّر على الكلمة **بالحرف**. لو العميل كتب "بطارية بتقعد كتير"
والمراجعة مكتوب فيها "battery lasts long" — البحث العادي **مش هيلاقيها**. عايزين بحث **بالمعنى (Semantic)**.

**نوع المشكلة:** استرجاع معلومات (Information Retrieval) بالتمثيلات الدلالية.

## 📦 ما الذي يثبته المشروع
الفرق بين **البحث اللفظي (Lexical/TF-IDF)** و**الدلالي (Semantic/Embeddings)** ·
بناء فهرس متجهي · ترتيب النتائج (Ranking) · تقييم البحث · مسار الإنتاج (sentence-transformers).
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| البحث اللفظي (TF-IDF / BM25) | Jurafsky — *Speech & Language Processing* (ch.6) | خط الأساس — مطابقة الكلمات |
| **التضمينات الدلالية (Embeddings)** | Jurafsky (ch.6) | فهم المعنى لا الحروف |
| تشابه جيب التمام (Cosine) | Jurafsky (ch.6) | ترتيب النتائج حسب القرب |
| LSA (Latent Semantic Analysis) | Deerwester et al. | تمثيل دلالي خفيف بدون نماذج ضخمة |
| تقييم البحث (Precision@k) | أدبيات IR | قياس جودة الترتيب |

> 🎯 **بيُستخدم في الواقع:** بحث المنتجات، البحث في الوثائق، الأسئلة المتشابهة، التوصيات، أساس الـ RAG.
> 🛠️ **هنا:** نقارن TF-IDF (لفظي) مع LSA (دلالي خفيف). الخلية الأخيرة فيها كود `sentence-transformers` للإنتاج.
""")

md("## 0️⃣ المكتبات وتحميل المستندات")
code("""import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
df = pd.read_csv('data/product_reviews_data.csv')
docs = df['review_text'].tolist()
print(f'Corpus: {len(docs)} reviews')
print('Example:', docs[0])""",
stub="""import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
# TODO: حمّل المراجعات في قائمة docs
df = ...
docs = ...
print(len(docs))""")

md("## 1️⃣ الفهرس اللفظي (Lexical Index — TF-IDF)")
code("""tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1,2), min_df=2)
tfidf_matrix = tfidf.fit_transform(docs)
def lexical_search(query, k=5):
    qv = tfidf.transform([query])
    sims = cosine_similarity(qv, tfidf_matrix)[0]
    top = sims.argsort()[::-1][:k]
    return [(docs[i], round(float(sims[i]),3)) for i in top]
print('TF-IDF index:', tfidf_matrix.shape)""",
stub="""tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1,2), min_df=2)
tfidf_matrix = tfidf.fit_transform(docs)
def lexical_search(query, k=5):
    # TODO: حوّل الاستعلام، احسب cosine، رجّع أعلى k
    ...
print(tfidf_matrix.shape)""")

md(r"""## 2️⃣ الفهرس الدلالي (Semantic Index — LSA)
نختزل أبعاد TF-IDF بـ Truncated SVD → كل مستند يبقى متجه "دلالي" بيلتقط الكلمات اللي بتظهر مع بعض.""")
code("""svd = TruncatedSVD(n_components=80, random_state=42)
lsa_matrix = svd.fit_transform(tfidf_matrix)
def semantic_search(query, k=5):
    qv = svd.transform(tfidf.transform([query]))
    sims = cosine_similarity(qv, lsa_matrix)[0]
    top = sims.argsort()[::-1][:k]
    return [(docs[i], round(float(sims[i]),3)) for i in top]
print('LSA index:', lsa_matrix.shape, '| variance captured:', round(svd.explained_variance_ratio_.sum(),2))""",
stub="""svd = TruncatedSVD(n_components=80, random_state=42)
lsa_matrix = svd.fit_transform(tfidf_matrix)
def semantic_search(query, k=5):
    # TODO: حوّل الاستعلام عبر tfidf ثم svd، احسب cosine مع lsa_matrix
    ...
print(lsa_matrix.shape)""")

md("## 3️⃣ المقارنة على استعلامات حقيقية")
code("""for q in ["great battery life", "poor quality and broke", "good value for money"]:
    print(f'\\n🔍 Query: "{q}"')
    print('  Lexical :', lexical_search(q, 2)[0][0][:70])
    print('  Semantic:', semantic_search(q, 2)[0][0][:70])""",
stub="""# TODO: قارن نتائج lexical_search و semantic_search على 3 استعلامات
for q in ["great battery life", "poor quality and broke"]:
    print(q, semantic_search(q,1))""")

md(r"""## 4️⃣ (اختياري — إنتاج) تضمينات حقيقية بـ sentence-transformers
في الإنتاج نستخدم نماذج تضمين مدرّبة (BERT) لدقة أعلى بكتير. محاطة بـ try/except.""")
code("""try:
    from sentence_transformers import SentenceTransformer    # pip install sentence-transformers
    model = SentenceTransformer('all-MiniLM-L6-v2')
    emb = model.encode(docs, show_progress_bar=False)
    def neural_search(query, k=5):
        q = model.encode([query])
        sims = cosine_similarity(q, emb)[0]
        return [(docs[i], round(float(sims[i]),3)) for i in sims.argsort()[::-1][:k]]
    print(neural_search("battery lasts a long time", 2))
except Exception as e:
    print(f'[sentence-transformers not installed: {type(e).__name__}] — using LSA fallback above.')""")

md(r"""## 5️⃣ تقييم البحث (Precision@k)
نختبر باستعلامات معروف نوع نتيجتها (إيجابي/سلبي) ونقيس نسبة النتائج الصحيحة في أعلى k.""")
code("""tests = [("excellent and works perfectly", "positive"),
         ("broke and waste of money", "negative"),
         ("amazing quality highly recommend", "positive"),
         ("terrible would not recommend", "negative")]
sent = df['sentiment'].tolist()
def prec_at_k(search_fn, k=5):
    hits=0; tot=0
    for q, label in tests:
        res = search_fn(q, k)
        idxs = [docs.index(d) for d,_ in res]
        hits += sum(sent[i]==label for i in idxs); tot += k
    return hits/tot
print(f'Lexical  Precision@5 = {prec_at_k(lexical_search):.0%}')
print(f'Semantic Precision@5 = {prec_at_k(semantic_search):.0%}')""",
stub="""tests = [("excellent and works perfectly","positive"),("broke and waste of money","negative")]
sent = df['sentiment'].tolist()
# TODO: احسب Precision@5 للبحثين
...""")

md(r"""## 6️⃣ الخلاصة والتوصيات (Conclusion)
- **النتيجة:** البحث الدلالي (LSA) بيلاقي مراجعات متشابهة بالمعنى حتى لو الكلمات مختلفة — حاجة البحث اللفظي بيفشل فيها.
- **التقييم:** Precision@5 بيوضّح أي طريقة بتجيب نتائج أكثر صلة.
- **حدود LSA:** خفيف لكنه أضعف من نماذج التضمين الحقيقية (BERT).
- **التوصية للإنتاج:** `sentence-transformers` للتضمين + قاعدة متجهات (FAISS/pgvector) للسرعة على ملايين المستندات.
- **الخطوة القادمة:** بحث هجين (Hybrid = لفظي + دلالي) — الأفضل عملياً.

> ✅ **اللي اتعلمته:** الفرق بين اللفظي والدلالي، بناء فهرس، الترتيب بالـ cosine، و Precision@k.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "d2_semantic_search")
