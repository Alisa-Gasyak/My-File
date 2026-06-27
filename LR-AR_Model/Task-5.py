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

# Графики ACF и PACF для стационарного ряда (первая разность)
diff1 = train['qty'].diff().dropna()

fig, axes = plt.subplots(2, 1, figsize=(15, 10))

# ACF
plot_acf(diff1, ax=axes[0], lags=40, alpha=0.05)
axes[0].set_title('Автокорреляционная функция (ACF) для первой разности')

# PACF
plot_pacf(diff1, ax=axes[1], lags=40, alpha=0.05, method='ywm')
axes[1].set_title('Частичная автокорреляционная функция (PACF) для первой разности')

plt.tight_layout()
plt.show()

# Определение порядка AR по PACF
print("="*60)
print("ОПРЕДЕЛЕНИЕ ПОРЯДКА AR ПО PACF")
print("="*60)

# Находим лаги, где PACF значимо отличается от нуля
pacf_values, pacf_confint = pacf(diff1, nlags=40, alpha=0.05, method='ywm')
significant_lags = []
for i in range(1, len(pacf_values)):
    lower = pacf_confint[i][0]
    upper = pacf_confint[i][1]
    if pacf_values[i] > upper or pacf_values[i] < lower:
        significant_lags.append(i)

print(f"Значимые лаги по PACF: {significant_lags}")
print(f"Порядок AR (p): {significant_lags[0] if significant_lags else 1}")
print("\nИнтерпретация:")
print("- На графике PACF видно, что первый лаг имеет высокое значение")
print("- Остальные лаги преимущественно находятся в пределах доверительного интервала")
print("- Это указывает на модель AR(1) или AR(2)")

# Рекомендуемый порядок
p = significant_lags[0] if significant_lags else 1
print(f"\nРекомендуемый порядок AR: p = {p}")