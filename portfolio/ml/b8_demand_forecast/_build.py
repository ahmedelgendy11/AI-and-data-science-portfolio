# -*- coding: utf-8 -*-
"""B8 — التنبؤ بالطلب على الطاقة باستخدام ML (Demand Forecasting with ML)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "_datagen"))
from nbtools import NB

nb = NB()
DIR = os.path.dirname(__file__)
SLUG = "b8_demand_forecast"
PROJECT = "ml/b8_demand_forecast"

# ── Title ──
nb.md("# ⚡ التنبؤ بالطلب على الطاقة باستخدام ML\n**Energy Demand Forecasting with Machine Learning**")

nb.cloud_setup(PROJECT, packages=["xgboost"])

# ── prereqs ──
nb.md("""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| الموضوع | المصدر المقترح |
|---|---|
| Time Series Feature Engineering (lags, rolling) | Hyndman Ch.5 / Géron Ch.15 |
| XGBoost / Gradient Boosting | Géron Ch.7 |
| Time Series Train/Test Split | Hyndman Ch.3 (لا تستخدم random split!) |
| Evaluation: RMSE, MAE, MAPE | Hyndman Ch.5 |

## 🎯 بيُستخدم في إيه (استخدام واقعي)
- **شركات الكهرباء** بتتنبأ بالطلب عشان تخطط الإنتاج وتتجنب الانقطاعات.
- **المصانع** بتستخدم forecasting عشان تحدد كمية المواد الخام المطلوبة.
- **الـ retail** بيتنبأ بالطلب عشان يدير المخزون ويمنع الـ out-of-stock.""")

# ── imports ──
nb.code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['figure.dpi'] = 100""",
stub="""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['figure.dpi'] = 100""")

# ── 1. Load & explore ──
nb.md("## 1️⃣ تحميل البيانات والاستكشاف")

nb.code("""df = pd.read_csv("data/energy_consumption_data.csv", parse_dates=["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)
print("Shape:", df.shape)
print("Date range:", df["timestamp"].min(), "->", df["timestamp"].max())
print("\\nColumns:", list(df.columns))
print(df.describe().round(1))
df.head()""",
stub="""# TODO: حمّل البيانات وحوّل timestamp لـ datetime ورتّب بالتاريخ
df = pd.read_csv("data/energy_consumption_data.csv", parse_dates=["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)
print("Shape:", df.shape)
df.head()""")

nb.code("""fig, axes = plt.subplots(3, 1, figsize=(14, 9), sharex=True)

axes[0].plot(df["timestamp"], df["consumption_kwh"], linewidth=0.5, color="#2ecc71")
axes[0].set_title("استهلاك الطاقة (kWh)")
axes[0].set_ylabel("kWh")

axes[1].plot(df["timestamp"], df["temperature_c"], linewidth=0.5, color="#e74c3c")
axes[1].set_title("درجة الحرارة")
axes[1].set_ylabel("°C")

axes[2].plot(df["timestamp"], df["humidity_pct"], linewidth=0.5, color="#3498db")
axes[2].set_title("نسبة الرطوبة")
axes[2].set_ylabel("%")

plt.tight_layout()
plt.savefig("data/timeseries_overview.png", dpi=120, bbox_inches="tight")
plt.show()""",
stub="""# TODO: ارسم 3 رسومات time series (consumption, temperature, humidity)
fig, axes = plt.subplots(3, 1, figsize=(14, 9), sharex=True)
# أكمل...
plt.tight_layout()
plt.show()""")

# ── 2. Feature engineering ──
nb.md("""## 2️⃣ هندسة الميزات الزمنية (Time Series Features)
**القاعدة الذهبية:** في السلاسل الزمنية، الميزات الأهم هي:
1. **Lag features** — قيم الماضي
2. **Rolling statistics** — متوسط/انحراف آخر N ساعة
3. **Calendar features** — الساعة، اليوم، الشهر""")

