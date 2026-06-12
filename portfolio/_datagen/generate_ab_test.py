# -*- coding: utf-8 -*-
"""
A/B test dataset: e-commerce checkout redesign experiment.
Group A = control (old page), Group B = treatment (new page).
True conversion: A=0.118, B=0.132 (a real but modest +1.4pp lift).
Revenue per converting user ~ Gamma. Includes device segment.
"""
import numpy as np
import pandas as pd
import sys

rng = np.random.default_rng(7)
N = 24000
P_A, P_B = 0.118, 0.132

group = rng.choice(["A", "B"], size=N, p=[0.5, 0.5])
device = rng.choice(["mobile", "desktop"], size=N, p=[0.62, 0.38])

p = np.where(group == "A", P_A, P_B)
# mild device effect: desktop converts a bit better
p = p + np.where(device == "desktop", 0.015, -0.009)
p = np.clip(p, 0.01, 0.99)
converted = (rng.random(N) < p).astype(int)

# revenue only for converters
revenue = np.where(converted == 1, np.round(rng.gamma(shape=2.2, scale=26.0, size=N), 2), 0.0)

start = pd.Timestamp("2024-03-01")
ts = start + pd.to_timedelta(rng.integers(0, 14 * 24 * 60, size=N), unit="m")

df = pd.DataFrame({
    "user_id": [f"U{200000+i}" for i in range(N)],
    "timestamp": ts.sort_values().values,
    "group": group,
    "device": device,
    "converted": converted,
    "revenue": revenue,
})

out = sys.argv[1] if len(sys.argv) > 1 else "ab_test_data.csv"
df.to_csv(out, index=False)
print(f"Wrote {out}: {len(df):,} rows")
print(df.groupby("group")["converted"].mean())
