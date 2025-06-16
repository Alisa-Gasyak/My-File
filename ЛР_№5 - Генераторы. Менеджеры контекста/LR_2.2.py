class BatchCalculatorContextManager:
    def __init__(self, filename):
        self.filename = filename
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, 'r')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
    
    def read_expressions(self):
        for line in self.file:
            yield line.strip()

def process_expressions(filename):
    """
    Функция-генератор для обработки выражений из файла
    """
    with BatchCalculatorContextManager(filename) as manager:
        for expression in manager.read_expressions():
            try:
                # Парсим выражение (формат "число-операция-число")
                # Ищем позицию оператора
                operand_pos = -1
                for i, char in enumerate(expression):
                    if char in '+-*/':
                        operand_pos = i
                        break
                
                if operand_pos == -1:
                    yield "Error: invalid expression format"
                    continue
                
                num1 = float(expression[:operand_pos])
                num2 = float(expression[operand_pos+1:])
                operand = expression[operand_pos]
                
                result = calculate(num1, num2, operand)
                yield result
            except ValueError:
                yield "Error: invalid numbers in expression"
            except Exception as e:
                yield f"Error: {str(e)}"

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
          return "Error: division by zero"
        return num1 / num2

def test_calculate():
    """
    Функция для тестирования функции calculate с помощью assert.
    """
    assert calculate(2, 3, '+') == 5
    assert calculate(5, 3, '-') == 2
    assert calculate(4, 2, '*') == 8
    assert calculate(8, 4, '/') == 2
    assert calculate(8, 0, '/') == "Error: division by zero"
    print("Все тесты пройдены!")

if __name__ == "__main__":
    test_calculate()  # Запуск тестов
    
    # Пример использования с файлом
    filename = r"C:\Users\gasal\Desktop\Программирование\ЛР_№5\file.txt" 
    
    print("\nОбработка выражений из файла:")
    for result in process_expressions(filename):
        print(result)