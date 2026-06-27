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
print("СРАВНЕНИЕ РЕЗУЛЬТАТОВ")
print("="*60)

results = {
    'Метод': ['Экспоненциальное сглаживание (α=0.7)', 'AR(1) на разностях', 'AR(2) на разностях', 'AR(7) на исходном ряду'],
    'Прогноз': [forecast_es, forecast_ar, forecast_ar2, forecast_orig],
    'Факт': [actual, actual, actual, actual],
    'Абсолютная ошибка': [abs(forecast_es - actual), abs(forecast_ar - actual), abs(forecast_ar2 - actual), abs(forecast_orig - actual)],
    'Относительная ошибка (%)': [
        abs(forecast_es - actual)/actual*100,
        abs(forecast_ar - actual)/actual*100,
        abs(forecast_ar2 - actual)/actual*100,
        abs(forecast_orig - actual)/actual*100
    ]
}

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

print("\n" + "="*60)
print("ВЫВОДЫ")
print("="*60)

print("""
1. ЛУЧШИЙ РЕЗУЛЬТАТ:
   Экспоненциальное сглаживание (α=0.7) показало наилучший результат
   с относительной ошибкой 1.73%. Это связано с тем, что метод хорошо
   реагирует на последние изменения в ряду.

2. AR-МОДЕЛИ:
   - Модель AR(7) на исходном ряду дала ошибку 3.84%, что неплохо,
     но хуже экспоненциального сглаживания.
   - Модели AR(1) и AR(2) на разностях показали очень плохие результаты
     (ошибка ~18.65%), так как они не учитывают тренд и сезонность.

3. ПРИЧИНЫ РАЗЛИЧИЙ:
   - Временной ряд имеет сильный тренд и сезонность, что усложняет
     прогнозирование простыми методами.
   - AR-модели на разностях теряют важную информацию о тренде.
   - Экспоненциальное сглаживание с высоким α хорошо адаптируется
     к изменениям.

4. РЕКОМЕНДАЦИИ:
   - Для более точного прогнозирования стоит использовать более
     сложные модели (SARIMA, Prophet, LSTM).
   - Учитывать праздничные дни и сезонность.
   - Использовать комбинацию нескольких методов.
""")

# Визуализация сравнения
fig, ax = plt.subplots(figsize=(12, 6))

methods = ['Эксп. сглаж.', 'AR(1) разн.', 'AR(2) разн.', 'AR(7) исход.']
errors = [abs(forecast_es - actual), abs(forecast_ar - actual), 
          abs(forecast_ar2 - actual), abs(forecast_orig - actual)]

bars = ax.bar(methods, errors, color=['green', 'red', 'red', 'orange'])
ax.axhline(y=abs(forecast_es - actual), color='green', linestyle='--', 
           label=f'Лучший результат: {abs(forecast_es - actual):.0f}')
ax.set_title('Сравнение ошибок прогнозов')
ax.set_ylabel('Абсолютная ошибка')
ax.legend()
ax.grid(True, alpha=0.3)

for bar, err in zip(bars, errors):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{err:.0f}\n({err/actual*100:.1f}%)',
            ha='center', va='bottom')

plt.tight_layout()
plt.show()