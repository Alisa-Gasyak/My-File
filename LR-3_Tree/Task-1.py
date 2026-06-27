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

# Разделение на обучающую и тестовую выборки (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print(f"Размер обучающей выборки: {X_train.shape}")
print(f"Размер тестовой выборки: {X_test.shape}")
print(f"\nРаспределение классов в обучающей выборке:")
print(y_train.value_counts())

from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# Создаем и обучаем модель
dt_stump = DecisionTreeClassifier(
    max_depth=1,           # Решающий пень
    criterion='entropy',   # Энтропия Шеннона
    random_state=42
)
dt_stump.fit(X_train, y_train)

# Визуализация дерева
plt.figure(figsize=(12, 6))
plot_tree(dt_stump, feature_names=X.columns, class_names=['female', 'male'], 
          filled=True, rounded=True, fontsize=12)
plt.title("Решающий пень (max_depth=1)")
plt.show()

# Получаем информацию о корневой вершине
feature_used = X.columns[dt_stump.tree_.feature[0]]
threshold = dt_stump.tree_.threshold[0]
left_samples = dt_stump.tree_.n_node_samples[1]   # левый лист
right_samples = dt_stump.tree_.n_node_samples[2]  # правый лист
total_samples = left_samples + right_samples

# Ответы на вопросы
print("="*60)
print("ЗАДАНИЕ 1: РЕШАЮЩИЙ ПЕНЬ")
print("="*60)
print(f"1. Фактор в корневой вершине: {feature_used}")
print(f"2. Пороговое значение: {threshold:.3f}")
print(f"3. Процент наблюдений, для которых выполняется условие: "
      f"{left_samples/total_samples*100:.1f}%")

# Предсказание и accuracy
y_pred = dt_stump.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"4. Accuracy на тестовой выборке: {acc:.3f}")

# Ответы на вопросы:
# 1. На основе какого фактора будет построено решающее правило в корневой вершине?
#     meanfun (средняя основная частота)

# 2. Чему равно оптимальное пороговое значение для данного фактора? Ответ округлите до трёх знаков после точки разделителя.
#       0.084 

# 3.  Сколько процентов наблюдений, для которых выполняется заданное в корневой вершине условие, содержится в обучающей выборке? Ответ округлите до одного знака после точки разделителя. 
#       77.8

# 4.  Сделайте предсказание и рассчитайте значение метрики accuracy на тестовой выборке. Ответ округлите до трёх знаков после точкиразделителя.
#       0.972
