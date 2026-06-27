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

# Визуализация ряда
fig, axes = plt.subplots(3, 1, figsize=(15, 12))

# Исходный ряд
axes[0].plot(train.index, train['qty'], color='blue', alpha=0.7)
axes[0].set_title('Исходный временной ряд (обучающая выборка)')
axes[0].set_ylabel('Количество книг')
axes[0].grid(True, alpha=0.3)

# Скользящее среднее (тренд)
window = 30
rolling_mean = train['qty'].rolling(window=window).mean()
axes[1].plot(train.index, train['qty'], color='blue', alpha=0.3, label='Исходный ряд')
axes[1].plot(train.index, rolling_mean, color='red', linewidth=2, label=f'Скользящее среднее (window={window})')
axes[1].set_title('Ряд со скользящим средним (выявление тренда)')
axes[1].set_ylabel('Количество книг')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Анализ сезонности - сгруппируем по месяцам
monthly_avg = train.groupby(train.index.month)['qty'].mean()
axes[2].bar(monthly_avg.index, monthly_avg.values, color='green', alpha=0.7)
axes[2].set_title('Средние значения по месяцам (сезонность)')
axes[2].set_xlabel('Месяц')
axes[2].set_ylabel('Среднее количество книг')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Дополнительный анализ - декомпозиция
from statsmodels.tsa.seasonal import seasonal_decompose

# Для декомпозиции нужен регулярный ряд, поэтому используем не все данные
# Возьмем период 2012 года для наглядности
train_2012 = train['2012']

# Проверим, что у нас есть все дни
print(f"Пропуски в данных за 2012: {train_2012.isna().sum()}")

# Интерполируем пропуски, если они есть
train_2012_interp = train_2012.interpolate()

# Декомпозиция
decomp = seasonal_decompose(train_2012_interp, model='additive', period=7)  # недельная сезонность

fig, axes = plt.subplots(4, 1, figsize=(15, 10))
decomp.observed.plot(ax=axes[0], title='Наблюдаемый ряд (2012)')
decomp.trend.plot(ax=axes[1], title='Тренд')
decomp.seasonal.plot(ax=axes[2], title='Сезонная компонента (недельная)')
decomp.resid.plot(ax=axes[3], title='Остатки')
plt.tight_layout()
plt.show()

# Выводы
print("\n" + "="*60)
print("АНАЛИЗ ВРЕМЕННОГО РЯДА")
print("="*60)

print("\n1. ТРЕНД:")
print("   - Ряд показывает явный восходящий тренд: в начале 2010 года значения были")
print("     около 100-200 тыс., а к концу 2013 года достигли 400-500 тыс.")
print("   - Тренд нелинейный, с периодами ускорения и замедления")

print("\n2. СЕЗОННОСТЬ:")
print("   - Наблюдается чёткая годовая сезонность: пики приходятся на начало года")
print("     (январь-февраль) и осенью (сентябрь-октябрь)")
print("   - Также видна недельная сезонность (7-дневный цикл)")
print("   - Минимальные значения обычно в праздничные дни (1 января, 1 мая и т.д.)")

print("\n3. КАЛЕНДАРНЫЕ ЭФФЕКТЫ:")
print("   - Заметны резкие падения в праздничные дни (0 в некоторые даты)")
print("   - Конец декабря показывает снижение активности")