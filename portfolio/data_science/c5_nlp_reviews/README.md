# 💬 Review Intelligence — Sentiment Classification + Topic Modeling

> Automatically classify customer-review sentiment and discover the hidden themes people talk about.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-NLP-orange) ![NLP](https://img.shields.io/badge/NLP-TF--IDF%20%2B%20LDA-purple)

## 📌 Problem
Thousands of reviews arrive daily. This project builds (1) a **sentiment classifier**
(positive / negative / neutral) and (2) an unsupervised **topic model** to surface recurring themes.

## 🧠 Pipeline
1. **EDA** — class imbalance + length analysis.
2. **Text cleaning** — lowercasing, regex, stopwords, short-token removal.
3. **TF-IDF** with unigrams + bigrams.
4. **Model battle** — MultinomialNB vs Logistic Regression vs LinearSVC, scored by **macro-F1** with `class_weight='balanced'` (the negative class is rare but important).
5. **Evaluation** — classification report + confusion matrix.
6. **Semantic space** — Truncated SVD (LSA) 2-D embedding of reviews.
7. **Topic modeling** — LDA reveals themes (quality, delivery, price, support…).

## 📈 Results (this dataset)
- Best macro-F1 ≈ **0.97** (LogReg / LinearSVC); the *neutral* (mixed) class is the hardest — as expected.
- LDA topics map cleanly onto real aspects: build quality, customer service, battery/price, packaging/design.

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook c5_nlp_reviews_solution.ipynb
```

## 🛠️ Skills demonstrated
`Text preprocessing` · `TF-IDF` · `Naive Bayes / SVM / LogReg` · `Imbalanced text` · `macro-F1` ·
`LSA embeddings` · `LDA topic modeling`

> **Production note:** swap TF-IDF for `sentence-transformers` embeddings (BERT) for harder, real-world text.
