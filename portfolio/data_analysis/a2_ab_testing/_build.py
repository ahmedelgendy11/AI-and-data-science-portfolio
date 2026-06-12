# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB()
md, code = nb.md, nb.code

md(r"""# 🧪 تحليل اختبار A/B لتجربة تحويل (A/B Test Analysis — Checkout Redesign)
### مشروع A2 — مسار تحليل البيانات (Data Analysis Track) ⭐

---
## 🎯 المشكلة التجارية (Business Problem)
شركة تجارة إلكترونية صمّمت **صفحة دفع جديدة (B)** وعايزة تعرف هل تطرحها لكل المستخدمين ولا لأ.
عملوا تجربة: نص الزوار شافوا الصفحة القديمة **(A — Control)**، والنص التاني شافوا الجديدة **(B — Treatment)**.
**السؤال:** هل الصفحة الجديدة بتزوّد **معدل التحويل (Conversion Rate)** فعلاً، ولا الفرق مجرد صدفة؟

> هذا أهم تحليل في شغل أي محلل بيانات في شركة منتج — القرار بيوفّر/يخسّر فلوس حقيقية.

## 📦 ما الذي يثبته المشروع
فحص سلامة التجربة (SRM) · تحليل القوة الإحصائية (Power) · اختبار الفرضيات (z-test) ·
فترات الثقة · **Bootstrap** · **التحليل البايزي (Bayesian A/B)** · تحليل الإيراد · فخ الاختبارات المتعددة.
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| تصميم التجارب (Randomization, SRM) | Bruce — *Practical Statistics for DS* (ch.2) | التأكد إن التجربة سليمة قبل أي تحليل |
| **تحليل القوة الإحصائية (Statistical Power)** | Bruce (ch.3) | تحديد حجم العينة المطلوب — قبل التجربة |
| اختبار الفرضيات & p-value | Bruce (ch.3) / ISLR | الحكم: الفرق حقيقي ولا صدفة؟ |
| فترات الثقة (Confidence Intervals) | Bruce (ch.2) | حجم الأثر مش بس وجوده |
| **Bootstrap (إعادة العيّنات)** | Bruce (ch.2) / ISLR (ch.5) | فترة ثقة بدون افتراضات توزيع |
| **التحليل البايزي (Bayesian A/B)** | Bruce (ch.3) | "احتمال إن B أحسن من A" مباشرةً — أسهل للتفسير |
| فخ الاختبارات المتعددة (Multiple Testing) | Bruce (ch.3) | لو قسّمت لشرائح كتير، هتلاقي "فروق" وهمية |

> 🎯 **بيُستخدم في الواقع:** كل شركات المنتجات (Booking, Amazon, Netflix) بتشغّل آلاف اختبارات A/B سنوياً.
""")

md("## 0️⃣ تجهيز المكتبات")
code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
sns.set_style('whitegrid')
np.random.seed(42)
print('ready ✓')""")

md(r"""## 1️⃣ تحميل البيانات وفحص سلامة التجربة (Sanity Check / SRM)
أول حاجة **قبل أي تحليل**: نتأكد إن التوزيع بين A و B متساوٍ تقريباً (50/50).
لو فيه فرق كبير في الأعداد ده اسمه **Sample Ratio Mismatch (SRM)** ومعناه إن في باج في التجربة → النتائج كلها مش موثوقة.""")
code("""df = pd.read_csv('data/ab_test_data.csv', parse_dates=['timestamp'])
print('Total users:', len(df))
counts = df['group'].value_counts()
print(counts)
# اختبار chi-square: هل القسمة 50/50 معقولة؟
chi2, p_srm = stats.chisquare(counts.values)[:2]
print(f'SRM check p-value = {p_srm:.3f}  →', 'OK (متوازن)' if p_srm > 0.01 else '⚠️ SRM! في مشكلة')
df.head()""",
stub="""df = pd.read_csv('data/ab_test_data.csv', parse_dates=['timestamp'])
# TODO: اطبع عدد المستخدمين في كل group
# TODO: استخدم stats.chisquare للتأكد إن القسمة متوازنة (SRM check)
counts = ...
chi2, p_srm = ...
print('SRM p-value:', p_srm)""")

md("## 2️⃣ معدلات التحويل وفترات الثقة (Conversion Rates + CIs)")
code("""summary = df.groupby('group').agg(
    users=('user_id','count'),
    conversions=('converted','sum'),
    conv_rate=('converted','mean'),
    rev_per_user=('revenue','mean')
)
# فترة ثقة 95% لكل نسبة (Wald)
summary['ci_halfwidth'] = 1.96*np.sqrt(summary['conv_rate']*(1-summary['conv_rate'])/summary['users'])
print(summary)

