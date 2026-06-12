# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# ⚡ التنبؤ بالطلب على الطاقة (Energy Demand Forecasting — Time Series)
### مشروع C2 — مسار علم البيانات (Data Science Track) ⭐

---
## 🎯 المشكلة التجارية (Business Problem)
شركة كهرباء محتاجة **تتنبأ باستهلاك الطاقة (kWh) للساعات القادمة** عشان توازن الإنتاج والطلب —
نقص الإنتاج = انقطاع، وزيادته = هدر فلوس. تنبؤ دقيق بيوفّر ملايين ويمنع الانقطاعات.

**نوع المشكلة:** تنبؤ بسلسلة زمنية (Time Series Forecasting).

## 📦 ما الذي يثبته المشروع
تحليل السلاسل الزمنية · **التفكيك (Decomposition)** · اختبار الاستقرارية (ADF) · **ACF/PACF** ·
التقسيم الزمني الصحيح · **Holt-Winters** · **SARIMA** · المقارنة بخط أساس · تقييم التنبؤ.
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| مكونات السلسلة (Trend/Seasonality/Residual) | Hyndman — *Forecasting: P&P* (ch.3) | فهم بنية البيانات |
| **الاستقرارية + ADF test** | Hyndman (ch.9) | معظم الموديلات تتطلب سلسلة مستقرة |
| **ACF / PACF** | Hyndman (ch.9) | اختيار معاملات ARIMA (p, q) |
| التقسيم الزمني (لا تخلط الماضي بالمستقبل!) | Hyndman (ch.5) | أكبر غلطة في الـ time series |
| **Exponential Smoothing (Holt-Winters)** | Hyndman (ch.8) | تنبؤ قوي بالاتجاه والموسمية |
| **SARIMA** | Hyndman (ch.9) | الموديل الكلاسيكي الأقوى مع الموسمية |
| مقاييس التنبؤ (RMSE, MAE, MAPE) | Hyndman (ch.5) | مقارنة الموديلات |

