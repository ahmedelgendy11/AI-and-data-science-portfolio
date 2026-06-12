# -*- coding: utf-8 -*-
"""
Credit-card-style transaction dataset with RARE fraud (~1.5%) and learnable signal.
Fraud propensity rises with: high amount ratio, night hour, foreign, large distance,
many recent transactions. Heavy class imbalance -> use PR-AUC & precision@k.
"""
import numpy as np, pandas as pd, sys
rng = np.random.default_rng(99)
N = 20000

hour = rng.integers(0, 24, N)
amount = np.round(np.clip(rng.lognormal(3.4, 1.0, N), 1, 5000), 2)
hist_avg = np.round(np.clip(rng.lognormal(3.4, 0.5, N), 5, 800), 2)
amount_ratio = np.round(amount / hist_avg, 2)
account_age_days = rng.integers(5, 3000, N)
n_tx_24h = rng.poisson(3, N)
distance_km = np.round(np.clip(rng.exponential(8, N), 0, 4000), 1)
is_foreign = rng.choice([0, 1], N, p=[0.92, 0.08])
merchant = rng.choice(["grocery","electronics","travel","restaurant","online","atm","fuel"], N,
                      p=[.25,.12,.08,.18,.20,.07,.10])

z = (-8.2
     + 1.9 * np.log1p(amount_ratio)
     + 2.4 * is_foreign
     + 0.0035 * distance_km
     + 0.28 * n_tx_24h
     + 1.8 * ((hour < 5) | (hour == 23)).astype(float)
     + np.where(np.isin(merchant, ["online", "electronics", "travel"]), 0.8, 0.0)
     + rng.normal(0, 0.35, N))
p = 1 / (1 + np.exp(-z))
fraud = (rng.random(N) < p).astype(int)

df = pd.DataFrame({
    "transaction_id": [f"T{700000+i}" for i in range(N)],
    "hour": hour, "amount": amount, "hist_avg_amount": hist_avg, "amount_ratio": amount_ratio,
    "account_age_days": account_age_days, "n_tx_last_24h": n_tx_24h,
    "distance_from_home_km": distance_km, "is_foreign": is_foreign,
    "merchant_category": merchant, "is_fraud": fraud,
})
out = sys.argv[1] if len(sys.argv) > 1 else "fraud_data.csv"
df.to_csv(out, index=False)
print(f"Wrote {out}: {len(df)} rows | fraud rate = {df['is_fraud'].mean():.2%}")