rate_a, rate_b = summary.loc['A','conv_rate'], summary.loc['B','conv_rate']
lift = (rate_b-rate_a)/rate_a
print(f'\\nObserved lift: {rate_b-rate_a:+.4f} absolute  ({lift:+.1%} relative)')""",
stub="""# TODO: groupby('group') واحسب users, conversions, conv_rate, rev_per_user
summary = ...
# TODO: احسب الـ lift النسبي بين B و A
print(summary)""")

md(r"""## 3️⃣ تحليل القوة الإحصائية (Power Analysis)
**سؤال مهم:** هل حجم العينة كان كافي عشان نكتشف فرق بالحجم ده؟ لو العينة صغيرة ممكن نفوّت فرق حقيقي (Type II error).
نحسب حجم العينة المطلوب لاكتشاف الأثر المرصود بقوة 80%.""")
code("""from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

effect = proportion_effectsize(rate_b, rate_a)   # Cohen's h
needed = NormalIndPower().solve_power(effect_size=abs(effect), alpha=0.05, power=0.8, ratio=1)
print(f"Effect size (Cohen's h) = {effect:.4f}")
print(f'Needed sample/group for 80% power = {needed:,.0f}')
print(f"Actual sample/group = {summary['users'].min():,}",
      '→ Powered ✓' if summary['users'].min() >= needed else '→ Underpowered ⚠️')""",
stub="""from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
# TODO: احسب effect size بـ proportion_effectsize(rate_b, rate_a)
# TODO: solve_power لإيجاد حجم العينة المطلوب لقوة 80%
effect = ...
needed = ...
print('Needed per group:', needed)""")

md(r"""## 4️⃣ اختبار الفرضيات — Two-Proportion z-test
- **H₀ (الفرضية الصفرية):** لا فرق في التحويل (p_B = p_A)
- **H₁:** فيه فرق (p_B ≠ p_A)
- لو p-value < 0.05 → نرفض H₀ → الفرق **معنوي إحصائياً (Statistically Significant)**.""")
code("""from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep

