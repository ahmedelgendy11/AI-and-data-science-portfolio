# -*- coding: utf-8 -*-
"""B9 — التنبؤ بتكلفة التأمين (Insurance Cost Prediction)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "_datagen"))
from nbtools import NB

nb = NB()
DIR = os.path.dirname(__file__)
SLUG = "b9_insurance_cost"
PROJECT = "ml/b9_insurance_cost"

# ── Title ──
nb.md("# 🏥 التنبؤ بتكلفة التأمين الصحي\n**Insurance Cost Prediction**")

nb.cloud_setup(PROJECT)

# ── prereqs ──
nb.md("""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| الموضوع | المصدر المقترح |
|---|---|
| Linear Regression + Regularization | ISLR Ch.3 & Ch.6 / Géron Ch.4 |
| Feature Interactions | Géron Ch.2 |
| Gradient Boosting (XGBoost) | Géron Ch.7 |
| Regression Evaluation (RMSE, MAE, R²) | ISLR Ch.2 |

## 🎯 بيُستخدم في إيه (استخدام واقعي)
- **شركات التأمين** بتستخدم النماذج دي لتسعير البوالص بدقة.
- **Actuaries** بيحتاجوا يفهموا إيه العوامل اللي بترفع التكلفة (التدخين، السمنة، العمر).
- **فرق الـ underwriting** بتستخدم الموديل عشان تحدد المخاطر.""")

# ── imports ──
nb.code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['figure.dpi'] = 100""",
stub="""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['figure.dpi'] = 100""")

# ── 1. Load & EDA ──
nb.md("## 1️⃣ تحميل البيانات والاستكشاف (EDA)")

nb.code("""df = pd.read_csv("data/insurance.csv")
print("Shape:", df.shape)
print("\\nData types:")
print(df.dtypes)
print("\\nMissing values:", df.isnull().sum().sum())
print("\\nStatistics:")
df.describe().round(1)""",
stub="""# TODO: حمّل البيانات من data/insurance.csv
# اطبع الشكل، الأنواع، القيم الناقصة، والإحصائيات
df = pd.read_csv(_____)
df.describe()""")

nb.code("""fig, axes = plt.subplots(2, 3, figsize=(15, 9))

# Target distribution
axes[0, 0].hist(df["charges"], bins=30, color="#3498db", edgecolor="white")
axes[0, 0].set_title("توزيع تكلفة التأمين (charges)")
axes[0, 0].set_xlabel("Charges ($)")

# Age vs charges
axes[0, 1].scatter(df["age"], df["charges"], alpha=0.4, s=15, c=df["smoker"].map({"yes":"red","no":"#3498db"}))
axes[0, 1].set_title("العمر vs التكلفة (أحمر=مدخن)")
axes[0, 1].set_xlabel("Age")
axes[0, 1].set_ylabel("Charges")

# BMI vs charges
axes[0, 2].scatter(df["bmi"], df["charges"], alpha=0.4, s=15, c=df["smoker"].map({"yes":"red","no":"#3498db"}))
axes[0, 2].set_title("BMI vs التكلفة (أحمر=مدخن)")
axes[0, 2].set_xlabel("BMI")

# Smoker boxplot
df.boxplot(column="charges", by="smoker", ax=axes[1, 0])
axes[1, 0].set_title("التكلفة حسب التدخين")
plt.sca(axes[1, 0]); plt.xlabel("Smoker"); plt.ylabel("Charges")

# Children boxplot
df.boxplot(column="charges", by="children", ax=axes[1, 1])
axes[1, 1].set_title("التكلفة حسب عدد الأولاد")

# Region boxplot
df.boxplot(column="charges", by="region", ax=axes[1, 2])
axes[1, 2].set_title("التكلفة حسب المنطقة")

plt.suptitle("")
plt.tight_layout()
plt.savefig("data/eda_overview.png", dpi=120, bbox_inches="tight")
plt.show()""",
stub="""# TODO: ارسم 6 رسومات استكشافية (2x3)
# توزيع charges, age vs charges, bmi vs charges, boxplots لـ smoker/children/region
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
# أكمل...
plt.tight_layout()
plt.show()""")

