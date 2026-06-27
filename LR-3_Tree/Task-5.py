import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Загрузка данных
df = pd.read_csv('voice_gender.csv')

# Разделение на признаки и целевую переменную
X = df.drop('label', axis=1)
y = df['label']

# Получаем важность признаков
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': best_model.feature_importances_
}).sort_values('importance', ascending=False)

print("="*60)
print("ЗАДАНИЕ 5: ВАЖНОСТЬ ПРИЗНАКОВ")
print("="*60)
print(feature_importance.to_string(index=False))

# Визуализация
plt.figure(figsize=(12, 8))
top_features = feature_importance.head(10)
plt.barh(top_features['feature'], top_features['importance'])
plt.xlabel('Важность')
plt.title('Топ-10 наиболее важных признаков')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Топ-3 признака
top3 = feature_importance.head(3)['feature'].tolist()
print(f"\nТоп-3 наиболее важных признака:")
for i, f in enumerate(top3, 1):
    print(f"  {i}. {f}")

# Выделите топ 3 наиболее важных факторов, участвующих в построении дерева решений

# meanfun (средняя основная частота)
# minfun (минимальная основная частота)
# IQR (межквартильный размах)
