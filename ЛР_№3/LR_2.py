import math
from statistics import median, variance, stdev

def convert_precision(tolerance):
    """
    Преобразует значение точности (tolerance) в порядок (количество знаков после запятой для округления).
    """
    if tolerance <= 0:
        raise ValueError("Tolerance must be positive.")
    return round(abs(round(math.log10(tolerance))))


def calculate(action, *args, tolerance=1e-6):
    """
    Выполняет арифметические или статистические операции над переданными числами.
    """
    if not args:
        return "Error"

    precision = convert_precision(tolerance)

    # Базовые операции (требуют минимум 2 аргумента)
    if action == '+':
        result = sum(args)
    elif action == '-':
        result = args[0] - sum(args[1:])
    elif action == '*':
        result = 1
        for num in args:
            result *= num
    elif action == '/':
        if 0 in args[1:]:
            return "Error"
        result = args[0]
        for num in args[1:]:
            result /= num

    # Статистические операции (работают с любым количеством аргументов)
    elif action == 'mean':
        result = sum(args) / len(args)
    elif action == 'variance':
        result = variance(args)
    elif action == 'std_deviation':
        result = stdev(args)
    elif action == 'median':
        result = median(args)
    elif action == 'iqr':
        sorted_args = sorted(args)
        n = len(sorted_args)
        q1 = median(sorted_args[:n//2])
        q3 = median(sorted_args[(n+1)//2:])
        result = q3 - q1
    else:
        return "Error"

    return round(result, precision) if isinstance(result, float) else result


def main():
    """
    Основная функция для ввода данных пользователем.
    """
    try:
        action = input("Введите операцию (+, -, *, /, mean, variance, std_deviation, median, iqr): ")
        nums = list(map(float, input("Введите числа через пробел: ").split()))
        
        result = calculate(action, *nums)
        print("Результат:", result)
    except ValueError:
        print("Error: некорректные данные.")
