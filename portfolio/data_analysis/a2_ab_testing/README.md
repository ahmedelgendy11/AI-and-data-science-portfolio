# 🧪 A/B Test Analysis — Checkout Redesign

> Did the new checkout page actually increase conversion, or is it just noise? A full experimentation analysis: frequentist **and** Bayesian.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![statsmodels](https://img.shields.io/badge/statsmodels-stats-orange) ![scipy](https://img.shields.io/badge/scipy-tests-green)

## 📌 Problem
An e-commerce company A/B-tested a redesigned checkout page (B) against the old one (A).
The analysis decides whether to ship B — a decision with real revenue impact.

## 🧠 Analysis pipeline
1. **Sanity check (SRM)** — verify the 50/50 split before trusting anything.
2. **Conversion rates + 95% CIs** per group.
3. **Power analysis** — was the test large enough to detect the effect?
4. **Two-proportion z-test** — significance + CI of the difference.
5. **Bootstrap** — assumption-free CI (agrees with the z-test).
6. **Bayesian A/B** — `P(B > A)` and expected uplift, the way a PM wants it.
7. **Revenue per user** — Welch t-test (conversion ≠ revenue!).
8. **Segmentation** — by device, with the multiple-testing caveat.

## 📈 Results (this dataset)
| Metric | Result |
|---|---|
| Observed lift | **+1.23 pp (+10.4% relative)** |
| z-test p-value | **0.0038** (significant) |
| 95% CI (B−A) | [+0.004, +0.021] |
| Power | Adequately powered (11.9k/group > 11.2k needed) |
| Bayesian P(B>A) | **99.8%** |
| Revenue/user | higher for B but **not** significant (p=0.23) |

**Decision:** Ship B for conversion; keep monitoring revenue post-launch.

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook a2_ab_testing_solution.ipynb
```

## 🛠️ Skills demonstrated
`Experiment design` · `SRM` · `Statistical power` · `Hypothesis testing` · `Confidence intervals` ·
`Bootstrap` · `Bayesian inference` · `Multiple testing awareness`