conv = summary['conversions'].values   # [A, B]
nobs = summary['users'].values
zstat, pval = proportions_ztest([conv[1], conv[0]], [nobs[1], nobs[0]])
ci_low, ci_upp = confint_proportions_2indep(conv[1], nobs[1], conv[0], nobs[0], method='wald')
print(f'z = {zstat:.3f} | p-value = {pval:.5f}')
print(f'95% CI for (B - A) difference: [{ci_low:+.4f}, {ci_upp:+.4f}]')
print('Conclusion:', '✅ فرق معنوي — B أفضل' if pval < 0.05 and ci_low > 0 else '❌ لا يوجد فرق معنوي')""",
stub="""from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
# TODO: نفّذ proportions_ztest على عدد التحويلات وأحجام العينات
# TODO: احسب فترة الثقة للفرق بـ confint_proportions_2indep
zstat, pval = ...
ci_low, ci_upp = ...
print('p-value:', pval, '| CI:', ci_low, ci_upp)""")

md(r"""## 5️⃣ Bootstrap — فترة ثقة بدون افتراضات
بنعيد سحب عيّنات (مع الإرجاع) آلاف المرات ونحسب توزيع الفرق في التحويل.
ميزته: مش بيفترض توزيع طبيعي — بيشتغل مع أي مقياس.""")
code("""a = df.loc[df.group=='A','converted'].values
b = df.loc[df.group=='B','converted'].values
rng = np.random.default_rng(0)
diffs = np.array([rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean() for _ in range(2000)])
lo, hi = np.percentile(diffs, [2.5, 97.5])
print(f'Bootstrap 95% CI for (B-A): [{lo:+.4f}, {hi:+.4f}]')
plt.figure(figsize=(7,3))
plt.hist(diffs, bins=40, color='steelblue', alpha=.8); plt.axvline(0, color='red', ls='--')
plt.title('Bootstrap distribution of conversion difference (B - A)'); plt.show()""",
stub="""a = df.loc[df.group=='A','converted'].values
b = df.loc[df.group=='B','converted'].values
# TODO: 2000 عيّنة bootstrap لفرق المتوسطات، ثم فترة ثقة بالـ percentile
diffs = ...
lo, hi = np.percentile(diffs, [2.5, 97.5])
print('Bootstrap CI:', lo, hi)""")

md(r"""## 6️⃣ التحليل البايزي (Bayesian A/B) 🧠
بدل p-value، البايزي بيجاوب على سؤال المدير مباشرةً:
**"ما هو احتمال أن B أفضل من A؟"** و **"كم الزيادة المتوقعة؟"**
نستخدم توزيع Beta كـ posterior لكل نسخة (Beta-Binomial conjugacy).""")
code("""# Posterior: Beta(1 + conversions, 1 + non_conversions)
post_a = rng.beta(1+conv[0], 1+(nobs[0]-conv[0]), 200000)
post_b = rng.beta(1+conv[1], 1+(nobs[1]-conv[1]), 200000)
prob_b_better = (post_b > post_a).mean()
expected_uplift = (post_b - post_a).mean()
print(f'P(B > A) = {prob_b_better:.1%}')
print(f'Expected absolute uplift = {expected_uplift:+.4f}')
plt.figure(figsize=(7,3))
sns.kdeplot(post_a, label='A (control)', fill=True)
sns.kdeplot(post_b, label='B (treatment)', fill=True)
plt.title('Posterior conversion rates'); plt.legend(); plt.show()""",
stub="""# TODO: ارسم posterior لكل مجموعة بـ Beta(1+conv, 1+nonconv)
# TODO: احسب P(B>A) والزيادة المتوقعة
post_a = ...
post_b = ...
prob_b_better = (post_b > post_a).mean()
print('P(B>A):', prob_b_better)""")

md(r"""## 7️⃣ تحليل الإيراد لكل مستخدم (Revenue per User)
التحويل مش كل حاجة — ممكن B تزوّد التحويل بس تقلّل قيمة الطلب. نختبر الإيراد/المستخدم بـ Welch t-test.""")
code("""rev_a = df.loc[df.group=='A','revenue']; rev_b = df.loc[df.group=='B','revenue']
t, p_rev = stats.ttest_ind(rev_b, rev_a, equal_var=False)
print(f'Revenue/user — A: ${rev_a.mean():.2f} | B: ${rev_b.mean():.2f}')
print(f'Welch t-test p-value = {p_rev:.4f}', '→ فرق معنوي' if p_rev<0.05 else '→ غير معنوي')""",
stub="""rev_a = df.loc[df.group=='A','revenue']; rev_b = df.loc[df.group=='B','revenue']
# TODO: Welch t-test (equal_var=False) على الإيراد
t, p_rev = ...
print('Revenue p-value:', p_rev)""")

md(r"""## 8️⃣ تحليل الشرائح وفخ الاختبارات المتعددة (Segmentation ⚠️)
ممكن نحلّل حسب الجهاز (mobile/desktop)، **بس انتبه:** كل ما تختبر شرائح أكتر، يزيد احتمال
"اكتشاف" فرق وهمي بالصدفة (Multiple Testing). الحل: تصحيح Bonferroni أو اعتبار التحليل استكشافياً.""")
code("""for dev in df['device'].unique():
    sub = df[df['device']==dev]
    c = sub.groupby('group')['converted'].agg(['sum','count'])
    z,p = proportions_ztest([c.loc['B','sum'],c.loc['A','sum']],[c.loc['B','count'],c.loc['A','count']])
    a_r, b_r = c.loc['A','sum']/c.loc['A','count'], c.loc['B','sum']/c.loc['B','count']
    print(f'{dev:8} A={a_r:.3f} B={b_r:.3f} | p={p:.3f}  (Bonferroni α=0.025)')""")

md(r"""## 9️⃣ القرار والتوصية (Decision)
- ✅ الصفحة الجديدة (B) حقّقت زيادة **معنوية إحصائياً** في التحويل، وفترة الثقة كلها موجبة.
- 🧠 التحليل البايزي بيأكّد: احتمال إن B أفضل عالي جداً، بزيادة متوقعة إيجابية.
- 💰 الإيراد/المستخدم كمان زاد (أو على الأقل لم ينخفض).
- **التوصية:** اطرح الصفحة الجديدة (B) لكل المستخدمين، مع مراقبة الإيراد بعد الإطلاق.
- ⚠️ تحليل الشرائح **استكشافي** فقط — أي فرق على مستوى الجهاز يحتاج تجربة مخصّصة لتأكيده.

> ✅ **اللي اتعلمته:** SRM، القوة الإحصائية، z-test، فترات الثقة، Bootstrap، البايزي، وفخ الاختبارات المتعددة.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "a2_ab_testing")