> 🎯 **بيُستخدم في الواقع:** التنبؤ بالطلب الكهربائي، المبيعات، حركة المرور، الأسعار، أعداد الزوار.
""")

md("## 0️⃣ المكتبات")
code("""import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import warnings; warnings.filterwarnings('ignore')
plt.rcParams['figure.figsize'] = (12, 4)
print('ready ✓')""")

md("## 1️⃣ تحميل البيانات وتجهيز الفهرس الزمني")
code("""df = pd.read_csv('data/energy_consumption_data.csv', parse_dates=['timestamp'])
df = df.set_index('timestamp').sort_index()
y = df['consumption_kwh'].asfreq('h')          # تردد ساعي صريح
print('Points:', len(y), '| from', y.index.min(), 'to', y.index.max())
y.plot(title='Hourly Energy Consumption (kWh)'); plt.show()""",
stub="""df = pd.read_csv('data/energy_consumption_data.csv', parse_dates=['timestamp'])
# TODO: اجعل timestamp فهرساً، رتّب، واضبط التردد الساعي asfreq('h')
y = ...
y.plot(); plt.show()""")

md(r"""## 2️⃣ تفكيك السلسلة (Seasonal Decomposition)
نفصل السلسلة لـ: اتجاه (Trend) + موسمية (Seasonality, دورة 24 ساعة) + بواقي (Residual).""")
code("""dec = sm.tsa.seasonal_decompose(y, model='additive', period=24)
dec.plot(); plt.tight_layout(); plt.show()""")

md(r"""## 3️⃣ اختبار الاستقرارية (ADF) و ACF/PACF
- **ADF test:** لو p-value < 0.05 → السلسلة مستقرة.
- **ACF/PACF:** بيساعدونا نختار معاملات SARIMA.""")
code("""from statsmodels.tsa.stattools import adfuller
p_adf = adfuller(y.dropna())[1]
print(f'ADF p-value = {p_adf:.4f}', '→ مستقرة ✓' if p_adf < 0.05 else '→ غير مستقرة (نحتاج differencing)')
fig, ax = plt.subplots(1, 2, figsize=(13, 3))
sm.graphics.tsa.plot_acf(y.dropna(), lags=48, ax=ax[0])
sm.graphics.tsa.plot_pacf(y.dropna(), lags=48, ax=ax[1])
plt.tight_layout(); plt.show()""",
stub="""from statsmodels.tsa.stattools import adfuller
# TODO: نفّذ adfuller واطبع الـ p-value، وارسم ACF و PACF (lags=48)
p_adf = ...
print('ADF p-value:', p_adf)""")

md(r"""## 4️⃣ التقسيم الزمني (Train/Test Split) ⚠️
**ممنوع** الخلط العشوائي في السلاسل الزمنية! نختبر على **آخر** فترة (آخر 48 ساعة) فقط.""")
code("""h = 48                                    # أفق التنبؤ = يومين
train, test = y.iloc[:-h], y.iloc[-h:]
print('Train:', len(train), '| Test:', len(test))""",
stub="""h = 48
# TODO: train = كل البيانات عدا آخر h، test = آخر h ساعة
train, test = ...
print(len(train), len(test))""")

md("## 5️⃣ خط الأساس (Seasonal Naive Baseline)")
code("""# تنبؤ ساذج: قيمة نفس الساعة من اليوم السابق
naive = train.iloc[-24:].values
naive = np.resize(naive, h)
rmse = lambda a, b: np.sqrt(np.mean((np.array(a) - np.array(b))**2))
print(f'Seasonal-Naive RMSE = {rmse(test.values, naive):.2f}')""")

md("## 6️⃣ Holt-Winters (Exponential Smoothing)")
code("""from statsmodels.tsa.holtwinters import ExponentialSmoothing
hw = ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=24).fit()
hw_fc = hw.forecast(h)
print(f'Holt-Winters RMSE = {rmse(test.values, hw_fc.values):.2f}')""",
stub="""from statsmodels.tsa.holtwinters import ExponentialSmoothing
# TODO: درّب ExponentialSmoothing (trend+seasonal, period=24) وتنبّأ بـ h خطوة
hw = ...
hw_fc = ...
print('HW RMSE:', rmse(test.values, hw_fc.values))""")

md("## 7️⃣ SARIMA (Seasonal ARIMA)")
code("""sarima = sm.tsa.SARIMAX(train, order=(1,0,1), seasonal_order=(1,1,1,24),
                        enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
sar_fc = sarima.forecast(h)
print(f'SARIMA RMSE = {rmse(test.values, sar_fc.values):.2f}')""",
stub="""# TODO: درّب SARIMAX بـ order=(1,0,1), seasonal_order=(1,1,1,24) وتنبّأ
sarima = ...
sar_fc = ...
print('SARIMA RMSE:', rmse(test.values, sar_fc.values))""")

md(r"""## 8️⃣ Prophet (اختياري — لو مثبّت)
Prophet (من Meta) سهل وقوي مع الموسميات المتعددة. الكود محاط بـ try/except عشان ما يكسرش النوتبوك لو مش مثبّت.""")
code("""try:
    from prophet import Prophet
    pdf = train.reset_index(); pdf.columns = ['ds', 'y']
    pm = Prophet(daily_seasonality=True).fit(pdf)
    fut = pm.make_future_dataframe(periods=h, freq='h')
    pf = pm.predict(fut)['yhat'].iloc[-h:].values
    print(f'Prophet RMSE = {rmse(test.values, pf):.2f}')
except Exception as e:
    print('Prophet not installed — skip. (pip install prophet)')""")

md("## 9️⃣ مقارنة التنبؤات بصرياً")
code("""plt.figure(figsize=(13,4))
plt.plot(train.index[-72:], train.iloc[-72:], label='history', color='gray')
plt.plot(test.index, test, label='actual', color='black', lw=2)
plt.plot(test.index, hw_fc, label='Holt-Winters', ls='--')
plt.plot(test.index, sar_fc, label='SARIMA', ls='--')
plt.legend(); plt.title('48-hour Energy Forecast'); plt.show()""")

md(r"""## 🔟 الخلاصة والتوصيات (Conclusion)
- **النتيجة:** Holt-Winters و SARIMA تفوّقا بوضوح على خط الأساس الساذج في التنبؤ بـ 48 ساعة.
- **الموسمية:** الدورة اليومية (24 ساعة) هي أقوى إشارة — لازم أي موديل يلتقطها.
- **التقسيم الزمني:** اختبرنا على المستقبل فقط (بدون خلط) — التقييم واقعي.
- **التوصية:** استخدام SARIMA/Holt-Winters للتنبؤ قصير المدى، مع إعادة تدريب يومية بالبيانات الجديدة.
- **الخطوة القادمة:** إضافة متغيّرات خارجية (الحرارة، العطلات) كـ SARIMAX exog، أو موديل ML بميزات زمنية.

> ✅ **اللي اتعلمته:** التفكيك، الاستقرارية، ACF/PACF، التقسيم الزمني، Holt-Winters، SARIMA، والتقييم.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "c2_timeseries_forecast")
