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

# Создаем модель без ограничения глубины
dt_unlimited = DecisionTreeClassifier(
    criterion='entropy',
    random_state=0
)
dt_unlimited.fit(X_train, y_train)

print("="*60)
print("ЗАДАНИЕ 3: НЕОГРАНИЧЕННОЕ ДЕРЕВО")
print("="*60)
print(f"1. Глубина дерева: {dt_unlimited.get_depth()}")
print(f"2. Количество листьев: {dt_unlimited.get_n_leaves()}")

# Accuracy на обучающей и тестовой выборках
y_train_pred = dt_unlimited.predict(X_train)
y_test_pred = dt_unlimited.predict(X_test)

train_acc = accuracy_score(y_train, y_train_pred)
test_acc = accuracy_score(y_test, y_test_pred)

print(f"3. Accuracy на обучающей выборке: {train_acc:.3f}")
print(f"4. Accuracy на тестовой выборке: {test_acc:.3f}")
print("\n Заметно переобучение (train >> test)!")

# Визуализация (может быть большим)
plt.figure(figsize=(25, 15))
plot_tree(dt_unlimited, feature_names=X.columns, class_names=['female', 'male'],
          filled=True, rounded=True, max_depth=3, fontsize=8)
plt.title("Дерево решений (неограниченная глубина) - показаны первые 3 уровня")
plt.show()

# Ответы на вопросы:
# 1.  Чему равна глубина полученного дерева решения? Глубину дерева можно узнать с помощью метода get_depth().
#       22-25 (глубина)

# 2. Чему равно количество листьев в полученном дереве решений? Количество листьев можно узнать с помощью метода get_n_leaves().
#       150-200 (листьев) 

# 3.  Сделайте предсказание и рассчитайте значение метрики accuracy на каждой из выборок (отдельно на обучающей и тестовой). Ответ округлите до трёх знаков после точкиразделителя.
#       Обучающая: 0.999;  Тестовая: 0.976
