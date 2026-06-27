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

# Создаем и обучаем модель
dt_depth2 = DecisionTreeClassifier(
    max_depth=2,
    criterion='entropy',
    random_state=42
)
dt_depth2.fit(X_train, y_train)

# Визуализация
plt.figure(figsize=(14, 8))
plot_tree(dt_depth2, feature_names=X.columns, class_names=['female', 'male'],
          filled=True, rounded=True, fontsize=11)
plt.title("Дерево решений (max_depth=2)")
plt.show()

# Определяем используемые признаки
used_features = set()
for i in range(dt_depth2.tree_.node_count):
    if dt_depth2.tree_.feature[i] >= 0:  # не лист
        used_features.add(X.columns[dt_depth2.tree_.feature[i]])

print("="*60)
print("ЗАДАНИЕ 2: ДЕРЕВО ГЛУБИНОЙ 2")
print("="*60)
print(f"1. Используемые признаки: {sorted(used_features)}")

# Считаем листья с классом female
leaf_indices = dt_depth2.tree_.children_left == -1  # листья
female_leaves = 0
for i in range(dt_depth2.tree_.node_count):
    if leaf_indices[i]:
        if dt_depth2.tree_.value[i][0][0] > dt_depth2.tree_.value[i][0][1]:
            female_leaves += 1

print(f"2. Количество листьев с классом female: {female_leaves}")

# Accuracy
y_pred = dt_depth2.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"3. Accuracy на тестовой выборке: {acc:.3f}")

# Ответы на вопросы:
# 1. На основе какого фактора будет построено данное дерево решений?
#     A, D, E (meanfreq, meanfun, minfun)

# 2. Сколько листьев в построенном дереве содержат в качестве предсказания класс female? Для того, чтобы отобразить имена классов при визуализации дерева решения с помощью функции plot_tree(), укажите параметр class_names=dt.classes_.
#       3 листа с классом female 

# 3.  Сделайте предсказание и рассчитайте значение метрики accuracy на тестовой выборке. Ответ округлите до трёх знаков после точкиразделителя.
#       0.981
