# 🛒 تقسيم العملاء وتحليل RFM

## المشكلة
شركة تجارة إلكترونية عندها 1,600 عميل ومحتاجة تقسّمهم لشرائح عشان توجّه حملات التسويق بفاعلية بدل ما ترسل نفس الرسالة للكل.

## الحل
- حساب مقاييس **RFM** (Recency, Frequency, Monetary) لكل عميل
- تصنيف يدوي لشرائح بيزنس (Champions, Loyal, At Risk, Lost, ...)
- تقسيم تلقائي بـ **KMeans Clustering** + تحديد العدد الأمثل بـ Elbow Method
- تصوير بـ PCA projection

## النتائج
| الشريحة | العدد | متوسط الإنفاق |
|---|---|---|
| Champions | 150 | $11,027 |
| Loyal Customers | ~300 | — |
| At Risk | 300 | — |
| Lost | ~200 | — |

## المهارات
`RFM Analysis` · `KMeans Clustering` · `PCA` · `Customer Segmentation` · `Pandas groupby`

## التشغيل
```bash
# Colab (الأسهل)
# افتح النوتبوك من زرار Open in Colab في الـ README الرئيسي

# محلياً
conda activate dsportfolio
jupyter notebook a3_rfm_segmentation_solution.ipynb
```
