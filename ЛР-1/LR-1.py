# Импорт библиотек
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, roc_curve, 
                             confusion_matrix, classification_report)

# 1. Загрузка данных
df = pd.read_csv('adult.csv')
print("Данные загружены. Размер:", df.shape)

# 2. Предобработка
df_clean = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)

# Кодирование категорий
le_geo = LabelEncoder()
le_gen = LabelEncoder()
df_clean['Geography'] = le_geo.fit_transform(df_clean['Geography'])
df_clean['Gender'] = le_gen.fit_transform(df_clean['Gender'])

# Разделение
X = df_clean.drop('Exited', axis=1)
y = df_clean['Exited']

# Масштабирование
scaler = StandardScaler()
num_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProduct', 'EstimatedSalary']
X_scaled = X.copy()
X_scaled[num_cols] = scaler.fit_transform(X[num_cols])

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Модель
model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# 4. Предсказания
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# 5. Метрики
print("\n" + "="*50)
print("МЕТРИКИ КАЧЕСТВА МОДЕЛИ")
print("="*50)
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
print(f"F1-Score:  {f1_score(y_test, y_pred):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_proba):.4f}")
print("="*50)

# 6. Визуализация матрицы ошибок
plt.figure(figsize=(8,6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.title('Матрица ошибок')
plt.xlabel('Предсказано')
plt.ylabel('Фактически')
plt.show()

# 7. ROC-кривая
plt.figure(figsize=(8,6))
fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.plot(fpr, tpr, label=f'AUC = {roc_auc_score(y_test, y_proba):.4f}')
plt.plot([0,1], [0,1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC-кривая')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# 8. Важность признаков
coef_df = pd.DataFrame({
    'Признак': X.columns,
    'Коэффициент': model.coef_[0]
}).sort_values('Коэффициент', key=abs, ascending=False)

print("\nВАЖНОСТЬ ПРИЗНАКОВ:")
print(coef_df.to_string(index=False))

# Визуализация важности
plt.figure(figsize=(10,6))
coef_sorted = coef_df.sort_values('Коэффициент')
colors = ['red' if x < 0 else 'green' for x in coef_sorted['Коэффициент']]
plt.barh(coef_sorted['Признак'], coef_sorted['Коэффициент'], color=colors)
plt.axvline(0, color='black', linestyle='-', linewidth=0.5)
plt.title('Важность признаков в модели')
plt.xlabel('Коэффициент логистической регрессии')
plt.tight_layout()
plt.show()