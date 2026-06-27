import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings
warnings.filterwarnings('ignore')

# Загружаем данные
df = pd.read_csv('tovar_moving.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)
df.set_index('date', inplace=True)

print("Первые 5 строк данных:")
print(df.head())
print(f"\nВсего наблюдений: {len(df)}")
print(f"Период: с {df.index.min()} по {df.index.max()}")

# Отделяем последнее значение как тестовое
train = df.iloc[:-1]
test = df.iloc[-1:]

print(f"Последнее значение (тестовое): {test['qty'].values[0]:.0f}")
print(f"Размер обучающей выборки: {len(train)}")
print(f"Размер тестовой выборки: {len(test)}")