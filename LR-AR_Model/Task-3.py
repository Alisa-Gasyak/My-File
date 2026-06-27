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

# Экспоненциальное сглаживание
def exponential_smoothing(data, alpha):
    """Простое экспоненциальное сглаживание"""
    result = [data[0]]
    for n in range(1, len(data)):
        result.append(alpha * data[n] + (1 - alpha) * result[-1])
    return np.array(result)

# Применяем к обучающей выборке
train_values = train['qty'].values
smoothed = exponential_smoothing(train_values, alpha=0.7)

# Прогноз на последнее значение - это последнее сглаженное значение
forecast_es = smoothed[-1]
actual = test['qty'].values[0]

print("="*60)
print("ЭКСПОНЕНЦИАЛЬНОЕ СГЛАЖИВАНИЕ (α = 0.7)")
print("="*60)
print(f"Прогноз: {forecast_es:.0f}")
print(f"Фактическое значение: {actual:.0f}")
print(f"Абсолютная ошибка: {abs(forecast_es - actual):.0f}")
print(f"Относительная ошибка: {abs(forecast_es - actual)/actual*100:.2f}%")

# Визуализация
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(train.index, train['qty'], color='blue', alpha=0.5, label='Исходный ряд')
ax.plot(train.index, smoothed, color='red', linewidth=2, label=f'Эксп. сглаживание (α={alpha})')
ax.axvline(x=train.index[-1], color='gray', linestyle='--', alpha=0.7)
ax.scatter(train.index[-1], smoothed[-1], color='red', s=100, zorder=5, 
           label=f'Прогноз: {smoothed[-1]:.0f}')
ax.scatter(test.index[0], actual, color='green', s=100, zorder=5,
           label=f'Факт: {actual:.0f}')
ax.set_title('Экспоненциальное сглаживание')
ax.set_ylabel('Количество книг')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()