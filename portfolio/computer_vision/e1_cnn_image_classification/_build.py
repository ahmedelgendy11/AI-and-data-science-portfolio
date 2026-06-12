# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_datagen"))
from nbtools import NB

nb = NB(); md, code = nb.md, nb.code

md(r"""# 👕 تصنيف صور المنتجات بشبكة CNN (Image Classification with a CNN)
### مشروع E1 — مسار الرؤية الحاسوبية (Computer Vision Track) ⭐

---
## 🎯 المشكلة التجارية (Business Problem)
متجر إلكتروني بيرفع آلاف صور المنتجات يومياً ومحتاج **يصنّفها تلقائياً** (تيشيرت، شنطة، حذاء...)
بدل ما حد يكتب التصنيف بإيده. ده بيوفّر وقت ويخلّي الكتالوج منظّم وقابل للبحث.

**نوع المشكلة:** تصنيف صور متعدّد الفئات (Multi-class Image Classification) — 10 أنواع ملابس.

## 📦 ما الذي يثبته المشروع
بناء **شبكة التفاف (CNN)** من الصفر بـ Keras · المعالجة المسبقة للصور · طبقات Conv/Pool ·
منع overfitting (Dropout) · تقييم بصري + مصفوفة اللخبطة · قراءة منحنيات التدريب.
""")

md(r"""## 📚 قبل ما تبدأ — محتاج تذاكر إيه
| المفهوم | المصدر | بيُستخدم في إيه |
|---|---|---|
| الشبكات العصبية (طبقات، activation) | Géron — *Hands-On ML* (ch.10) | أساس أي شبكة |
| **طبقات الالتفاف (Convolution)** | Géron (ch.14) / Goodfellow (ch.9) | استخراج الأنماط البصرية (حواف، أشكال) |
| **التجميع (Pooling)** | Géron (ch.14) | تقليل الأبعاد والحفاظ على المهم |
| Softmax + Cross-Entropy | Géron (ch.10) | إخراج احتمالات للفئات المتعددة |
| Normalization للصور (÷255) | Géron (ch.14) | تثبيت التدريب وتسريعه |
| Dropout / Overfitting | Géron (ch.11) | منع الحفظ الأعمى للتدريب |
| منحنيات التدريب (Loss/Acc curves) | Géron (ch.10) | تشخيص: underfit ولا overfit؟ |

> 🎯 **بيُستخدم في الواقع:** فهرسة صور المنتجات، التشخيص الطبي بالأشعة، السيارات ذاتية القيادة، مراقبة الجودة في المصانع.
> 🛠️ **ملاحظة:** التدريب على CPU أبطأ — استخدمنا عدد epochs قليل. على GPU يبقى أسرع بكتير.
""")

md("## 0️⃣ المكتبات وتحميل البيانات (Fashion-MNIST)")
code("""import numpy as np, matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
tf.random.set_seed(42)
print('TensorFlow', tf.__version__)

(X_train, y_train), (X_test, y_test) = keras.datasets.fashion_mnist.load_data()
CLASSES = ['T-shirt','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle boot']
print('Train:', X_train.shape, '| Test:', X_test.shape)""",
stub="""import numpy as np, matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
tf.random.set_seed(42)
# TODO: حمّل Fashion-MNIST من keras.datasets
(X_train, y_train), (X_test, y_test) = ...
CLASSES = ['T-shirt','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle boot']
print(X_train.shape)""")

md("## 1️⃣ استكشاف الصور (EDA)")
code("""fig, axes = plt.subplots(2, 5, figsize=(11, 5))
for i, ax in enumerate(axes.flat):
    ax.imshow(X_train[i], cmap='gray'); ax.set_title(CLASSES[y_train[i]]); ax.axis('off')
plt.suptitle('Fashion-MNIST samples'); plt.tight_layout(); plt.show()
print('Pixel range:', X_train.min(), '-', X_train.max())
print('Class balance:', np.bincount(y_train))""")

