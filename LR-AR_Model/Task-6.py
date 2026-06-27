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

print("="*60)
print("ПОСТРОЕНИЕ МОДЕЛИ AR")
print("="*60)

# Строим модель AR(p) на исходном ряду
# Стандартный AutoReg ожидает стационарный ряд, но мы строим на исходном с diff

# Вариант 1: AR на стационарном ряду (первая разность)
p_recommended = 1  # из PACF

# Строим модель на разностях
model_diff = AutoReg(diff1, lags=p_recommended).fit()
print(f"\nМодель AR({p_recommended}) на разностях:")
print(model_diff.summary())

# Прогнозируем следующее значение разности
# Для прогноза последнего значения нам нужно:
# 1. Получить последние p значений разности
# 2. Использовать модель для предсказания следующего значения разности
# 3. Прибавить к последнему значению исходного ряда

last_diff_values = diff1.iloc[-p_recommended:].values
if p_recommended == 1:
    last_diff = last_diff_values[0]
else:
    # Для AR(p) нужно сделать прогноз
    forecast_diff = model_diff.forecast(steps=1)[0]
    last_diff = forecast_diff

last_original = train['qty'].iloc[-1]
forecast_ar = last_original + last_diff

print(f"\nПрогноз с использованием AR({p_recommended}):")
print(f"  Последнее значение исходного ряда: {last_original:.0f}")
print(f"  Прогнозируемая разность: {last_diff:.0f}")
print(f"  Прогноз: {forecast_ar:.0f}")

# Для сравнения построим модель AR с другим порядком (p=2)
model_diff2 = AutoReg(diff1, lags=2).fit()
forecast_diff2 = model_diff2.forecast(steps=1)[0]
forecast_ar2 = last_original + forecast_diff2

# Также попробуем AR на исходном ряду
model_orig = AutoReg(train['qty'], lags=7).fit()  # недельная сезонность
forecast_orig = model_orig.forecast(steps=1)[0]

print(f"\nСравнение моделей AR:")
print(f"  AR(1) (разности): {forecast_ar:.0f}")
print(f"  AR(2) (разности): {forecast_ar2:.0f}")
print(f"  AR(7) (исходный): {forecast_orig:.0f}")

# Фактическое значение
actual = test['qty'].values[0]
print(f"\nФактическое значение: {actual:.0f}")

# Ошибки
errors = {
    'AR(1)': abs(forecast_ar - actual),
    'AR(2)': abs(forecast_ar2 - actual),
    'AR(7)': abs(forecast_orig - actual)
}

print("\nОшибки прогнозов:")
for model, err in errors.items():
    print(f"  {model}: {err:.0f} ({err/actual*100:.2f}%)")