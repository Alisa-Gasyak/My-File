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

def adf_test(series, title=''):
    """Тест Дики-Фуллера на стационарность"""
    result = adfuller(series, autolag='AIC')
    print(f'Результаты ADF теста для {title}:')
    print(f'  ADF статистика: {result[0]:.6f}')
    print(f'  p-value: {result[1]:.6f}')
    print(f'  Критические значения:')
    for key, value in result[4].items():
        print(f'    {key}: {value:.6f}')
    print(f'  Стационарен при 5%: {"ДА" if result[1] < 0.05 else "НЕТ"}')
    return result[1] < 0.05

print("="*60)
print("ПРОВЕРКА НА СТАЦИОНАРНОСТЬ")
print("="*60)

# 1. Исходный ряд
is_stationary = adf_test(train['qty'], 'исходного ряда')

# Если не стационарен, пробуем взять разности
if not is_stationary:
    # Первая разность
    diff1 = train['qty'].diff().dropna()
    print("\n" + "-"*40)
    is_stationary_diff1 = adf_test(diff1, 'первой разности')
    
    # Визуализация
    fig, axes = plt.subplots(2, 1, figsize=(15, 8))
    
    axes[0].plot(train.index, train['qty'])
    axes[0].set_title('Исходный ряд')
    axes[0].set_ylabel('Количество книг')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(train.index[1:], diff1)
    axes[1].set_title('Первая разность')
    axes[1].set_ylabel('Разность')
    axes[1].axhline(y=0, color='red', linestyle='--', alpha=0.5)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Если первая разность не стационарна, пробуем вторую
    if not is_stationary_diff1:
        diff2 = diff1.diff().dropna()
        print("\n" + "-"*40)
        is_stationary_diff2 = adf_test(diff2, 'второй разности')
        
        if is_stationary_diff2:
            print("\nПорядок интегрирования d = 2")
        else:
            print("\nРяд не становится стационарным после 2-х разностей")
    else:
        print("\nПорядок интегрирования d = 1")
else:
    print("\nПорядок интегрирования d = 0")