md(r"""## 2️⃣ المعالجة المسبقة (Preprocessing)
- **تطبيع (Normalize):** نقسم على 255 → القيم بين 0 و 1 (تدريب أثبت).
- **إعادة التشكيل:** نضيف بُعد القناة (28×28 → 28×28×1) عشان طبقات الـ Conv.""")
code("""X_train = (X_train / 255.0).reshape(-1, 28, 28, 1).astype('float32')
X_test  = (X_test / 255.0).reshape(-1, 28, 28, 1).astype('float32')
print('Shape for CNN:', X_train.shape)""",
stub="""# TODO: طبّع الصور (÷255) وأعد تشكيلها لـ (-1,28,28,1)
X_train = ...
X_test  = ...
print(X_train.shape)""")

md(r"""## 3️⃣ بناء شبكة CNN (Model Architecture)
المعمارية: **Conv → Pool → Conv → Pool → Flatten → Dense → Dropout → Softmax**.
طبقات الالتفاف بتتعلّم أنماط بصرية (حواف ثم أشكال)، والـ pooling بيقلّل الحجم.""")
code("""model = keras.Sequential([
    layers.Input((28, 28, 1)),
    layers.Conv2D(32, 3, activation='relu', padding='same'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu', padding='same'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(10, activation='softmax'),
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()""",
stub="""# TODO: ابنِ CNN: Conv2D(32)->Pool->Conv2D(64)->Pool->Flatten->Dense(128)->Dropout->Dense(10,softmax)
model = keras.Sequential([...])
# TODO: compile بـ adam + sparse_categorical_crossentropy
model.summary()""")

md("## 4️⃣ التدريب (Training)")
code("""history = model.fit(X_train, y_train, validation_split=0.1,
                    epochs=5, batch_size=128, verbose=2)""",
stub="""# TODO: درّب الموديل 5 epochs مع validation_split=0.1
history = ...""")

md("## 5️⃣ منحنيات التدريب (هل overfit؟)")
code("""fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].plot(history.history['loss'], label='train'); ax[0].plot(history.history['val_loss'], label='val')
ax[0].set_title('Loss'); ax[0].legend()
ax[1].plot(history.history['accuracy'], label='train'); ax[1].plot(history.history['val_accuracy'], label='val')
ax[1].set_title('Accuracy'); ax[1].legend(); plt.show()""")

md("## 6️⃣ التقييم على بيانات الاختبار")
code("""test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f'Test accuracy = {test_acc:.3f}')
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
y_pred = model.predict(X_test, verbose=0).argmax(1)
print(classification_report(y_test, y_pred, target_names=CLASSES))
plt.figure(figsize=(8,6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues',
            xticklabels=CLASSES, yticklabels=CLASSES)
plt.xticks(rotation=45, ha='right'); plt.title('Confusion Matrix'); plt.show()""",
stub="""# TODO: قيّم على الاختبار، اطبع الدقة و classification_report و confusion matrix
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print('Test acc:', test_acc)""")

md("## 7️⃣ عرض تنبؤات على عينات (Predictions)")
code("""idx = np.random.choice(len(X_test), 10, replace=False)
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
for ax, i in zip(axes.flat, idx):
    ax.imshow(X_test[i].reshape(28,28), cmap='gray')
    ok = y_pred[i] == y_test[i]
    ax.set_title(f'{CLASSES[y_pred[i]]}', color='green' if ok else 'red'); ax.axis('off')
plt.suptitle('Predictions (green=correct, red=wrong)'); plt.tight_layout(); plt.show()""")

md(r"""## 8️⃣ الخلاصة والتوصيات (Conclusion)
- **النتيجة:** الـ CNN حقّق دقة كويسة (~90%) على تصنيف 10 أنواع ملابس في 5 epochs فقط.
- **أصعب الفئات:** عادةً Shirt / Pullover / Coat بيتلخبطوا مع بعض (متشابهين بصرياً) — واضح في مصفوفة اللخبطة.
- **منع overfitting:** الـ Dropout خلّى فجوة train/val صغيرة.
- **التوصية:** للإنتاج، زوّد epochs، استخدم Data Augmentation (مشروع E2)، أو **Transfer Learning** (مشروع E3) لدقة أعلى.
- **الخطوة القادمة:** نشر الموديل كـ API يستقبل صورة ويرجّع التصنيف.

> ✅ **اللي اتعلمته:** بناء CNN، Conv/Pool، تطبيع الصور، Dropout، وتقييم نموذج رؤية.
""")

base = os.path.dirname(os.path.abspath(__file__))
nb.write(base, "e1_cnn_image_classification")