nb.code("""df["hour"] = df["timestamp"].dt.hour
df["dayofweek"] = df["timestamp"].dt.dayofweek
df["month"] = df["timestamp"].dt.month
df["is_weekend"] = (df["dayofweek"] >= 5).astype(int)

for lag in [1, 2, 3, 6, 12, 24]:
    df[f"lag_{lag}"] = df["consumption_kwh"].shift(lag)

for win in [3, 6, 12, 24]:
    df[f"rolling_mean_{win}"] = df["consumption_kwh"].shift(1).rolling(win).mean()
    df[f"rolling_std_{win}"] = df["consumption_kwh"].shift(1).rolling(win).std()

df = df.dropna().reset_index(drop=True)
print(f"Shape after features: {df.shape}")
print("New columns:", [c for c in df.columns if c not in ["timestamp", "consumption_kwh", "temperature_c", "humidity_pct", "is_holiday"]])""",
stub="""# TODO: أضف ميزات زمنية:
# 1) Calendar: hour, dayofweek, month, is_weekend
# 2) Lag features: lag_1, lag_2, ..., lag_24
# 3) Rolling: rolling_mean, rolling_std بأحجام نوافذ مختلفة
# ⚠️ مهم: shift(1) قبل الـ rolling عشان ما نسرّبش بيانات المستقبل!
df["hour"] = df["timestamp"].dt.hour
df["dayofweek"] = _____

for lag in [1, 2, 3, 6, 12, 24]:
    df[f"lag_{lag}"] = _____

# أكمل...
df = df.dropna().reset_index(drop=True)
print(f"Shape after features: {df.shape}")""")

# ── 3. Train/test split (temporal) ──
nb.md("""## 3️⃣ تقسيم البيانات (Temporal Split)
**⚠️ مهم جداً:** في السلاسل الزمنية، **ما بنستخدمش** `train_test_split` العشوائي!
بنقسّم **بالترتيب الزمني** — الأقدم للتدريب والأحدث للاختبار.""")

nb.code("""target = "consumption_kwh"
features = [c for c in df.columns if c not in [target, "timestamp"]]

split_idx = int(len(df) * 0.8)
train = df.iloc[:split_idx]
test = df.iloc[split_idx:]

X_train, y_train = train[features], train[target]
X_test, y_test = test[features], test[target]

print(f"Train: {len(train)} rows ({train['timestamp'].min().date()} -> {train['timestamp'].max().date()})")
print(f"Test:  {len(test)} rows ({test['timestamp'].min().date()} -> {test['timestamp'].max().date()})")""",
stub="""# TODO: قسّم البيانات 80/20 بالترتيب الزمني (مش عشوائي!)
# train = أول 80%، test = آخر 20%
target = "consumption_kwh"
features = [c for c in df.columns if c not in [target, "timestamp"]]

split_idx = int(len(df) * 0.8)
train = _____
test = _____
X_train, y_train = train[features], train[target]
X_test, y_test = test[features], test[target]
print(f"Train: {len(train)}, Test: {len(test)}")""")

# ── 4. Modeling ──
nb.md("## 4️⃣ تدريب ومقارنة النماذج")

nb.code("""models = {
    "Ridge": Ridge(alpha=1),
    "Random Forest": RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42),
    "XGBoost": xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=5,
                                 random_state=42, verbosity=0),
}

results = []
predictions = {}
best_score, best_name = -1, None

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    predictions[name] = y_pred

    rmse = root_mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    results.append({"Model": name, "RMSE": rmse, "MAE": mae, "R²": r2, "MAPE%": mape})
    if r2 > best_score:
        best_score, best_name = r2, name
    print(f"{name:20s}  RMSE={rmse:.1f}  MAE={mae:.1f}  R²={r2:.4f}  MAPE={mape:.1f}%")

results_df = pd.DataFrame(results).sort_values("R²", ascending=False)
print(f"\\n🏆 Best: {best_name} (R²={best_score:.4f})")""",
stub="""# TODO: درّب وقارن 3 نماذج: Ridge, Random Forest, XGBoost
# قيّم بـ RMSE, MAE, R², MAPE
models = {
    "Ridge": Ridge(alpha=1),
    "Random Forest": RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42),
    "XGBoost": xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=5,
                                 random_state=42, verbosity=0),
}
results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    # أكمل التقييم...
""")

# ── 5. Forecast visualization ──
nb.md("## 5️⃣ تصوير التنبؤات")

