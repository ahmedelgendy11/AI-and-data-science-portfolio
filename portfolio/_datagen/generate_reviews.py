# -*- coding: utf-8 -*-
"""
Realistic product-review generator with genuine ambiguity so text
classification is non-trivial (target macro-F1 ~0.85-0.92, not 1.0).

Adds: varied vocabulary, aspect mentions (delivery/price/quality/...),
negations, mixed 'neutral' reviews, and ~5% label noise.
LDA topics become meaningful because reviews mention real aspects.
"""
import numpy as np, pandas as pd, sys
rng = np.random.default_rng(11)

PRODUCTS = ["Laptop X1", "Wireless Earbuds", "Coffee Maker", "Running Shoes",
            "Office Chair", "Smart Watch", "Backpack", "Blender Pro", "Desk Lamp", "Phone Case"]
ASPECTS = ["the delivery", "the build quality", "the price", "customer service",
           "the battery life", "the design", "the material", "the packaging", "the size"]

POS = ["excellent", "great", "fantastic", "love it", "works perfectly", "highly recommend",
       "worth every penny", "exceeded expectations", "very reliable", "amazing quality",
       "fast and smooth", "exactly as described", "super happy"]
NEG = ["terrible", "very disappointed", "broke after a week", "waste of money", "poor quality",
       "stopped working", "would not recommend", "cheaply made", "arrived damaged",
       "worst purchase", "regret buying", "far too slow"]
NEU = ["okay", "average", "nothing special", "does the job", "decent for the price",
       "as expected", "neither good nor bad", "fine I guess", "mediocre"]

def make(sent):
    asp = rng.choice(ASPECTS)
    if sent == "positive":
        parts = [rng.choice(POS), f"{asp} is great"]
        if rng.random() < 0.25: parts.append("not disappointed at all")     # negation w/ pos
    elif sent == "negative":
        parts = [rng.choice(NEG), f"{asp} is bad"]
        if rng.random() < 0.25: parts.append("not worth it")
    else:  # neutral = genuinely mixed -> the hard class
        parts = [rng.choice(NEU)]
        if rng.random() < 0.6: parts.append(f"{rng.choice(POS)} but {rng.choice(NEG)}")
        else: parts.append(f"{asp} is fine")
    rng.shuffle(parts)
    return ". ".join(p.capitalize() for p in parts) + "."

rows = []
N = 2600
probs = {"positive": 0.50, "negative": 0.27, "neutral": 0.23}
sentiments = rng.choice(list(probs), size=N, p=list(probs.values()))
for i, s in enumerate(sentiments):
    text = make(s)
    # ~5% label noise (realistic human mislabeling)
    label = s if rng.random() > 0.05 else rng.choice(["positive", "negative", "neutral"])
    rating = {"positive": rng.choice([4, 5]), "negative": rng.choice([1, 2]),
              "neutral": 3}[s]
    rows.append([f"REV{10000+i}", rng.choice(PRODUCTS), text, int(rating), label])

df = pd.DataFrame(rows, columns=["review_id", "product_name", "review_text", "rating", "sentiment"])
df = df.sample(frac=1, random_state=11).reset_index(drop=True)
out = sys.argv[1] if len(sys.argv) > 1 else "product_reviews_data.csv"
df.to_csv(out, index=False)
print(f"Wrote {out}: {len(df)} rows")
print(df["sentiment"].value_counts())
