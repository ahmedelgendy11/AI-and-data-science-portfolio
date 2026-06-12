# -*- coding: utf-8 -*-
"""
Realistic e-commerce transaction generator WITH learnable churn signal.

Each customer has a latent `engagement` that drives BOTH:
  - how often / how much they order historically (frequency, monetary), and
  - how long they stay active (whether they appear in the future window).
=> Historical RFM features genuinely predict future churn (target AUC ~0.80),
   while noise keeps it realistic (not a perfect separator).

Output schema matches the original dataset so notebooks need no changes:
order_id, customer_id, order_date, product_name, category,
unit_price, quantity, total_amount, country, payment_method
"""
import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)

N_CUSTOMERS = 1600
START = pd.Timestamp("2022-07-01")
SNAPSHOT = pd.Timestamp("2023-12-31")
TOTAL_DAYS = (SNAPSHOT - START).days

CATALOG = {
    "Electronics": ["Laptop", "Headphones", "Smartphone", "Monitor", "Keyboard"],
    "Home & Kitchen": ["Blender", "Coffee Maker", "Toaster", "Cookware Set"],
    "Clothing": ["Sneakers", "Jacket", "T-Shirt", "Jeans"],
    "Books": ["Novel", "Cookbook", "Biography"],
    "Beauty": ["Perfume", "Skincare Set", "Makeup Kit"],
}
PRICES = {"Electronics": (80, 1200), "Home & Kitchen": (20, 250),
          "Clothing": (15, 180), "Books": (8, 40), "Beauty": (12, 120)}
COUNTRIES = ["USA", "UK", "Germany", "France", "Canada", "Australia"]
PAYMENTS = ["Credit Card", "PayPal", "Debit Card", "Apple Pay"]

rows = []
oid = 100000
for i in range(N_CUSTOMERS):
    cid = f"CUST{1000 + i}"
    engagement = rng.beta(2.0, 2.5)                      # 0..1 latent loyalty
    signup_offset = rng.integers(0, TOTAL_DAYS - 120)    # signs up before last ~4 months
    signup = START + pd.Timedelta(days=int(signup_offset))
    span_days = (SNAPSHOT - signup).days

    # active fraction of their possible lifetime — driven by engagement + noise
    active_frac = np.clip(engagement + rng.normal(0, 0.18), 0.05, 1.0)
    last_active = signup + pd.Timedelta(days=int(active_frac * span_days))

    # monthly order rate scales with engagement
    monthly_rate = 0.25 + 2.75 * engagement
    home_country = rng.choice(COUNTRIES, p=[.34, .18, .14, .12, .12, .10])
    home_payment = rng.choice(PAYMENTS, p=[.45, .30, .15, .10])

    # walk month by month from signup to last_active
    cur = signup
    n_orders = 0
    while cur <= last_active:
        k = rng.poisson(monthly_rate)
        for _ in range(k):
            day = cur + pd.Timedelta(days=int(rng.integers(0, 30)))
            if day > SNAPSHOT:
                continue
            cat = rng.choice(list(CATALOG.keys()))
            prod = rng.choice(CATALOG[cat])
            lo, hi = PRICES[cat]
            price = round(float(rng.uniform(lo, hi)), 2)
            qty = int(rng.integers(1, 4))
            country = home_country if rng.random() > 0.05 else rng.choice(COUNTRIES)
            payment = home_payment if rng.random() > 0.08 else rng.choice(PAYMENTS)
            rows.append([f"ORD{oid}", cid, day.strftime("%Y-%m-%d"), prod, cat,
                         price, qty, round(price * qty, 2), country, payment])
            oid += 1
            n_orders += 1
        cur += pd.Timedelta(days=30)

    # guarantee at least one historical order so the customer is learnable
    if n_orders == 0:
        day = signup + pd.Timedelta(days=int(rng.integers(0, max(1, span_days // 2))))
        cat = rng.choice(list(CATALOG.keys())); prod = rng.choice(CATALOG[cat])
        lo, hi = PRICES[cat]; price = round(float(rng.uniform(lo, hi)), 2)
        rows.append([f"ORD{oid}", cid, day.strftime("%Y-%m-%d"), prod, cat,
                     price, 1, price, home_country, home_payment])
        oid += 1

df = pd.DataFrame(rows, columns=["order_id", "customer_id", "order_date", "product_name",
                                 "category", "unit_price", "quantity", "total_amount",
                                 "country", "payment_method"])
# inject a little realistic messiness: a few missing countries/payments + dup rows
miss = rng.choice(df.index, size=int(0.015 * len(df)), replace=False)
df.loc[miss[:len(miss)//2], "country"] = np.nan
df.loc[miss[len(miss)//2:], "payment_method"] = np.nan
df = pd.concat([df, df.sample(40, random_state=SEED)], ignore_index=True)  # duplicates

df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)           # shuffle

import sys
out = sys.argv[1] if len(sys.argv) > 1 else "ecommerce_transactions.csv"
df.to_csv(out, index=False)
print(f"Wrote {out}: {len(df):,} rows, {df['customer_id'].nunique():,} customers")
