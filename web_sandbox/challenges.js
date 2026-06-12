// ═══════════════════════════════════════════════════════════════
//  CHALLENGES.JS — Challenge Definitions & Validation Logic
//  Interactive Data Science Web Sandbox (Ultimate Portfolio)
// ═══════════════════════════════════════════════════════════════

const CHALLENGES = {
  // ─────────────────────────────────────────────────────────────
  //  PROJECT 1: E-Commerce Analysis
  // ─────────────────────────────────────────────────────────────
  ecommerce: {
    name: "E-Commerce Analysis",
    icon: "🛒",
    dataset: "ecommerce_transactions.csv",
    challenges: [
      {
        id: "ec-1",
        title: "استكشاف البيانات",
        subtitle: "Data Exploration",
        description: "قم بتحميل ملف البيانات واستعرض شكل البيانات (shape)، أنواع الأعمدة (dtypes)، وأول 5 صفوف.",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/ecommerce_transactions.csv')
# TODO: Print shape, dtypes and head
print("Shape:", df.shape)
print("Dtypes:\n", df.dtypes)
print(df.head())`,
        hint: "استخدم df.shape و df.dtypes و df.head() لعرض معلومات الجدول.",
        validate: function(output) {
          return output.includes("Shape:") && output.includes("order_id");
        }
      },
      {
        id: "ec-2",
        title: "تنظيف التواريخ",
        subtitle: "Date Cleaning",
        description: "قم بتحويل عمود order_date إلى تنسيق datetime موحد باستخدام pd.to_datetime.",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/ecommerce_transactions.csv')
# TODO: Convert order_date to datetime
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', format='mixed')
print(df['order_date'].dtype)
print("NaT count:", df['order_date'].isna().sum())`,
        hint: "استخدم pd.to_datetime(df['order_date'], errors='coerce', format='mixed') للتحويل الموحد.",
        validate: function(output) {
          return output.toLowerCase().includes("datetime") && output.includes("NaT count:");
        }
      },
      {
        id: "ec-3",
        title: "حذف المكررات والقيم المفقودة",
        subtitle: "Duplicates & Missing Values",
        description: "قم بحذف الصفوف المكررة وإزالة التواريخ غير الصالحة (NaT) من عمود order_date.",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/ecommerce_transactions.csv')
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', format='mixed')
# TODO: Drop duplicates and NaT rows
df = df.drop_duplicates().dropna(subset=['order_date'])
print("Cleaned Shape:", df.shape)`,
        hint: "استخدم df.drop_duplicates() وحذف القيم الفارغة باستخدام dropna(subset=['order_date']).",
        validate: function(output) {
          return output.includes("Cleaned Shape:") && /\(\d+, \d+\)/.test(output);
        }
      },
      {
        id: "ec-4",
        title: "حساب مؤشرات RFM",
        subtitle: "RFM Calculation",
        description: "قم بحساب Recency و Frequency و Monetary لكل عميل.",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/ecommerce_transactions.csv')
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', format='mixed')
df = df.drop_duplicates().dropna(subset=['order_date'])
# TODO: Calculate RFM
max_date = df['order_date'].max()
rfm = df.groupby('customer_id').agg({
    'order_date': lambda x: (max_date - x.max()).days,
    'order_id': 'nunique',
    'total_amount': 'sum'
}).rename(columns={'order_date':'Recency', 'order_id':'Frequency', 'total_amount':'Monetary'})
print(rfm.head())`,
        hint: "استخدم groupby('customer_id') مع تجميع الأعمدة للتواريخ والمبيعات.",
        validate: function(output) {
          return output.includes("Recency") && output.includes("Frequency") && output.includes("Monetary");
        }
      },
      {
        id: "ec-5",
        title: "معدل الاحتفاظ بالعملاء",
        subtitle: "Cohort Retention",
        description: "احسب الشهر الذي طلب فيه كل عميل لأول مرة (Cohort Month).",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/ecommerce_transactions.csv')
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', format='mixed')
df = df.drop_duplicates().dropna(subset=['order_date'])
# TODO: Compute Cohort Month
df['order_month'] = df['order_date'].dt.to_period('M')
df['cohort_month'] = df.groupby('customer_id')['order_month'].transform('min')
print(df[['customer_id', 'order_month', 'cohort_month']].head())`,
        hint: "استخدم dt.to_period('M') للحصول على الشهر، ثم groupby مع transform('min').",
        validate: function(output) {
          return output.includes("order_month") && output.includes("cohort_month");
        }
      },
      {
        id: "ec-6",
        title: "موديل التنبؤ بالرحيل",
        subtitle: "Churn Prediction",
        description: "قم بتعريف Churn (عدم الشراء لـ 90 يوماً)، وتدريب موديل Logistic Regression لقياس الدقة.",
        starterCode: `import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load & Prep
df = pd.read_csv('/data/ecommerce_transactions.csv')
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', format='mixed')
df = df.drop_duplicates().dropna(subset=['order_date'])
max_date = df['order_date'].max()
rfm = df.groupby('customer_id').agg({
    'order_date': lambda x: (max_date - x.max()).days,
    'order_id': 'nunique',
    'total_amount': 'sum'
}).rename(columns={'order_date':'Recency', 'order_id':'Frequency', 'total_amount':'Monetary'})

# TODO: Create Target and fit LogisticRegression
rfm['Churn'] = (rfm['Recency'] > 90).astype(int)
X = rfm[['Frequency', 'Monetary']]
y = rfm['Churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)
acc = accuracy_score(y_test, model.predict(X_test))
print(f"Accuracy: {acc:.4f}")`,
        hint: "استخدم train_test_split و LogisticRegression و accuracy_score لحساب النسبة.",
        validate: function(output) {
          return output.includes("Accuracy:") && parseFloat(output.split("Accuracy:")[1]) > 0.5;
        }
      }
    ]
  },

  // ─────────────────────────────────────────────────────────────
  //  PROJECT 2: Health Risk & ML
  // ─────────────────────────────────────────────────────────────
  health: {
    name: "Health Risk & ML",
    icon: "🏥",
    dataset: "health_risk_data.csv",
    challenges: [
      {
        id: "he-1",
        title: "استكشاف البيانات الطبية",
        subtitle: "Medical Exploration",
        description: "افحص حجم البيانات وعدد القيم المفقودة في أعمدة bmi و cholesterol.",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/health_risk_data.csv')
# TODO: Print missing count per column
print(df[['bmi', 'cholesterol']].isna().sum())`,
        hint: "استخدم isna().sum() على الأعمدة المستهدفة.",
        validate: function(output) {
          return output.includes("bmi") && output.includes("cholesterol");
        }
      },
      {
        id: "he-2",
        title: "توحيد تصنيف البيانات",
        subtitle: "Categorical Standardization",
        description: "قم بتوحيد فئات عمود gender لتكون Male أو Female فقط.",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/health_risk_data.csv')
# TODO: Replace categorical inconsistencies
df['gender'] = df['gender'].replace({'M':'Male', 'male':'Male', 'F':'Female', 'female':'Female'})
print(df['gender'].value_counts())`,
        hint: "استخدم df['gender'].replace({...}) مع الفئات المقابلة.",
        validate: function(output) {
          return output.includes("Male") && output.includes("Female") && !output.includes(" F ");
        }
      },
      {
        id: "he-3",
        title: "علاج القيم المفقودة والتحجيم",
        subtitle: "Imputation & Scaling",
        description: "قم بملء القيم المفقودة باستخدام الوسيط (median) وتحجيم الأعمدة العددية.",
        starterCode: `import pandas as pd
from sklearn.preprocessing import StandardScaler
df = pd.read_csv('/data/health_risk_data.csv')
df['bmi'] = df['bmi'].fillna(df['bmi'].median())
# TODO: Scale features
scaler = StandardScaler()
df['scaled_bmi'] = scaler.fit_transform(df[['bmi']])
print("Mean:", round(df['scaled_bmi'].mean(), 2))
print("Std:", round(df['scaled_bmi'].std(), 2))`,
        hint: "استخدم StandardScaler و fit_transform لتحجيم عمود bmi.",
        validate: function(output) {
          return output.includes("Mean: -0.0") || output.includes("Mean: 0.0") && output.includes("Std: 1.0");
        }
      },
      {
        id: "he-4",
        title: "مقارنة موديلات التصنيف",
        subtitle: "Classification Battle",
        description: "قم بتدريب نموذج Logistic Regression ونموذج Random Forest، وقارن دقة كل منهما.",
        starterCode: `import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv('/data/health_risk_data.csv')
df['bmi'] = df['bmi'].fillna(df['bmi'].median())
X = df[['age', 'bmi']]
y = df['heart_disease']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TODO: Train LR and RF, print both accuracies
lr = LogisticRegression().fit(X_train, y_train)
rf = RandomForestClassifier(random_state=42).fit(X_train, y_train)
print("LR Accuracy:", accuracy_score(y_test, lr.predict(X_test)))
print("RF Accuracy:", accuracy_score(y_test, rf.predict(X_test)))`,
        hint: "استخدم accuracy_score لمقارنة مخرجات التوقع للموديلين.",
        validate: function(output) {
          return output.includes("LR Accuracy:") && output.includes("RF Accuracy:");
        }
      },
      {
        id: "he-5",
        title: "عصبون اصطناعي مفرد",
        subtitle: "Single Neuron scratch",
        description: "قم ببناء دالة التمرير الأمامي لعصبون اصطناعي مفرد بـ NumPy.",
        starterCode: `import numpy as np
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def forward(inputs, weights, bias):
    # TODO: Dot product and sigmoid
    return sigmoid(np.dot(inputs, weights) + bias)

inputs = np.array([25.0, 130.0])
weights = np.array([0.05, 0.02])
bias = -3.0
print("Neuron Output:", round(forward(inputs, weights, bias), 4))`,
        hint: "استخدم np.dot(inputs, weights) + bias لحساب مدخلات الخلية العصبية قبل الـ Sigmoid.",
        validate: function(output) {
          return output.includes("Neuron Output:") && output.includes("0.7006");
        }
      },
      {
        id: "he-6",
        title: "تدريب شبكة عصبية MLP",
        subtitle: "MLP Classifier",
        description: "قم بتدريب شبكة عصبية متعددة الطبقات (MLPClassifier) لتقييم المخاطر الطبية.",
        starterCode: `import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv('/data/health_risk_data.csv')
df['bmi'] = df['bmi'].fillna(df['bmi'].median())
X = df[['age', 'bmi', 'systolic_bp']]
y = df['heart_disease']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TODO: Train MLP Classifier
mlp = MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=200, random_state=42)
mlp.fit(X_train, y_train)
print("MLP Accuracy:", accuracy_score(y_test, mlp.predict(X_test)))`,
        hint: "استخدم MLPClassifier مع معاملات hidden_layer_sizes و max_iter وتدريبها عبر fit.",
        validate: function(output) {
          return output.includes("MLP Accuracy:");
        }
      }
    ]
  },

  // ─────────────────────────────────────────────────────────────
  //  PROJECT 3: Stock Market Analysis
  // ─────────────────────────────────────────────────────────────
  stock: {
    name: "Stock Market Analysis",
    icon: "📈",
    dataset: "stock_market_data.csv",
    challenges: [
      {
        id: "st-1",
        title: "حساب العوائد اليومية",
        subtitle: "Daily Returns",
        description: "احسب العوائد اليومية لسهم AAPL باستخدام pct_change().",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/stock_market_data.csv')
aapl = df[df['ticker'] == 'AAPL'].copy()
# TODO: Calculate daily_return
aapl['daily_return'] = aapl['close'].pct_change()
print("Mean Return:", round(aapl['daily_return'].mean(), 6))`,
        hint: "استخدم pct_change() على عمود سعر الإغلاق close.",
        validate: function(output) {
          return output.includes("Mean Return:");
        }
      },
      {
        id: "st-2",
        title: "حساب نسبة شارب",
        subtitle: "Sharpe Ratio",
        description: "احسب نسبة شارب السنوية لسهم AAPL (معدل خالي من المخاطر = 2% سنوياً).",
        starterCode: `import pandas as pd
import numpy as np
df = pd.read_csv('/data/stock_market_data.csv')
aapl = df[df['ticker'] == 'AAPL'].copy()
aapl['daily_return'] = aapl['close'].pct_change()
# TODO: Annualized Sharpe Ratio
rf_daily = 0.02 / 252
sharpe = (aapl['daily_return'].mean() - rf_daily) / aapl['daily_return'].std() * np.sqrt(252)
print("Sharpe Ratio:", round(sharpe, 4))`,
        hint: "المعادلة: (المتوسط اليومي - العائد خالي المخاطر اليومي) / الانحراف المعياري * جذر 252.",
        validate: function(output) {
          return output.includes("Sharpe Ratio:") && parseFloat(output.split("Sharpe Ratio:")[1]) > 0.0;
        }
      },
      {
        id: "st-3",
        title: "المتوسطات المتحركة ومؤشر RSI",
        subtitle: "Technical Indicators",
        description: "احسب المتوسط المتحرك البسيط لـ 20 يوماً لسعر إغلاق سهم AAPL.",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/stock_market_data.csv')
aapl = df[df['ticker'] == 'AAPL'].copy()
# TODO: Calculate 20-day SMA
aapl['SMA_20'] = aapl['close'].rolling(20).mean()
print("SMA_20 last values:\n", aapl['SMA_20'].tail())`,
        hint: "استخدم rolling(20).mean() على عمود close.",
        validate: function(output) {
          return output.includes("SMA_20 last values:");
        }
      },
      {
        id: "st-4",
        title: "تحديد اتجاه السعر للمستقبل",
        subtitle: "Target Variable Setup",
        description: "قم بإنشاء عمود Target يمثل صعود السهم لليوم التالي (1 صعود، 0 هبوط).",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/stock_market_data.csv')
aapl = df[df['ticker'] == 'AAPL'].copy()
# TODO: Define next-day Target
aapl['Target'] = (aapl['close'].shift(-1) > aapl['close']).astype(int)
print(aapl[['close', 'Target']].head())`,
        hint: "استخدم shift(-1) لمقارنة سعر إغلاق الغد بسعر اليوم.",
        validate: function(output) {
          return output.includes("Target") && output.includes("close");
        }
      },
      {
        id: "st-5",
        title: "التنبؤ باتجاه السوق الذكي",
        subtitle: "Market Trend Classifier",
        description: "قم بتدريب نموذج Random Forest للتنبؤ باتجاه السهم واعرض دقة النموذج.",
        starterCode: `import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv('/data/stock_market_data.csv')
aapl = df[df['ticker'] == 'AAPL'].copy()
aapl['SMA_20'] = aapl['close'].rolling(20).mean()
aapl['Target'] = (aapl['close'].shift(-1) > aapl['close']).astype(int)
aapl = aapl.dropna()

X = aapl[['open', 'high', 'low', 'close', 'volume', 'SMA_20']]
y = aapl['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TODO: Fit RandomForestClassifier and print accuracy
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
print("Accuracy:", accuracy_score(y_test, model.predict(X_test)))`,
        hint: "استخدم RandomForestClassifier لتدريب النموذج ومقارنة توقعاته مع y_test.",
        validate: function(output) {
          return output.includes("Accuracy:");
        }
      },
      {
        id: "st-6",
        title: "محاكاة التداول الخوارزمي",
        subtitle: "Algorithmic Backtesting",
        description: "احسب العوائد التراكمية لاستراتيجية تداول خوارزمية بسيطة تعتمد على إشارة الموديل.",
        starterCode: `import pandas as pd
import numpy as np
df = pd.read_csv('/data/stock_market_data.csv')
aapl = df[df['ticker'] == 'AAPL'].copy()
aapl['daily_return'] = aapl['close'].pct_change()
# Assume signal: buy on days where daily return > 0
aapl['Signal'] = (aapl['daily_return'] > 0).astype(int)
# TODO: Calculate Strategy Returns
aapl['strat_return'] = aapl['daily_return'] * aapl['Signal'].shift(1)
cum_return = (1 + aapl['strat_return'].fillna(0)).cumprod() - 1
print("Final Cum Return:", round(cum_return.iloc[-1], 4))`,
        hint: "اضرب العائد اليومي في إشارة اليوم السابق Signal.shift(1)، ثم احسب الضرب التراكمي cumprod().",
        validate: function(output) {
          return output.includes("Final Cum Return:");
        }
      }
    ]
  },

  // ─────────────────────────────────────────────────────────────
  //  PROJECT 4: Math for Data Science
  // ─────────────────────────────────────────────────────────────
  math: {
    name: "Math & Stats for DS",
    icon: "🧮",
    dataset: "stock_market_data.csv", // Reuse stock data or general calculations
    challenges: [
      {
        id: "ma-1",
        title: "حساب ضرب المصفوفات",
        subtitle: "Matrix Dot Product",
        description: "قم بحساب حاصل الضرب النقطي لمصفوفتين يدوياً ومقارنته بـ np.dot.",
        starterCode: `import numpy as np
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
# TODO: Calculate matrix multiplication manually or using np.dot
res = np.dot(A, B)
print("Result:\n", res)`,
        hint: "استخدم دالة np.dot(A, B) لحساب ضرب المصفوفات في NumPy.",
        validate: function(output) {
          return output.includes("19") && output.includes("43");
        }
      },
      {
        id: "ma-2",
        title: "حساب محدد المصفوفة والمعكوس",
        subtitle: "Determinant & Inverse",
        description: "احسب محدد (Determinant) ومعكوس مصفوفة 2x2.",
        starterCode: `import numpy as np
A = np.array([[1, 2], [3, 4]])
# TODO: Calculate Determinant & Inverse
det = np.linalg.det(A)
inv = np.linalg.inv(A)
print(f"Det: {round(det, 2)}")
print("Inverse:\n", inv)`,
        hint: "استخدم الدوال np.linalg.det() و np.linalg.inv() لتنفيذ العمليات المطلوبة.",
        validate: function(output) {
          return output.includes("Det: -2.0") && output.includes("-2.");
        }
      },
      {
        id: "ma-3",
        title: "خطوة الانحدار التدريجي",
        subtitle: "Gradient Descent Step",
        description: "قم بحساب تحديث المعامل x في خطوة واحدة للانحدار التدريجي لدالة التكلفة f(x) = x^2 - 4x.",
        starterCode: `x = 10.0
lr = 0.1
# f'(x) = 2*x - 4
# TODO: Compute gradient and next x value
grad = 2 * x - 4
x_next = x - lr * grad
print("Next x:", x_next)`,
        hint: "صيغة التحديث: x = x - (learning_rate * gradient) حيث المشتقة هي 2*x - 4.",
        validate: function(output) {
          return output.includes("Next x: 8.4");
        }
      },
      {
        id: "ma-4",
        title: "اختبار الفرضيات t-test",
        subtitle: "Hypothesis Testing (t-test)",
        description: "قم بإجراء اختبار t-test مستقل لمعرفة مدى تشابه مجموعتين إحصائياً.",
        starterCode: `import scipy.stats as stats
group1 = [23, 25, 28, 30, 21]
group2 = [31, 33, 29, 35, 34]
# TODO: Calculate ttest_ind and print p-value
t_stat, p_val = stats.ttest_ind(group1, group2)
print("p-value:", round(p_val, 6))`,
        hint: "استخدم دالة stats.ttest_ind(group1, group2) لحساب المعيار الإحصائي وقيمة p-value.",
        validate: function(output) {
          return output.includes("p-value:") && parseFloat(output.split("p-value:")[1]) < 0.05;
        }
      },
      {
        id: "ma-5",
        title: "حساب الإنتروبيا (Entropy)",
        subtitle: "Entropy Calculation",
        description: "احسب الإنتروبيا الرياضية لمتغير عشوائي ثنائي ذو احتمالية نجاح p=0.2.",
        starterCode: `import numpy as np
p = 0.2
q = 1 - p
# TODO: Calculate Entropy in bits
entropy = - (p * np.log2(p) + q * np.log2(q))
print("Entropy:", round(entropy, 4))`,
        hint: "الإنتروبيا تساوي: - (p * log2(p) + (1-p) * log2(1-p)).",
        validate: function(output) {
          return output.includes("Entropy: 0.7219");
        }
      },
      {
        id: "ma-6",
        title: "اختبار مربع كاي (Chi-Square)",
        subtitle: "Chi-Square Test",
        description: "قم بإجراء اختبار مربع كاي لمعرفة مدى استقلالية متغيرين فئويين.",
        starterCode: `import scipy.stats as stats
# Contingency table (e.g. gender vs preference)
obs = [[20, 30], [30, 15]]
# TODO: Calculate chi2 contingency
chi2, p, dof, ex = stats.chi2_contingency(obs)
print("p-value:", round(p, 4))`,
        hint: "استخدم دالة stats.chi2_contingency(obs) لتقييم علاقة الارتباط الإحصائية.",
        validate: function(output) {
          return output.includes("p-value:") && parseFloat(output.split("p-value:")[1]) < 0.05;
        }
      }
    ]
  },

  // ─────────────────────────────────────────────────────────────
  //  PROJECT 5: Customer Segmentation
  // ─────────────────────────────────────────────────────────────
  clustering: {
    name: "Customer Segmentation",
    icon: "👥",
    dataset: "customer_segmentation_data.csv",
    challenges: [
      {
        id: "cl-1",
        title: "استكشاف بيانات العملاء",
        subtitle: "Segmentation EDA",
        description: "قم بتحميل وعرض الإحصاءات العامة لجدول تقسيم العملاء.",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/customer_segmentation_data.csv')
print(df.describe())`,
        hint: "استخدم df.describe() لعرض متوسط السن والدخل السنوي للعملاء.",
        validate: function(output) {
          return output.includes("annual_income_k") && output.includes("mean");
        }
      },
      {
        id: "cl-2",
        title: "تحجيم ميزات العملاء",
        subtitle: "Feature Standardization",
        description: "قم بتحجيم ميزات السن والدخل والإنفاق باستخدام StandardScaler.",
        starterCode: `import pandas as pd
from sklearn.preprocessing import StandardScaler
df = pd.read_csv('/data/customer_segmentation_data.csv')
X = df[['age', 'annual_income_k', 'spending_score_1_100']]
# TODO: Scale features
X_scaled = StandardScaler().fit_transform(X)
print("Scaled Shape:", X_scaled.shape)`,
        hint: "استخدم StandardScaler().fit_transform() على ميزات التجميع.",
        validate: function(output) {
          return output.includes("Scaled Shape: (1000, 3)");
        }
      },
      {
        id: "cl-3",
        title: "تطبيق خوارزمية K-Means",
        subtitle: "K-Means Clustering",
        description: "قم بتجميع العملاء في 4 مجموعات (Clusters) وحساب القصور الذاتي (Inertia).",
        starterCode: `import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
df = pd.read_csv('/data/customer_segmentation_data.csv')
X_scaled = StandardScaler().fit_transform(df[['age', 'annual_income_k', 'spending_score_1_100']])
# TODO: Apply KMeans with k=4
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
kmeans.fit(X_scaled)
print("Inertia:", round(kmeans.inertia_, 2))`,
        hint: "استخدم KMeans(n_clusters=4) مع ضبط n_init لحساب الانضغاط (Inertia).",
        validate: function(output) {
          return output.includes("Inertia:");
        }
      },
      {
        id: "cl-4",
        title: "درجة السلوهيت (Silhouette)",
        subtitle: "Silhouette Score",
        description: "احسب درجة Silhouette لتقييم جودة المجموعات المكتشفة.",
        starterCode: `import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
df = pd.read_csv('/data/customer_segmentation_data.csv')
X_scaled = StandardScaler().fit_transform(df[['age', 'annual_income_k', 'spending_score_1_100']])
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)
# TODO: Calculate silhouette score
score = silhouette_score(X_scaled, labels)
print("Silhouette Score:", round(score, 4))`,
        hint: "استخدم silhouette_score(X_scaled, labels) لتقييم تباعد وتقارب العناقيد.",
        validate: function(output) {
          return output.includes("Silhouette Score:");
        }
      },
      {
        id: "cl-5",
        title: "تقليل الأبعاد باستخدام PCA",
        subtitle: "PCA Dimensionality Reduction",
        description: "قم بتقليل أبعاد ميزات العملاء إلى بعدين (2 Components) للرسم ثنائي الأبعاد.",
        starterCode: `import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
df = pd.read_csv('/data/customer_segmentation_data.csv')
X_scaled = StandardScaler().fit_transform(df[['age', 'annual_income_k', 'spending_score_1_100']])
# TODO: Apply PCA with 2 components
pca = PCA(n_components=2)
pca_res = pca.fit_transform(X_scaled)
print("PCA shape:", pca_res.shape)`,
        hint: "استخدم PCA(n_components=2).fit_transform() لتقليل عدد الأبعاد.",
        validate: function(output) {
          return output.includes("PCA shape: (1000, 2)");
        }
      },
      {
        id: "cl-6",
        title: "تحليل خصائص المجموعات",
        subtitle: "Cluster Profiling",
        description: "احسب متوسط خصائص العملاء (السن، الدخل، الإنفاق) لكل مجموعة.",
        starterCode: `import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
df = pd.read_csv('/data/customer_segmentation_data.csv')
X_scaled = StandardScaler().fit_transform(df[['age', 'annual_income_k', 'spending_score_1_100']])
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)
# TODO: Calculate average characteristics per cluster
profiles = df.groupby('Cluster')[['age', 'annual_income_k', 'spending_score_1_100']].mean()
print(profiles)`,
        hint: "استخدم groupby('Cluster') ثم دالة mean() على الأعمدة الثلاثة الديموغرافية.",
        validate: function(output) {
          return output.includes("annual_income_k") && output.includes("spending_score_1_100") && output.includes("3 ");
        }
      }
    ]
  },

  // ─────────────────────────────────────────────────────────────
  //  PROJECT 6: House Prices Regression
  // ─────────────────────────────────────────────────────────────
  regression: {
    name: "House Prices Regression",
    icon: "🏠",
    dataset: "house_prices_data.csv",
    challenges: [
      {
        id: "re-1",
        title: "الالتواء والتحويل اللوغاريتمي",
        subtitle: "Target Skewness Correction",
        description: "قم بحساب التحويل اللوغاريتمي لسعر العقار sale_price باستخدام np.log1p.",
        starterCode: `import pandas as pd
import numpy as np
df = pd.read_csv('/data/house_prices_data.csv')
# TODO: Add log_price to dataframe
df['log_price'] = np.log1p(df['sale_price'])
print("Original skew:", round(df['sale_price'].skew(), 2))
print("Log skew:", round(df['log_price'].skew(), 2))`,
        hint: "استخدم np.log1p() لتحويل دالة السعر وتوزيعها بشكل طبيعي متماثل.",
        validate: function(output) {
          return output.includes("Original skew:") && output.includes("Log skew:");
        }
      },
      {
        id: "re-2",
        title: "علاج القيم المفقودة بالحي",
        subtitle: "Neighborhood Imputation",
        description: "املأ القيم المفقودة في المساحة square_footage بمتوسط المساحة لنفس الحي السكني.",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/house_prices_data.csv')
print("Null count before:", df['square_footage'].isna().sum())
# TODO: Fill missing square_footage with neighborhood median
df['square_footage'] = df.groupby('neighborhood')['square_footage'].transform(lambda x: x.fillna(x.median()))
print("Null count after:", df['square_footage'].isna().sum())`,
        hint: "استخدم groupby مع transform للتعويض بالقيمة الممثلة للحي السكني.",
        validate: function(output) {
          return output.includes("Null count before: 45") && output.includes("Null count after: 0");
        }
      },
      {
        id: "re-3",
        title: "الترميز الرقمي (One-Hot Encoding)",
        subtitle: "One-Hot Categorical Encoding",
        description: "قم بترميز الأعمدة الفئوية مثل neighborhood باستخدام pd.get_dummies.",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/house_prices_data.csv')
# TODO: One-hot encode the dataframe
df_encoded = pd.get_dummies(df, columns=['neighborhood'], drop_first=True)
print("Columns after encoding:", [c for c in df_encoded.columns if "neighborhood" in c])`,
        hint: "استخدم pd.get_dummies(df, columns=['neighborhood'], drop_first=True).",
        validate: function(output) {
          return output.includes("neighborhood_Suburbs") && output.includes("neighborhood_Uptown");
        }
      },
      {
        id: "re-4",
        title: "خوارزميات الانحدار المنتظم",
        subtitle: "Regularized Regression Battle",
        description: "قم بتدريب نموذج Ridge Regression ونموذج Lasso، وقارن معامل تحديد R2 لكل منهما.",
        starterCode: `import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import r2_score

df = pd.read_csv('/data/house_prices_data.csv')
df['square_footage'] = df['square_footage'].fillna(df['square_footage'].median())
X = pd.get_dummies(df[['square_footage', 'bedrooms', 'bathrooms', 'neighborhood']], drop_first=True)
y = df['sale_price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TODO: Fit Ridge and Lasso, calculate R2
ridge = Ridge().fit(X_train, y_train)
lasso = Lasso(max_iter=2000).fit(X_train, y_train)
print("Ridge R2:", round(r2_score(y_test, ridge.predict(X_test)), 4))
print("Lasso R2:", round(r2_score(y_test, lasso.predict(X_test)), 4))`,
        hint: "قم بتدريب Ridge و Lasso وحساب دقة التنبؤ لكل منهما باستخدام r2_score.",
        validate: function(output) {
          return output.includes("Ridge R2:") && output.includes("Lasso R2:");
        }
      },
      {
        id: "re-5",
        title: "توليف المعاملات للغابة العشوائية",
        subtitle: "GridSearchCV Tuning",
        description: "استخدم GridSearchCV للبحث عن أفضل المعاملات الفائقة لنموذج RandomForestRegressor.",
        starterCode: `import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('/data/house_prices_data.csv')
df['square_footage'] = df['square_footage'].fillna(df['square_footage'].median())
X = pd.get_dummies(df[['square_footage', 'bedrooms', 'bathrooms']], drop_first=True)
y = df['sale_price']

# TODO: Run GridSearchCV
grid = GridSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_grid={'n_estimators': [10, 30], 'max_depth': [5, 10]},
    cv=3
)
grid.fit(X, y)
print("Best params:", grid.best_params_)`,
        hint: "استخدم GridSearchCV مع ضبط param_grid و fit للبحث والتقييم.",
        validate: function(output) {
          return output.includes("Best params:") && output.includes("n_estimators");
        }
      },
      {
        id: "re-6",
        title: "حساب نسبة الخطأ التربيعية RMSE",
        subtitle: "RMSE Evaluation",
        description: "احسب جذر متوسط الخطأ التربيعي (RMSE) لنموذج التنبؤ بأسعار المنازل.",
        starterCode: `import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

df = pd.read_csv('/data/house_prices_data.csv')
df['square_footage'] = df['square_footage'].fillna(df['square_footage'].median())
X = pd.get_dummies(df[['square_footage', 'bedrooms', 'bathrooms']], drop_first=True)
y = df['sale_price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TODO: Fit RF and print RMSE
rf = RandomForestRegressor(random_state=42).fit(X_train, y_train)
rmse = np.sqrt(mean_squared_error(y_test, rf.predict(X_test)))
print("RMSE:", round(rmse, 2))`,
        hint: "استخدم np.sqrt(mean_squared_error(y_test, predictions)) لحساب نسبة الانحراف الفعلي.",
        validate: function(output) {
          return output.includes("RMSE:");
        }
      }
    ]
  },

  // ─────────────────────────────────────────────────────────────
  //  PROJECT 7: NLP Sentiment Analysis
  // ─────────────────────────────────────────────────────────────
  nlp: {
    name: "NLP Review Sentiment",
    icon: "💬",
    dataset: "product_reviews_data.csv",
    challenges: [
      {
        id: "nl-1",
        title: "استكشاف أطوال المراجعات",
        subtitle: "Review Text Length EDA",
        description: "احسب عدد الكلمات في كل مراجعة لتحديد أطوال نصوص مراجعات العملاء.",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/product_reviews_data.csv')
# TODO: Calculate review text length in words
df['word_count'] = df['review_text'].apply(lambda x: len(str(x).split()))
print("Mean words:", round(df['word_count'].mean(), 2))`,
        hint: "استخدم apply() مع دالة lambda x: len(x.split()) لحساب الكلمات.",
        validate: function(output) {
          return output.includes("Mean words:");
        }
      },
      {
        id: "nl-2",
        title: "تنظيف النصوص البدائي",
        subtitle: "Basic Text Cleansing",
        description: "قم بتحويل نص المراجعة بالكامل لحروف صغيرة وتنظيف الرموز الخاصة.",
        starterCode: `import pandas as pd
import re
df = pd.read_csv('/data/product_reviews_data.csv')
# TODO: Clean text (lowercase & remove symbols)
def clean(text):
    return re.sub(r'[^a-zA-Z\s]', '', text.lower())

df['clean_text'] = df['review_text'].apply(clean)
print("Cleaned review snippet:", df['clean_text'].iloc[0])`,
        hint: "استخدم re.sub() مع نمط الحروف الإنجليزية والمسافات لاستبدال الرموز الأخرى.",
        validate: function(output) {
          return output.includes("Cleaned review snippet:") && !/[^a-z\s]/.test(output.split("Cleaned review snippet:")[1].trim());
        }
      },
      {
        id: "nl-3",
        title: "تحويل النصوص مصفوفة TF-IDF",
        subtitle: "TF-IDF Vectorization",
        description: "قم بتحويل نصوص المراجعات إلى مصفوفة سمات رقمية تعتمد على أهمية الكلمات TF-IDF.",
        starterCode: `import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
df = pd.read_csv('/data/product_reviews_data.csv')
# TODO: Extract TF-IDF Matrix
vec = TfidfVectorizer(stop_words='english')
X = vec.fit_transform(df['review_text'])
print("Vocabulary size:", len(vec.vocabulary_))`,
        hint: "استخدم TfidfVectorizer(stop_words='english') مع دالة fit_transform.",
        validate: function(output) {
          return output.includes("Vocabulary size:") && parseInt(output.split("Vocabulary size:")[1]) > 10;
        }
      },
      {
        id: "nl-4",
        title: "مصنف Naive Bayes للنصوص",
        subtitle: "Naive Bayes Classifier",
        description: "قم بتدريب نموذج Multinomial Naive Bayes لتصنيف آراء العملاء.",
        starterCode: `import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

df = pd.read_csv('/data/product_reviews_data.csv')
X = TfidfVectorizer(stop_words='english').fit_transform(df['review_text'])
y = df['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TODO: Fit MultinomialNB
model = MultinomialNB()
model.fit(X_train, y_train)
print("NB Accuracy:", accuracy_score(y_test, model.predict(X_test)))`,
        hint: "استخدم MultinomialNB() وقم بتدريبه وحساب النسبة دقة التنبؤ.",
        validate: function(output) {
          return output.includes("NB Accuracy:") && parseFloat(output.split("NB Accuracy:")[1]) > 0.6;
        }
      },
      {
        id: "nl-5",
        title: "مصنف SVM المتقدم للنصوص",
        subtitle: "SVM Text Classifier",
        description: "قم بتدريب نموذج SVM (LinearSVC) لتصنيف النصوص ومقارنة دقته بالنموذج السابق.",
        starterCode: `import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score

df = pd.read_csv('/data/product_reviews_data.csv')
X = TfidfVectorizer(stop_words='english').fit_transform(df['review_text'])
y = df['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TODO: Fit LinearSVC
model = LinearSVC(random_state=42)
model.fit(X_train, y_train)
print("SVM Accuracy:", accuracy_score(y_test, model.predict(X_test)))`,
        hint: "استخدم LinearSVC(random_state=42) للمقارنة المباشرة مع Naive Bayes.",
        validate: function(output) {
          return output.includes("SVM Accuracy:") && parseFloat(output.split("SVM Accuracy:")[1]) > 0.7;
        }
      },
      {
        id: "nl-6",
        title: "مصفوفة اللخبطة والتحليل النهائي",
        subtitle: "NLP Confusion Matrix",
        description: "قم بحساب وطباعة مصفوفة اللخبطة (Confusion Matrix) لتقييم مصنف SVM.",
        starterCode: `import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix

df = pd.read_csv('/data/product_reviews_data.csv')
X = TfidfVectorizer(stop_words='english').fit_transform(df['review_text'])
y = df['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearSVC(random_state=42).fit(X_train, y_train)

# TODO: Get Confusion Matrix
cm = confusion_matrix(y_test, model.predict(X_test))
print("Confusion Matrix:\n", cm)`,
        hint: "استخدم confusion_matrix(y_test, predictions) لطباعة المصفوفة الفئوية.",
        validate: function(output) {
          return output.includes("Confusion Matrix:") && output.includes("[[");
        }
      }
    ]
  },

  // ─────────────────────────────────────────────────────────────
  //  PROJECT 8: Time Series Forecasting
  // ─────────────────────────────────────────────────────────────
  timeseries: {
    name: "Time Series Forecasting",
    icon: "⚡",
    dataset: "energy_consumption_data.csv",
    challenges: [
      {
        id: "ts-1",
        title: "رسم واختبار استقرار البيانات",
        subtitle: "ADF Stationarity Test",
        description: "أجرِ اختبار Dickey-Fuller لتحديد مدى استقرار السلسلة الزمنية إحصائياً.",
        starterCode: `import pandas as pd
from statsmodels.tsa.stattools import adfuller
df = pd.read_csv('/data/energy_consumption_data.csv')
# TODO: Perform ADF Test
res = adfuller(df['consumption_kwh'])
print("ADF Statistic:", round(res[0], 4))
print("p-value:", round(res[1], 6))`,
        hint: "استخدم دالة adfuller(df['consumption_kwh']) لمراجعة قيمة p-value إحصائياً.",
        validate: function(output) {
          return output.includes("ADF Statistic:") && output.includes("p-value:");
        }
      },
      {
        id: "ts-2",
        title: "تفكيك السلسلة للاتجاه والموسمية",
        subtitle: "Seasonal Decompose",
        description: "قم بفصل مكونات السلسلة الزمنية إلى اتجاه وموسمية (فترة 24 ساعة).",
        starterCode: `import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
df = pd.read_csv('/data/energy_consumption_data.csv')
# TODO: Perform seasonal decompose
decomp = seasonal_decompose(df['consumption_kwh'], period=24)
print("Trend Head:\n", decomp.trend.head(30))`,
        hint: "استخدم seasonal_decompose(df['consumption_kwh'], period=24) لاستخراج الترند العام.",
        validate: function(output) {
          return output.includes("Trend Head:") && output.includes("NaN");
        }
      },
      {
        id: "ts-3",
        title: "تقسيم عينات التدريب والاختبار",
        subtitle: "Time-based Train/Test Split",
        description: "قم بفصل السلسلة الزمنية لعينتي تدريب واختبار (90% تدريب، 10% اختبار).",
        starterCode: `import pandas as pd
df = pd.read_csv('/data/energy_consumption_data.csv')
# TODO: Time Series Split
train_size = int(len(df) * 0.9)
train = df['consumption_kwh'].iloc[:train_size]
test = df['consumption_kwh'].iloc[train_size:]
print("Train size:", len(train))
print("Test size:", len(test))`,
        hint: "استخدم استقطاع المصفوفات iloc بالاعتماد على معامل train_size.",
        validate: function(output) {
          return output.includes("Train size: 1800") && output.includes("Test size: 200");
        }
      },
      {
        id: "ts-4",
        title: "نموذج التمهيد الأسي هولت-وينترز",
        subtitle: "Holt-Winters Smoothing",
        description: "قم بتدريب نموذج Exponential Smoothing ذو الموسمية والاتجاه التراكمي.",
        starterCode: `import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
df = pd.read_csv('/data/energy_consumption_data.csv')
train = df['consumption_kwh'].iloc[:1800]
# TODO: Fit HW Exponential Smoothing
es = ExponentialSmoothing(train, seasonal_periods=24, trend='add', seasonal='add').fit()
print("Forecasted 5 steps:\n", es.forecast(5))`,
        hint: "استخدم ExponentialSmoothing مع معاملات trend='add' و seasonal='add' وتمرير fit.",
        validate: function(output) {
          return output.includes("Forecasted 5 steps:");
        }
      },
      {
        id: "ts-5",
        title: "نموذج ARIMA للتنبؤ",
        subtitle: "ARIMA Forecasting Model",
        description: "قم بتدريب نموذج ARIMA(1, 0, 1) وتوقع استهلاك الطاقة القادم.",
        starterCode: `import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
df = pd.read_csv('/data/energy_consumption_data.csv')
train = df['consumption_kwh'].iloc[:1800]
# TODO: Fit ARIMA model
model = ARIMA(train, order=(1, 0, 1)).fit()
print("ARIMA Forecast:\n", model.forecast(5))`,
        hint: "استخدم ARIMA(train, order=(1, 0, 1)).fit() لحساب تقديرات التنبؤ.",
        validate: function(output) {
          return output.includes("ARIMA Forecast:");
        }
      },
      {
        id: "ts-6",
        title: "حساب دقة التنبؤ RMSE",
        subtitle: "Forecasting RMSE Evaluation",
        description: "احسب دقة توقعات نموذج Holt-Winters بمقارنتها ببيانات الاختبار عبر RMSE.",
        starterCode: `import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error

df = pd.read_csv('/data/energy_consumption_data.csv')
train = df['consumption_kwh'].iloc[:1800]
test = df['consumption_kwh'].iloc[1800:]
model = ExponentialSmoothing(train, seasonal_periods=24, trend='add', seasonal='add').fit()
preds = model.forecast(len(test))

# TODO: Compute RMSE
rmse = np.sqrt(mean_squared_error(test, preds))
print("RMSE:", round(rmse, 2))`,
        hint: "استخدم np.sqrt(mean_squared_error(test, predictions)) لقياس متوسط الخطأ بالـ kWh.",
        validate: function(output) {
          return output.includes("RMSE:") && parseFloat(output.split("RMSE:")[1]) < 300.0;
        }
      }
    ]
  },

  // ─────────────────────────────────────────────────────────────
  //  PROJECT 9: SQL Mastery
  // ─────────────────────────────────────────────────────────────
  sql: {
    name: "SQL Database Mastery",
    icon: "🗄️",
    dataset: "company_database.db",
    challenges: [
      {
        id: "sq-1",
        title: "الاتصال واستعراض الجداول",
        subtitle: "List DB Tables",
        description: "اكتب استعلام SQL لاستعراض كافة أسماء الجداول المتواجدة في قاعدة البيانات.",
        starterCode: `import sqlite3
import pandas as pd
conn = sqlite3.connect('/data/company_database.db')
# TODO: Query sqlite_master for table names
q = "SELECT name FROM sqlite_master WHERE type='table';"
print(pd.read_sql_query(q, conn))
conn.close()`,
        hint: "استعلم من جدول sqlite_master حيث type='table' لاستكشاف محتويات قاعدة البيانات.",
        validate: function(output) {
          return output.includes("departments") && output.includes("employees") && output.includes("sales");
        }
      },
      {
        id: "sq-2",
        title: "إجمالي المبيعات للموظفين",
        subtitle: "Sales Aggregation & JOIN",
        description: "اكتب استعلام SQL لحساب إجمالي مبيعات كل موظف مرتبة تنازلياً مع دمج الاسم.",
        starterCode: `import sqlite3
import pandas as pd
conn = sqlite3.connect('/data/company_database.db')
# TODO: Join employees and sales, group by name and sum amount
q = '''
SELECT e.name, SUM(s.amount) as total_sales
FROM employees e
JOIN sales s ON e.emp_id = s.emp_id
GROUP BY e.emp_id
ORDER BY total_sales DESC;
'''
print(pd.read_sql_query(q, conn))
conn.close()`,
        hint: "استخدم INNER JOIN بين employees و sales مع تجميع البيانات GROUP BY وحساب SUM(amount).",
        validate: function(output) {
          return output.includes("total_sales") && output.includes("Omar");
        }
      },
      {
        id: "sq-3",
        title: "متوسط الرواتب بالأقسام",
        subtitle: "Average Salary per Dept",
        description: "احسب متوسط راتب الموظفين في كل قسم إداري.",
        starterCode: `import sqlite3
import pandas as pd
conn = sqlite3.connect('/data/company_database.db')
# TODO: Join employees and departments, group by dept_name, calculate avg salary
q = '''
SELECT d.dept_name, AVG(e.salary) as avg_salary
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
GROUP BY d.dept_id;
'''
print(pd.read_sql_query(q, conn))
conn.close()`,
        hint: "استخدم JOIN مع التجميع لحساب متوسط الراتب AVG(salary).",
        validate: function(output) {
          return output.includes("dept_name") && output.includes("avg_salary");
        }
      },
      {
        id: "sq-4",
        title: "ترتيب الموظفين بالدوال التحليلية",
        subtitle: "ROW_NUMBER() Window Function",
        description: "استخدم دالة ROW_NUMBER() لترتيب رواتب الموظفين داخل كل قسم تنازلياً.",
        starterCode: `import sqlite3
import pandas as pd
conn = sqlite3.connect('/data/company_database.db')
# TODO: Write query with ROW_NUMBER() OVER(PARTITION BY...)
q = '''
SELECT 
    name,
    dept_id,
    salary,
    ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY salary DESC) as salary_rank
FROM employees
'''
print(pd.read_sql_query(q, conn))
conn.close()`,
        hint: "الدالة: ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY salary DESC).",
        validate: function(output) {
          return output.includes("salary_rank") && output.includes("Layla");
        }
      },
      {
        id: "sq-5",
        title: "استعلام فرعي للمقارنة",
        subtitle: "Subquery Salary Comparison",
        description: "استعلم عن الموظفين الذين تزيد رواتبهم عن متوسط رواتب الشركة بأكملها.",
        starterCode: `import sqlite3
import pandas as pd
conn = sqlite3.connect('/data/company_database.db')
# TODO: Write query with subquery SELECT AVG(salary) FROM employees
q = '''
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
'''
print(pd.read_sql_query(q, conn))
conn.close()`,
        hint: "استخدم شرط WHERE salary > (SELECT AVG(salary) FROM employees).",
        validate: function(output) {
          return output.includes("Layla") && !output.includes("Fatima");
        }
      },
      {
        id: "sq-6",
        title: "الاستعلام المؤقت CTE المتقدم",
        subtitle: "Common Table Expression",
        description: "اكتب استعلاماً مؤقتاً (WITH CTE) لاستخراج الموظف الذي حقق أعلى مبيعات فردية.",
        starterCode: `import sqlite3
import pandas as pd
conn = sqlite3.connect('/data/company_database.db')
# TODO: Write query using WITH sales_cte AS (...)
q = '''
WITH sales_cte AS (
    SELECT emp_id, MAX(amount) as max_sale
    FROM sales
)
SELECT e.name, s.max_sale
FROM employees e
JOIN sales_cte s ON e.emp_id = s.emp_id;
'''
print(pd.read_sql_query(q, conn))
conn.close()`,
        hint: "استخدم WITH cte_name AS (SELECT ...) ثم استعلم من الجداول بالربط مع الـ CTE.",
        validate: function(output) {
          return output.includes("max_sale") && output.includes("Ahmad") || output.includes("Omar");
        }
      }
    ]
  },

  // ─────────────────────────────────────────────────────────────
  //  PROJECT 10: GenAI & RAG
  // ─────────────────────────────────────────────────────────────
  genai: {
    name: "GenAI & RAG",
    icon: "🤖",
    dataset: "product_reviews_data.csv",
    challenges: [
      {
        id: "ge-1",
        title: "تصميم أوامر النموذج اللغوي",
        subtitle: "Mock LLM Classification",
        description: "اكتب دالة تحاكي استجابة نموذج LLM لتصنيف مراجعة نصية بناءً على الأوامر.",
        starterCode: `def mock_llm_classify(review_text):
    # Prompt: Classify the sentiment of this review as Positive or Negative.
    # TODO: Perform mock classification logic based on keywords
    lower = review_text.lower()
    if 'love' in lower or 'great' in lower:
        return "Positive"
    elif 'worst' in lower or 'bad' in lower:
        return "Negative"
    return "Neutral"

print(mock_llm_classify("I love this smartwatch, it is great!"))`,
        hint: "افحص الكلمات المفتاحية بالدالة لمحاكاة التوقع المناسب للأمر.",
        validate: function(output) {
          return output.trim() === "Positive";
        }
      },
      {
        id: "ge-2",
        title: "استخلاص ميزات النصوص بالأمر",
        subtitle: "Mock LLM Keyword Extraction",
        description: "اكتب دالة تحاكي استدعاء LLM لاستخلاص الكلمات الدلالية الأساسية.",
        starterCode: `def mock_llm_keywords(review_text):
    # Prompt: Extract main product category mentioned in review.
    # TODO: Simple logic
    lower = review_text.lower()
    if 'chair' in lower:
        return "Furniture"
    elif 'blender' in lower:
        return "Appliances"
    return "Electronics"

print(mock_llm_keywords("The blender works average."))`,
        hint: "تأكد من أن الدالة تعيد الفئة الصحيحة عند وجود كلمات مفتاحية مثل blender.",
        validate: function(output) {
          return output.trim() === "Appliances";
        }
      },
      {
        id: "ge-3",
        title: "حساب تشابه الجيب بالـ NumPy",
        subtitle: "Cosine Similarity in NumPy",
        description: "احسب تشابه الجيب بين متجهين مُمثلين للنصوص رياضياً باستخدام NumPy.",
        starterCode: `import numpy as np
v1 = np.array([1, 2, 3])
v2 = np.array([2, 3, 4])
# TODO: Calculate cosine similarity = dot(v1, v2) / (norm(v1) * norm(v2))
cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
print("Similarity:", round(cos_sim, 6))`,
        hint: "تشابه الجيب يساوي حاصل الضرب النقطي مقسوماً على حاصل ضرب معياري المتجهين.",
        validate: function(output) {
          return output.includes("Similarity:") && output.includes("0.99258");
        }
      },
      {
        id: "ge-4",
        title: "استرجاع المستندات المتجهي",
        subtitle: "RAG Context Retrieval",
        description: "استخدم مصفوفة الجيب لاسترجاع المستند الأكثر ملاءمة للاستعلام.",
        starterCode: `import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = ["Get a laptop for fast coding.", "Smart watch with health features.", "Blender for kitchen use."]
query = "need a computer to write code"

# TODO: Fit Tfidf, calculate similarities and find top index
vec = TfidfVectorizer()
X = vec.fit_transform(docs)
q_vec = vec.transform([query])
sims = cosine_similarity(q_vec, X)[0]
best_idx = np.argmax(sims)
print("Best Match:", docs[best_idx])`,
        hint: "استخدم TfidfVectorizer لتحويل النصوص، ثم cosine_similarity، ثم np.argmax لاسترداد الفائز.",
        validate: function(output) {
          return output.includes("Best Match: Get a laptop for fast coding.");
        }
      },
      {
        id: "ge-5",
        title: "تغذية السياق للأمر الـ RAG",
        subtitle: "Context Feeding Template",
        description: "اكتب قالب صياغة الأمر المغذي بالسياق المسترجع للـ RAG.",
        starterCode: `context = "Product: Blender 3000. Price: $39.99. Rating: 4."
query = "What is the price of the blender?"

# TODO: Format prompt with context and query
prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
print(prompt)`,
        hint: "تأكد من أن المتغير prompt يحتوي على النصوص المدخلة من السياق والسؤال.",
        validate: function(output) {
          return output.includes("Price: $39.99") && output.includes("What is the price");
        }
      },
      {
        id: "ge-6",
        title: "تقييم مخرجات نماذج اللغة",
        subtitle: "LLM Output Evaluation",
        description: "احسب دقة تشابه جيب التمام لمخرجات النموذج المقترحة بالمخرجات الفعلية.",
        starterCode: `import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

actual = "The price of the blender is 39.99 dollars."
predicted = "Blender price is 39.99."

# TODO: Calculate cosine similarity of both strings
vec = TfidfVectorizer()
X = vec.fit_transform([actual, predicted])
sim = cosine_similarity(X[0], X[1])[0][0]
print("Eval Sim:", round(sim, 4))`,
        hint: "استخدم TfidfVectorizer و cosine_similarity لقياس التشابه البنائي للنصين.",
        validate: function(output) {
          return output.includes("Eval Sim:") && parseFloat(output.split("Eval Sim:")[1]) > 0.4;
        }
      }
    ]
  }
};