# ── 2. Feature engineering ──
nb.md("## 2️⃣ هندسة الميزات (Feature Engineering)")

nb.code("""df["bmi_smoker"] = df["bmi"] * (df["smoker"] == "yes").astype(int)
df["age_sq"] = df["age"] ** 2
df["overweight"] = (df["bmi"] >= 30).astype(int)

print("New features added: bmi_smoker, age_sq, overweight")
print("Shape:", df.shape)
df.head()""",
stub="""# TODO: أضف ميزات جديدة:
# bmi_smoker = bmi * smoker (interaction)
# age_sq = age² (non-linearity)
# overweight = 1 لو bmi >= 30
df["bmi_smoker"] = _____
df["age_sq"] = _____
df["overweight"] = _____
df.head()""")

# ── 3. Preprocessing + split ──
nb.md("## 3️⃣ تجهيز البيانات والتقسيم")

nb.code("""target = "charges"
num_cols = ["age", "bmi", "children", "bmi_smoker", "age_sq", "overweight"]
cat_cols = ["sex", "smoker", "region"]

X = df[num_cols + cat_cols]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(drop="first", sparse_output=False), cat_cols)
])""",
stub="""# TODO: حدد الأعمدة العددية والفئوية
# اعمل train/test split (80/20)
# اعمل ColumnTransformer بـ StandardScaler للعددي و OneHotEncoder للفئوي
target = "charges"
num_cols = [___]
cat_cols = [___]
X = df[num_cols + cat_cols]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
preprocessor = ColumnTransformer([___])""")

# ── 4. Modeling ──
nb.md("## 4️⃣ تدريب ومقارنة النماذج")

nb.code("""models = {
    "Linear Regression": LinearRegression(),
    "Ridge (alpha=1)": Ridge(alpha=1),
    "Random Forest (200)": RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=4, random_state=42),
    "XGBoost": xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=4,
                                 random_state=42, verbosity=0),
}

results = []
best_score, best_name, best_pipe = -1, None, None

for name, model in models.items():
    pipe = Pipeline([("pre", preprocessor), ("model", model)])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    rmse = root_mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results.append({"Model": name, "RMSE": rmse, "MAE": mae, "R²": r2})
    if r2 > best_score:
        best_score, best_name, best_pipe = r2, name, pipe
    print(f"{name:25s}  RMSE={rmse:,.0f}  MAE={mae:,.0f}  R²={r2:.4f}")

results_df = pd.DataFrame(results).sort_values("R²", ascending=False)
print(f"\\n🏆 Best: {best_name} (R²={best_score:.4f})")""",
stub="""# TODO: درّب وقارن 5 نماذج: Linear, Ridge, RF, GBM, XGBoost
# كل واحد في Pipeline مع preprocessor
# قيّم بـ RMSE, MAE, R² على test set
models = {
    "Linear Regression": LinearRegression(),
    "Ridge (alpha=1)": Ridge(alpha=1),
    "Random Forest (200)": RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42),
    "XGBoost": xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=4, random_state=42, verbosity=0),
}
results = []
for name, model in models.items():
    pipe = Pipeline([("pre", preprocessor), ("model", model)])
    # أكمل...
    pass
""")

# ── 5. Evaluation ──
nb.md("## 5️⃣ تقييم النموذج الأفضل")

nb.code("""y_pred_best = best_pipe.predict(X_test)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Actual vs Predicted
axes[0].scatter(y_test, y_pred_best, alpha=0.4, s=15, color="#2ecc71")
mn, mx = y_test.min(), y_test.max()
axes[0].plot([mn, mx], [mn, mx], "r--", linewidth=2, label="Perfect fit")
axes[0].set_xlabel("Actual Charges ($)")
axes[0].set_ylabel("Predicted Charges ($)")
axes[0].set_title(f"Actual vs Predicted — {best_name}")
axes[0].legend()

# Residuals
residuals = y_test - y_pred_best
axes[1].hist(residuals, bins=30, color="#e74c3c", edgecolor="white", alpha=0.8)
axes[1].axvline(0, color="black", linestyle="--")
axes[1].set_title("توزيع الأخطاء (Residuals)")
axes[1].set_xlabel("Error ($)")

plt.tight_layout()
plt.savefig("data/evaluation.png", dpi=120, bbox_inches="tight")
plt.show()
print(f"Residual mean: ${residuals.mean():,.0f}, std: ${residuals.std():,.0f}")""",
stub="""# TODO: ارسم:
# 1) Actual vs Predicted scatter
# 2) Residuals histogram
# استخدم النموذج الأفضل
y_pred_best = best_pipe.predict(X_test)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
# أكمل...
plt.tight_layout()
plt.show()""")