nb.code("""fig, ax = plt.subplots(figsize=(14, 5))
plot_df = test[["timestamp"]].copy()
plot_df["actual"] = y_test.values
plot_df["predicted"] = predictions[best_name]

ax.plot(plot_df["timestamp"], plot_df["actual"], label="Actual", linewidth=1, alpha=0.8)
ax.plot(plot_df["timestamp"], plot_df["predicted"], label=f"Predicted ({best_name})",
        linewidth=1, alpha=0.8, color="#e74c3c")
ax.set_title("الطلب الفعلي vs التنبؤ")
ax.set_xlabel("Time")
ax.set_ylabel("Consumption (kWh)")
ax.legend()
plt.tight_layout()
plt.savefig("data/forecast_plot.png", dpi=120, bbox_inches="tight")
plt.show()""",
stub="""# TODO: ارسم خط الطلب الفعلي وخط التنبؤ من أفضل نموذج
fig, ax = plt.subplots(figsize=(14, 5))
# أكمل...
plt.show()""")

# ── 6. Feature importance ──
nb.md("## 6️⃣ أهمية الميزات")

nb.code("""best_model = models[best_name]
if hasattr(best_model, "feature_importances_"):
    fi = pd.Series(best_model.feature_importances_, index=features).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 8))
    fi.tail(15).plot.barh(ax=ax, color="#3498db")
    ax.set_title(f"Top 15 Features — {best_name}")
    ax.set_xlabel("Importance")
    plt.tight_layout()
    plt.savefig("data/feature_importance.png", dpi=120, bbox_inches="tight")
    plt.show()

    print("\\nTop 5 features:")
    for feat, imp in fi.tail(5).items():
        print(f"  {feat:25s} {imp:.4f}")""",
stub="""# TODO: اعرض أهم 15 ميزة من أفضل نموذج
# أكمل...
""")

# ── 7. Time Series CV ──
nb.md("""## 7️⃣ التحقق بـ Time Series Cross-Validation
بنستخدم **TimeSeriesSplit** عشان نتأكد إن الأداء مش بالصدفة.""")

nb.code("""tscv = TimeSeriesSplit(n_splits=5)
best_model_fresh = xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=5,
                                     random_state=42, verbosity=0)

X_all, y_all = df[features], df[target]
cv_scores = cross_val_score(best_model_fresh, X_all, y_all, cv=tscv, scoring="r2")

print(f"Time Series CV (5-fold) — {best_name}:")
for i, s in enumerate(cv_scores):
    print(f"  Fold {i+1}: R² = {s:.4f}")
print(f"  Mean: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")""",
stub="""# TODO: استخدم TimeSeriesSplit (5 folds) لتقييم أفضل نموذج
from sklearn.model_selection import cross_val_score
tscv = TimeSeriesSplit(n_splits=5)
# أكمل...
""")

# ── 8. Summary ──
nb.md("## 8️⃣ الخلاصة")

nb.code("""print("=" * 50)
print("⚡ ملخص التنبؤ بالطلب على الطاقة")
print("=" * 50)
print(f"\\n🏆 أفضل نموذج: {best_name}")
print(f"   R²: {best_score:.4f}")
best_results = results_df[results_df["Model"] == best_name].iloc[0]
print(f"   RMSE: {best_results['RMSE']:.1f} kWh")
print(f"   MAPE: {best_results['MAPE%']:.1f}%")
print(f"\\n📌 أهم الملاحظات:")
print("   1. Lag features (خصوصاً lag_1, lag_24) هي الأهم — الاستهلاك القريب بيتنبأ بالقادم")
print("   2. الساعة من اليوم (hour) مهمة — patterns يومية واضحة")
print("   3. درجة الحرارة بتأثر على الاستهلاك (تكييف/تدفئة)")
print("   4. XGBoost بيتفوق على Linear models لأن العلاقات non-linear")
print("\\n✅ التحليل اكتمل بنجاح!")""",
stub="""# TODO: اطبع ملخص نهائي بالنتائج والملاحظات
print("ملخص التنبؤ بالطلب:")
# أكمل...
""")

# ── Write ──
nb.write(DIR, SLUG)
