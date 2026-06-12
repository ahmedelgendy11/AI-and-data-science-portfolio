# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 🤖 نظام أسئلة وأجوبة بالـ RAG (Retrieval-Augmented Generation Q&A)
### مشروع D1 — مسار الذكاء الاصطناعي التوليدي (GenAI Track) ⭐

---
## 🎯 المشكلة التجارية (Business Problem)
شركة عندها قاعدة معرفة (سياسات شحن، إرجاع، دفع، ضمان...) والعملاء بيسألوا نفس الأسئلة طول الوقت.
عايزين **مساعد ذكي يجاوب على أسئلة العملاء** بالاعتماد على **مستندات الشركة الحقيقية** —
مش من "مخيلة" النموذج (عشان ما يخترعش معلومات غلط / Hallucination).

**الحل:** RAG = **استرجاع (Retrieval)** المستند المناسب + **توليد (Generation)** إجابة مبنية عليه.

## 📦 ما الذي يثبته المشروع
تقطيع المستندات (Chunking) · **التضمينات (Embeddings)** · **البحث المتجهي (Vector Search)** ·
خط أنابيب RAG كامل · هندسة الـ Prompt · تقييم الاسترجاع (Hit@k) · مسار الإنتاج (LLM API).
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| التضمينات (Embeddings) | Jurafsky — *Speech & Language Processing* (ch.6) | تحويل النص لمتجه يمثّل المعنى |
| تشابه جيب التمام (Cosine Similarity) | Jurafsky (ch.6) | قياس قرب السؤال من المستندات |
| **RAG (Retrieval-Augmented Generation)** | Lewis et al. 2020 / وثائق LangChain | ربط الـ LLM بمصدر معرفة موثوق |
| Chunking (تقطيع المستندات) | أدلة RAG العملية | المستندات الطويلة تتقسّم لقطع قابلة للاسترجاع |
| هندسة الـ Prompt (Context injection) | وثائق OpenAI/Anthropic | حقن السياق المسترجَع في تعليمات النموذج |
| تقييم الاسترجاع (Recall@k / Hit@k) | أدبيات استرجاع المعلومات | قياس: هل جبنا المستند الصح؟ |

> 🎯 **بيُستخدم في الواقع:** شات بوتس خدمة العملاء، مساعدي الوثائق الداخلية، البحث القانوني/الطبي، كل تطبيقات "اسأل مستنداتك".
> 🛠️ **هنا أوفلاين:** نستخدم TF-IDF كـ embeddings ومولّد بسيط — والكود فيه خلايا اختيارية لـ `sentence-transformers` و LLM API حقيقي للإنتاج.
""")

md("## 0️⃣ المكتبات وتحميل قاعدة المعرفة")
code("""import json, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open('data/knowledge_base.json', encoding='utf-8') as f:
    KB = json.load(f)
print(f'Loaded {len(KB)} documents')
print('Example:', KB[0]['title'], '→', KB[0]['text'][:80], '...')""",
stub="""import json, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# TODO: حمّل data/knowledge_base.json
KB = ...
print(len(KB), 'documents')""")

md(r"""## 1️⃣ التقطيع (Chunking)
المستندات هنا قصيرة فكل مستند = قطعة واحدة. في الواقع المستندات الطويلة تتقسّم لقطع متداخلة
(مثلاً 200 كلمة بتداخل 40) عشان الاسترجاع يبقى دقيق. الدالة دي بتوضّح الفكرة.""")
code("""def chunk(text, size=60, overlap=15):
    words = text.split()
    if len(words) <= size:
        return [text]
    return [' '.join(words[i:i+size]) for i in range(0, len(words), size-overlap)]

# نبني فهرس القطع: كل قطعة تعرف مصدرها
chunks, meta = [], []
for doc in KB:
    for c in chunk(doc['text']):
        chunks.append(c); meta.append({'id': doc['id'], 'title': doc['title']})
print(f'{len(KB)} docs → {len(chunks)} chunks')""",
stub="""def chunk(text, size=60, overlap=15):
    # TODO: قسّم النص لقطع بطول size وتداخل overlap
    ...
chunks, meta = [], []
for doc in KB:
    for c in chunk(doc['text']):
        chunks.append(c); meta.append({'id': doc['id'], 'title': doc['title']})
print(len(chunks), 'chunks')""")

md(r"""## 2️⃣ بناء فهرس التضمينات (Embedding Index)
نحوّل كل قطعة لمتجه TF-IDF. (في الإنتاج: متجهات كثيفة من نموذج embeddings + قاعدة متجهات زي FAISS).""")
code("""embedder = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
doc_vectors = embedder.fit_transform(chunks)
print('Index shape:', doc_vectors.shape)""",
stub="""# TODO: درّب TfidfVectorizer على القطع واحصل على doc_vectors
embedder = ...
doc_vectors = ...
print(doc_vectors.shape)""")

md("## 3️⃣ دالة الاسترجاع (Retrieval — Top-k)")
code("""def retrieve(query, k=3):
    qv = embedder.transform([query])
    sims = cosine_similarity(qv, doc_vectors)[0]
    top = sims.argsort()[::-1][:k]
    return [(meta[i]['id'], meta[i]['title'], chunks[i], float(sims[i])) for i in top]

for r in retrieve("How long does delivery take?"):
    print(f"  [{r[3]:.2f}] {r[1]}")""",
stub="""def retrieve(query, k=3):
    # TODO: حوّل السؤال لمتجه، احسب cosine_similarity مع doc_vectors، رجّع أعلى k
    ...
