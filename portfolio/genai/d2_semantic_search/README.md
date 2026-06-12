# 🔎 Semantic Search Engine

> Search a corpus by **meaning**, not exact keywords — and learn when semantic actually beats lexical.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![NLP](https://img.shields.io/badge/NLP-IR-purple) ![GenAI](https://img.shields.io/badge/GenAI-embeddings-black)

## 📌 Problem
Keyword search matches literal words: a query "battery lasts long" misses a review saying
"great battery life" if the exact tokens differ. Semantic search ranks by meaning.

## 🧠 Pipeline
1. **Lexical index** — TF-IDF + cosine (baseline).
2. **Semantic index** — Truncated SVD (LSA) latent vectors.
3. **Side-by-side comparison** on real queries.
4. **Optional production embeddings** — `sentence-transformers` (guarded, runs offline too).
5. **Evaluation** — Precision@5 on labeled queries.

## 📈 Results (this dataset) — an honest lesson
| Method | Precision@5 |
|---|---|
| Lexical (TF-IDF) | 100% |
| Semantic (LSA) | 85% |

On a templated corpus with exact-keyword queries, **lexical wins**. Semantic search's real advantage
appears on **paraphrases/synonyms** and needs proper neural embeddings (BERT). The pro move is **hybrid
search** (lexical + semantic) — which is exactly what production systems do.

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook d2_semantic_search_solution.ipynb
# optional: pip install sentence-transformers
```

## 🛠️ Skills demonstrated
`Lexical vs semantic search` · `TF-IDF` · `LSA embeddings` · `Cosine ranking` · `Precision@k` · `Hybrid search`
