# 🤖 RAG Q&A System — Retrieval-Augmented Generation

> A customer-support assistant that answers questions **grounded in the company's own documents** — not the model's imagination.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![RAG](https://img.shields.io/badge/RAG-retrieval%2Bgeneration-purple) ![GenAI](https://img.shields.io/badge/GenAI-LLM-black)

## 📌 Problem
Customers repeatedly ask the same questions (shipping, returns, payment, warranty…). A RAG assistant
retrieves the relevant policy document and generates an answer from it — preventing hallucinations.

## 🧠 Pipeline
1. **Knowledge base** — 20 support documents (`data/knowledge_base.json`).
2. **Chunking** — split long docs into overlapping passages.
3. **Embeddings** — TF-IDF vectors (offline). *Production:* `sentence-transformers`.
4. **Vector search** — cosine similarity, top-k retrieval.
5. **RAG** — retrieve → build a grounded **prompt** → generate.
6. **Optional real LLM** — Anthropic/OpenAI cell, guarded so it runs offline too.
7. **Evaluation** — retrieval **Hit@k** on a labeled question set.

## 📈 Results (this dataset)
- **Hit@1 = 75%**, **Hit@3 = 92%** with TF-IDF retrieval.
- The gap shows exactly *why* production systems use dense embeddings: TF-IDF misses paraphrases
  ("get my money back" vs "refund").

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook d1_rag_qa_solution.ipynb
# optional real LLM:  pip install anthropic  &&  set ANTHROPIC_API_KEY=...
```

## 🛠️ Skills demonstrated
`Embeddings` · `Vector search` · `Chunking` · `RAG pipeline` · `Prompt engineering` · `Hit@k evaluation`

> **Production path:** dense embeddings (BERT) + a real vector DB (FAISS / Chroma / pgvector) + an LLM for fluent generation + answer-faithfulness evaluation.