for r in retrieve("How long does delivery take?"):
    print(r[1])""")

md(r"""## 4️⃣ خط أنابيب RAG: استرجاع → بناء Prompt → توليد
المولّد هنا **بسيط (extractive)** — بيبني الإجابة من السياق المسترجَع. الأهم: شكل الـ **Prompt**
اللي بيتبعت للـ LLM في الإنتاج (تعليمات + سياق + سؤال) — وده موضّح في الدالة.""")
code('''def build_prompt(query, contexts):
    ctx = "\\n".join(f"- {c[2]}" for c in contexts)
    return f"""You are a helpful support assistant. Answer ONLY using the context below.
If the answer is not in the context, say you don't know.

Context:
{ctx}

Question: {query}
Answer:"""

def rag_answer(query, k=3):
    contexts = retrieve(query, k)
    prompt = build_prompt(query, contexts)
    # --- مولّد بسيط (offline): يرجّع أكثر قطعة صلة كإجابة مبنية على المصدر ---
    answer = contexts[0][2]
    source = contexts[0][1]
    return answer, source, prompt

ans, src, prompt = rag_answer("Can I get a refund and how long does it take?")
print("ANSWER:", ans)
print("SOURCE:", src)''',
stub='''def build_prompt(query, contexts):
    # TODO: ابنِ prompt فيه تعليمات + السياق المسترجَع + السؤال
    ...
def rag_answer(query, k=3):
    contexts = retrieve(query, k)
    prompt = build_prompt(query, contexts)
    answer, source = contexts[0][2], contexts[0][1]
    return answer, source, prompt
print(rag_answer("Can I get a refund?")[0])''')

md(r"""## 5️⃣ (اختياري — إنتاج) توليد بـ LLM حقيقي
لو عندك مفتاح API، الخلية دي بتبعت السياق المسترجَع لـ Claude/GPT ليصيغ إجابة طبيعية.
محاطة بـ try/except عشان ما تكسرش النوتبوك أوفلاين.""")
code('''import os
def rag_answer_llm(query, k=3):
    contexts = retrieve(query, k)
    prompt = build_prompt(query, contexts)
    try:
        from anthropic import Anthropic                     # pip install anthropic
        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        msg = client.messages.create(model="claude-3-5-haiku-latest",
                                      max_tokens=300,
                                      messages=[{"role": "user", "content": prompt}])
        return msg.content[0].text
    except Exception as e:
        return f"[LLM skipped: {type(e).__name__}] Falling back to extractive answer:\\n{contexts[0][2]}"

print(rag_answer_llm("Do you ship internationally and how long?"))''')

md(r"""## 6️⃣ تقييم الاسترجاع (Retrieval Evaluation — Hit@k) 📊
المقياس الأساسي في RAG: **هل المستند الصح ظهر ضمن أعلى k نتيجة؟** نختبر بمجموعة أسئلة معروفة إجابتها.""")
code("""test_set = [
    ("How many days for standard shipping?",        "ship-01"),
    ("Do you deliver to other countries?",          "ship-02"),
    ("What is the minimum order for free shipping?","ship-03"),
    ("How do I return an item I bought?",           "ret-01"),
    ("When will I get my money back?",              "ret-02"),
    ("Which cards can I pay with?",                 "pay-01"),
    ("Can I pay in installments?",                  "pay-02"),
    ("Is there a warranty on electronics?",         "war-01"),
    ("I forgot my password, what do I do?",         "acc-02"),
    ("How do I reach customer service?",            "supp-01"),
    ("Can I cancel my order after placing it?",     "supp-02"),
    ("Do you match competitor prices?",             "prod-02"),
]
def hit_at_k(k):
    hits = sum(expected in [r[0] for r in retrieve(q, k)] for q, expected in test_set)
    return hits / len(test_set)
print(f'Hit@1 = {hit_at_k(1):.0%}')
print(f'Hit@3 = {hit_at_k(3):.0%}')""",
stub="""test_set = [("How many days for standard shipping?","ship-01"),
            ("How do I return an item?","ret-01"),
            ("Which cards can I pay with?","pay-01")]
# TODO: احسب Hit@1 و Hit@3 (هل المستند المتوقّع ضمن أعلى k؟)
def hit_at_k(k): ...
print('Hit@1:', hit_at_k(1))""")

md(r"""## 7️⃣ الخلاصة والتوصيات (Conclusion)
- **النتيجة:** خط أنابيب RAG كامل بيسترجع المستند الصح ويبني عليه الإجابة — Hit@3 عالي.
- **مكوّنات النظام:** Chunking → Embeddings → Vector Search → Prompt → Generation.
- **مكافحة الـ Hallucination:** الإجابة **مقيّدة بالسياق المسترجَع** فقط، مش معرفة النموذج العامة.
- **التوصية للإنتاج:**
  1. استبدال TF-IDF بـ `sentence-transformers` (دقة أعلى في فهم المعنى).
  2. استخدام قاعدة متجهات حقيقية (FAISS / Chroma / pgvector) للتوسّع.
  3. ربط LLM حقيقي (الخلية 5) لصياغة إجابات طبيعية.
  4. إضافة تقييم للإجابة نفسها (faithfulness) مش بس الاسترجاع.

> ✅ **اللي اتعلمته:** Embeddings، Vector Search، RAG، Prompt Engineering، وتقييم الاسترجاع.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "d1_rag_qa")
