# 📊 Statistical Study & Hypothesis Testing

> Answer real questions from patient data with statistical rigor — distributions, CLT, bootstrap, and the right hypothesis tests.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![scipy](https://img.shields.io/badge/scipy-stats-green) ![statistics](https://img.shields.io/badge/inference-CLT%20%2B%20bootstrap-blueviolet)

## 📌 Problem
A medical research team needs to answer questions ("is cholesterol higher in heart-disease patients?",
"is age related to heart disease?") with **statistical confidence**, not gut feeling.

## 🧠 Pipeline
1. **Distributions** — shape & skewness of clinical variables.
2. **Central Limit Theorem** — demonstrated empirically (sampling distribution of the mean ≈ normal).
3. **Confidence intervals** — analytic (t) **and** bootstrap (they agree → robust).
4. **t-test** — cholesterol: disease vs healthy, with **Cohen's d** effect size.
5. **Chi-square** — age group × heart disease (independence test).
6. **ANOVA** — cholesterol across 3 age groups.

## 📈 Results (this dataset)
| Test | Result |
|---|---|
| t-test (cholesterol, disease vs healthy) | t=32.3, p≈0, **Cohen's d = 1.47 (large)** |
| Chi-square (age group × disease) | χ²=710, p≈0 (strongly related) |
| ANOVA (cholesterol × age group) | F=845, p≈0 (significant) |

**Key lesson:** statistical significance (p<0.05) isn't enough — **effect size** tells you if the
difference actually *matters*.

## ▶️ Run
```bash
conda run -n dsportfolio jupyter notebook c9_statistical_study_solution.ipynb
```

## 🛠️ Skills demonstrated
`Distributions` · `Central Limit Theorem` · `Confidence intervals` · `Bootstrap` ·
`t-test / ANOVA / Chi-square` · `Effect size (Cohen's d)`