# ── 6. Feature importance ──
nb.md("## 6️⃣ أهمية الميزات (Feature Importance)")

nb.code("""feature_names = num_cols + list(
    best_pipe.named_steps["pre"].transformers_[1][1].get_feature_names_out(cat_cols))

inner = best_pipe.named_steps["model"]
if hasattr(inner, "feature_importances_"):
    importances = inner.feature_importances_
    fi = pd.Series(importances, index=feature_names).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    fi.tail(10).plot.barh(ax=ax, color="#3498db")
    ax.set_title(f"Feature Importance — {best_name}")
    ax.set_xlabel("Importance")
    plt.tight_layout()
    plt.savefig("data/feature_importance.png", dpi=120, bbox_inches="tight")
    plt.show()
else:
    coefs = inner.coef_
    fi = pd.Series(np.abs(coefs), index=feature_names).sort_values(ascending=True)
    print("Top features (|coefficient|):")
    print(fi.tail(10).to_string())
""",
stub="""# TODO: اعرض أهم الميزات من النموذج الأفضل
# لو tree-based: feature_importances_
# لو linear: |coefficients|
# أكمل...
""")

# ── 7. Model comparison chart ──
nb.md("## 7️⃣ مقارنة النماذج")

nb.code("""fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(results_df))
bars = ax.bar(x, results_df["R²"], color=["#e74c3c" if n == best_name else "#3498db"
              for n in results_df["Model"]], edgecolor="white")
ax.set_xticks(x)
ax.set_xticklabels(results_df["Model"], rotation=25, ha="right")
ax.set_ylabel("R² Score")
ax.set_title("مقارنة أداء النماذج")
ax.set_ylim(results_df["R²"].min() - 0.05, 1.0)
for i, v in enumerate(results_df["R²"]):
    ax.text(i, v + 0.005, f"{v:.3f}", ha="center", fontweight="bold", fontsize=9)
plt.tight_layout()
plt.savefig("data/model_comparison.png", dpi=120, bbox_inches="tight")
plt.show()""",
stub="""# TODO: ارسم bar chart لمقارنة R² بين النماذج
# لوّن النموذج الأفضل بلون مختلف
fig, ax = plt.subplots(figsize=(10, 5))
# أكمل...
plt.show()""")

# ── 8. Summary ──
nb.md("## 8️⃣ الخلاصة والتوصيات")

nb.code("""print("=" * 50)
print("📊 ملخص النتائج")
print("=" * 50)
print(f"\\n🏆 أفضل نموذج: {best_name}")
print(f"   R² = {best_score:.4f}")
print(f"   RMSE = ${root_mean_squared_error(y_test, y_pred_best):,.0f}")
print(f"   MAE = ${mean_absolute_error(y_test, y_pred_best):,.0f}")
print(f"\\n📌 أهم العوامل المؤثرة على التكلفة:")
print("   1. التدخين (أكبر عامل بفارق كبير)")
print("   2. العمر (علاقة طردية)")
print("   3. BMI (خصوصاً للمدخنين — interaction)")
print("   4. عدد الأولاد")
print("\\n✅ التحليل اكتمل بنجاح!")""",
stub="""# TODO: اطبع ملخص نهائي
# أفضل نموذج، R², RMSE، أهم العوامل
print("ملخص النتائج:")
# أكمل...
""")

# ── Write ──
nb.write(DIR, SLUG)
