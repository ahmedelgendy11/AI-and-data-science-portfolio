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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

df = pd.read_csv('/data/ecommerce_transactions.csv')


# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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

inputs = np.array([25.0, 130.0])
weights = np.array([0.05, 0.02])

# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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
rf_daily = 0.02 / 252

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
# f(x) = x^2 - 4x
# احسب المشتقة ثم طبّق خطوة التحديث
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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
obs = [[20, 30], [30, 15]]

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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
q = "SELECT name FROM sqlite_master WHERE type='table';"

# اكتب الحل هنا
`,
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
q = '''

# اكتب الحل هنا
`,
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
q = '''

# اكتب الحل هنا
`,
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
q = '''

# اكتب الحل هنا
`,
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
q = '''

# اكتب الحل هنا
`,
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
q = '''

# اكتب الحل هنا
`,
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
        starterCode: `
# اكتب الحل هنا
`,
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
        starterCode: `
# اكتب الحل هنا
`,
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

# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
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


# اكتب الحل هنا
`,
        hint: "استخدم TfidfVectorizer و cosine_similarity لقياس التشابه البنائي للنصين.",
        validate: function(output) {
          return output.includes("Eval Sim:") && parseFloat(output.split("Eval Sim:")[1]) > 0.4;
        }
      }
    ]
  }
};
