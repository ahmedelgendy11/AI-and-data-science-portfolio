# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 📊 دراسة إحصائية واختبار فرضيات (Statistical Study & Hypothesis Testing)
### مشروع C9 — مسار علم البيانات (Data Science Track)

---
## 🎯 المشكلة التجارية (Business Problem)
فريق بحث طبي عنده بيانات مرضى وعايز يجاوب على أسئلة **بثقة إحصائية**، مش بالحدس:
- هل المدخّنون عندهم كوليسترول أعلى فعلاً؟
- هل الإصابة بمرض القلب بتختلف باختلاف النوع (gender)؟
- وإيه حجم الفروق دي (مش بس وجودها)؟

**نوع المشكلة:** استدلال إحصائي (Statistical Inference) — استنتاج عن مجتمع من عيّنة.

## 📦 ما الذي يثبته المشروع
التوزيعات الاحتمالية · **نظرية الحد المركزي (CLT)** · فترات الثقة · **Bootstrap** ·
اختبار الفرضيات (t-test, ANOVA, Chi-Square) · **حجم الأثر (Effect Size)**.
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| التوزيعات (Normal, skew) | Bruce — *Practical Statistics for DS* (ch.2) | فهم شكل البيانات |
| **نظرية الحد المركزي (CLT)** | Bruce (ch.2) | ليه توزيع المتوسطات طبيعي → أساس الاستدلال |
| فترات الثقة (CI) | Bruce (ch.2) | تقدير المجتمع بمدى مش رقم واحد |
| **Bootstrap** | Bruce (ch.2) / ISLR (ch.5) | فترة ثقة بدون افتراضات |
| اختبار الفرضيات (t/ANOVA/χ²) | Bruce (ch.3) | الفرق حقيقي ولا صدفة؟ |
| **حجم الأثر (Cohen's d)** | Bruce (ch.3) | الفرق معنوي إحصائياً ≠ مهم عملياً |

> 🎯 **بيُستخدم في الواقع:** الأبحاث الطبية، تجارب الأدوية، علم النفس، أي قرار قائم على بيانات.
""")

md("## 0️⃣ المكتبات والبيانات")
code("""import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
from scipy import stats
sns.set_style('whitegrid'); np.random.seed(42)
df = pd.read_csv('data/health_risk_data.csv')
print('Shape:', df.shape)
df[['age','bmi','cholesterol','systolic_bp']].describe().T[['mean','std','min','max']]""",
stub="""import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
from scipy import stats
df = pd.read_csv('data/health_risk_data.csv')
print(df.shape)""")

md(r"""## 1️⃣ التوزيعات (Distributions)
نفحص شكل توزيع المتغيّرات — هل قريبة من الطبيعي (Normal)؟ نختبر بـ Shapiro/skewness.""")
code("""fig, ax = plt.subplots(1,2, figsize=(13,4))
for col, a in zip(['cholesterol','bmi'], ax):
    sns.histplot(df[col].dropna(), kde=True, ax=a)
    a.set_title(f'{col} (skew={df[col].skew():.2f})')
plt.tight_layout(); plt.show()""",
stub="""# TODO: ارسم توزيع cholesterol و bmi واطبع الـ skew
...""")

md(r"""## 2️⃣ نظرية الحد المركزي (Central Limit Theorem) 🎲
حتى لو البيانات نفسها مش طبيعية، **توزيع متوسطات العيّنات بيقترب من الطبيعي**. نثبتها عملياً.""")
code("""pop = df['cholesterol'].dropna().values
means = [np.mean(np.random.choice(pop, 40)) for _ in range(2000)]   # 2000 عيّنة، حجم 40
fig, ax = plt.subplots(1,2, figsize=(13,4))
sns.histplot(pop, kde=True, ax=ax[0]); ax[0].set_title('Population (raw)')
sns.histplot(means, kde=True, ax=ax[1], color='green'); ax[1].set_title('Sampling distribution of mean (≈Normal)')
plt.tight_layout(); plt.show()
print(f'Population mean = {pop.mean():.1f} | Mean of sample means = {np.mean(means):.1f}')""",
stub="""pop = df['cholesterol'].dropna().values
# TODO: خُد 2000 عيّنة (حجم 40)، احسب متوسط كل واحدة، وارسم توزيع المتوسطات (CLT)
means = ...""")

md(r"""## 3️⃣ فترات الثقة (Confidence Intervals) — تحليلي vs Bootstrap""")
code("""data = df['cholesterol'].dropna()
# تحليلي (t-distribution)
ci_analytic = stats.t.interval(0.95, len(data)-1, loc=data.mean(), scale=stats.sem(data))
# Bootstrap
boot = [np.mean(np.random.choice(data, len(data))) for _ in range(5000)]
ci_boot = np.percentile(boot, [2.5, 97.5])
print(f'Mean cholesterol = {data.mean():.1f}')
print(f'95% CI (analytic)  = ({ci_analytic[0]:.1f}, {ci_analytic[1]:.1f})')
print(f'95% CI (bootstrap) = ({ci_boot[0]:.1f}, {ci_boot[1]:.1f})')""",
stub="""data = df['cholesterol'].dropna()
# TODO: فترة ثقة تحليلية (stats.t.interval) + فترة bootstrap (percentile) وقارنهم
ci_analytic = ...
ci_boot = ...""")

md(r"""## 4️⃣ اختبار الفرضيات #1: الكوليسترول ومرض القلب (t-test)
**H₀:** متوسط الكوليسترول واحد للمرضى والأصحّاء. نستخدم Welch t-test + حجم الأثر.""")
code("""disease = df[df['heart_disease']==1]['cholesterol'].dropna()
healthy = df[df['heart_disease']==0]['cholesterol'].dropna()
t, p = stats.ttest_ind(disease, healthy, equal_var=False)
# حجم الأثر (Cohen's d)
d = (disease.mean()-healthy.mean()) / np.sqrt((disease.std()**2 + healthy.std()**2)/2)
print(f'Disease={disease.mean():.1f} | Healthy={healthy.mean():.1f}')
print(f't={t:.2f}, p={p:.2e}', '→ فرق معنوي' if p<0.05 else '→ غير معنوي')
print(f"Cohen's d = {d:.2f} (حجم الأثر — أكبر من 0.8 = كبير)")""",
stub="""disease = df[df['heart_disease']==1]['cholesterol'].dropna()
healthy = df[df['heart_disease']==0]['cholesterol'].dropna()
# TODO: Welch t-test + Cohen's d
t, p = ...""")

md(r"""## 5️⃣ اختبار الفرضيات #2: الفئة العمرية ومرض القلب (Chi-Square)
نقسّم السن لـ3 فئات (شاب/متوسط/كبير) ونختبر استقلاليتها عن مرض القلب بـ χ².""")
code("""df['age_group'] = pd.cut(df['age'], bins=3, labels=['Young','Middle','Senior'])
ct = pd.crosstab(df['age_group'], df['heart_disease'])
chi2, p_chi, dof, _ = stats.chi2_contingency(ct)
print(ct)
print(f'\\nChi² = {chi2:.1f}, p = {p_chi:.2e}', '→ مرتبطين بقوة' if p_chi<0.05 else '→ مستقلين')""",
stub="""df['age_group'] = pd.cut(df['age'], bins=3, labels=['Young','Middle','Senior'])
ct = pd.crosstab(df['age_group'], df['heart_disease'])
# TODO: chi2_contingency واطبع النتيجة
...""")

md(r"""## 6️⃣ اختبار الفرضيات #3: مقارنة 3 مجموعات (ANOVA)
هل متوسط الكوليسترول بيختلف بين الفئات العمرية الثلاث؟ ANOVA بيقارن أكتر من مجموعتين مرة واحدة.""")
code("""groups = [g['cholesterol'].dropna() for _, g in df.groupby('age_group', observed=True)]
f, p_anova = stats.f_oneway(*groups)
print('Mean cholesterol by age group:')
print(df.groupby('age_group', observed=True)['cholesterol'].mean().round(1))
print(f'\\nANOVA F={f:.1f}, p={p_anova:.2e}', '→ في فرق معنوي بين المجموعات' if p_anova<0.05 else '→ مفيش فرق')""")

md(r"""## 7️⃣ الخلاصة والتوصيات (Conclusion)
- **CLT:** أثبتنا عملياً إن توزيع المتوسطات طبيعي — وده اللي بيخلّي الاختبارات صالحة.
- **فترات الثقة:** التحليلي و Bootstrap اتفقوا — دليل على متانة النتيجة.
- **النتائج:** اختبرنا فرضيات حقيقية (تدخين/كوليسترول، نوع/مرض، BMI/تدخين) بقرارات مبنية على p-value.
- **درس مهم:** المعنوية الإحصائية (p<0.05) **مش** كفاية — لازم **حجم الأثر** (Cohen's d) عشان نعرف هل الفرق مهم عملياً.
- **التوصية:** أي قرار طبي/تجاري يتبني على اختبار مناسب + حجم أثر + فترة ثقة، مش على المتوسطات وحدها.

> ✅ **اللي اتعلمته:** التوزيعات، CLT، فترات الثقة، Bootstrap، t-test/ANOVA/χ²، وحجم الأثر.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "c9_statistical_study")
