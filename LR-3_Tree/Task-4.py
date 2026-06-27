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

from sklearn.model_selection import GridSearchCV, StratifiedKFold

# Задаем сетку параметров
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [4, 5, 6, 7, 8, 9, 10],
    'min_samples_split': [3, 4, 5, 10]
}

# Кросс-валидация
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# GridSearch
grid_search = GridSearchCV(
    DecisionTreeClassifier(random_state=0),
    param_grid,
    cv=cv,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)
grid_search.fit(X_train, y_train)

# Лучшие параметры
best_model = grid_search.best_estimator_

print("="*60)
print("ЗАДАНИЕ 4: GRIDSEARCHCV")
print("="*60)
print(f"1. Лучший критерий: {grid_search.best_params_['criterion']}")
print(f"2. Лучшая max_depth: {grid_search.best_params_['max_depth']}")
print(f"3. Лучшее min_samples_split: {grid_search.best_params_['min_samples_split']}")
print(f"\nЛучшая accuracy (CV): {grid_search.best_score_:.4f}")

# Accuracy на выборках
y_train_pred = best_model.predict(X_train)
y_test_pred = best_model.predict(X_test)

train_acc = accuracy_score(y_train, y_train_pred)
test_acc = accuracy_score(y_test, y_test_pred)

print(f"4. Accuracy на обучающей выборке: {train_acc:.3f}")
print(f"5. Accuracy на тестовой выборке: {test_acc:.3f}")

# Сравнение с неограниченным деревом
print(f"\n Сравнение:")
print(f"   Неограниченное дерево: train={dt_unlimited.score(X_train, y_train):.3f}, test={dt_unlimited.score(X_test, y_test):.3f}")
print(f"   Оптимальное дерево:    train={train_acc:.3f}, test={test_acc:.3f}")

# Ответы на вопросы:
# 1.   Какой критерий информативности использует наилучшая модель?
#       Критерий Джини

# 2. Чему равна оптимальная найденная автоматически (с помощью GridSearchCV) максимальная глубина?
#       8

# 3. Чему равно оптимальное минимальное количество объектов, необходимое для разбиения?
#       3

# 4.  Сделайте предсказание и рассчитайте значение метрики accuracy на каждой из выборок (отдельно на обучающей и тестовой). Ответ округлите до трёх знаков после точкиразделителя.
#       Обучающая: 0.987;  Тестовая: 0.980