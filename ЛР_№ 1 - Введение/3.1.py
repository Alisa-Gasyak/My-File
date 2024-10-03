def calculate(num1, num2, operand):
    """
     Функция принимает два числа и тип операции. Служит для выполнения операций с числами. Выводит результат или сообщение об ошибке.
    """
    if operand == '+':
        return num1 + num2
    elif operand == '-':
        return num1 - num2
    elif operand == '*':
         return num1 * num2
    elif operand == '/':
        if num2 == 0:
          return "Error"
        return num1 / num2


def main():
    """
    Основная функция, которая запрашивает у пользователя ввод двух чисел и тип операции. Запускает функцию calculate() и выводит результат.
    """
    try:
      num1 = float(input("Введите первое число: "))
      num2 = float(input("Введите второе число: "))
      operand = input("Введите операцию (+, -, *, /): ")

      result = calculate(num1, num2, operand)
      print("Результат:", result)
    except ValueError:
      print("Error: uncorrect data .")

def test_calculate():
    """
    Функция для тестирования функции calculate с помощью assert.
    """
    assert calculate(2, 3, '+') == 5
    assert calculate(5, 3, '-') == 2
    assert calculate(4, 2, '*') == 8
    assert calculate(8, 4, '/') == 2
    assert calculate(8, 0, '/') == "Error"

    print("Все тесты пройдены!")


if __name__ == "__main__":
    test_calculate()  # Запуск тестов
    main()            # Запуск основной функции

