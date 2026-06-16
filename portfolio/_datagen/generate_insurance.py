# -*- coding: utf-8 -*-
"""Generate realistic insurance cost dataset with clear signal."""
import numpy as np, pandas as pd, os

np.random.seed(42)
N = 1500

age = np.random.randint(18, 65, N)
sex = np.random.choice(["male", "female"], N)
bmi = np.round(np.random.normal(28, 6, N).clip(15, 55), 1)
children = np.random.choice([0, 1, 2, 3, 4, 5], N, p=[0.30, 0.25, 0.20, 0.13, 0.08, 0.04])
smoker = np.random.choice(["yes", "no"], N, p=[0.20, 0.80])
region = np.random.choice(["northeast", "northwest", "southeast", "southwest"], N)

charges = (
    250 * age
    + 200 * bmi
    + 500 * children
    + 20000 * (smoker == "yes").astype(float)
    + 150 * bmi * (smoker == "yes").astype(float)
    + np.where(sex == "male", 800, 0)
    + np.random.normal(0, 2500, N)
).clip(1000)
charges = np.round(charges, 2)

df = pd.DataFrame({
    "age": age, "sex": sex, "bmi": bmi, "children": children,
    "smoker": smoker, "region": region, "charges": charges
})

out = os.path.join(os.path.dirname(__file__), "..", "ml", "b9_insurance_cost", "data", "insurance.csv")
df.to_csv(out, index=False)
print(f"Wrote {len(df)} rows -> {out}")
print(df.describe().round(1))
