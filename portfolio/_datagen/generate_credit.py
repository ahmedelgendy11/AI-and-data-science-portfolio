# -*- coding: utf-8 -*-
"""
Credit-risk / loan-default dataset with learnable, imbalanced signal (~18% default).
Default propensity is a logistic function of credit score, debt-to-income,
prior defaults, loan-to-income ratio, employment length (+ noise).
"""
import numpy as np, pandas as pd, sys
rng = np.random.default_rng(2024)
N = 8000

credit_score = np.clip(rng.normal(680, 75, N), 300, 850)
income = np.round(np.clip(rng.lognormal(10.9, 0.5, N), 15000, 400000), -2)
loan_amount = np.round(np.clip(income * rng.uniform(0.1, 0.9, N), 1000, 200000), -2)
loan_term = rng.choice([12, 24, 36, 48, 60], N, p=[.1, .2, .35, .2, .15])
emp_length = np.clip(rng.exponential(5, N), 0, 40).round(1)
dti = np.clip(rng.beta(2, 5, N) + loan_amount / (income + 1) * 0.3, 0.02, 0.95).round(3)
num_prior_defaults = rng.poisson(0.3, N).clip(0, 6)
home = rng.choice(["RENT", "MORTGAGE", "OWN"], N, p=[.45, .40, .15])
purpose = rng.choice(["debt_consolidation", "credit_card", "home_improvement",
                      "major_purchase", "medical", "small_business"], N,
                     p=[.35, .22, .15, .12, .08, .08])
interest_rate = np.round(np.clip(18 - (credit_score - 300) / 550 * 12 + rng.normal(0, 1.5, N), 4, 30), 2)
loan_to_income = loan_amount / (income + 1)

# ---- default propensity (logistic) ----
z = (-0.018 * (credit_score - 680)      # higher score -> lower risk
     + 3.2 * dti                         # higher debt burden -> higher risk
     + 0.55 * num_prior_defaults         # past defaults -> higher risk
     + 2.0 * loan_to_income              # borrowing too much vs income
     - 0.05 * emp_length                 # stable job -> lower risk
     + 0.08 * (interest_rate - 12)
     + np.where(home == "RENT", 0.25, 0.0)
     + rng.normal(0, 0.9, N))            # irreducible noise
p = 1 / (1 + np.exp(-(z - 4.0)))         # shift to ~18% base rate
default = (rng.random(N) < p).astype(int)

df = pd.DataFrame({
    "applicant_id": [f"A{50000+i}" for i in range(N)],
    "credit_score": credit_score.round().astype(int),
    "annual_income": income.astype(int),
    "loan_amount": loan_amount.astype(int),
    "loan_term_months": loan_term,
    "employment_length_yrs": emp_length,
    "debt_to_income": dti,
    "num_prior_defaults": num_prior_defaults,
    "home_ownership": home,
    "loan_purpose": purpose,
    "interest_rate": interest_rate,
    "default": default,
})
# realistic missingness
for col, frac in [("employment_length_yrs", 0.04), ("annual_income", 0.02)]:
    idx = rng.choice(df.index, int(frac * N), replace=False)
    df.loc[idx, col] = np.nan

out = sys.argv[1] if len(sys.argv) > 1 else "credit_risk_data.csv"
df.to_csv(out, index=False)
print(f"Wrote {out}: {len(df)} rows | default rate = {df['default'].mean():.1%}")
