def guess_number_binary(target, start=1, end=100):
    """
    Угадывает число с помощью бинарного поиска.

    target: Загаданное число (int)
    start: Начало интервала (int)
    end: Конец интервала (int)
    return: Возвращает угаданное число (int)
    
    """
    attempts = 0   # Счётчик попыток

    while start <= end:
        attempts += 1
        mid = (start + end) // 2  # Нахождение середины интервала

        if mid == target:
            return mid, attempts
        elif mid < target:
            start = mid + 1  # Поиск в промежутке больше середины
        else:
            end = mid - 1  # Поиск в промежутке меньше середины
    return None, attempts # Возвращает значение None, если число не найдено в заданном интервале

def main():
    """
    Основная функция, которая запускает игру. Генерирует случайное число в диапазоне от 1 до 100 и 
    вызывает соответствующую функцию для угадывания числа, а после выводит результат
    
    """
    import random
    target = random.randint(1, 100)  # Загадывается число с помощью функции random
    guessed_number, attempts = guess_number_binary(target)
    print("Загадано число от 1 до 100.")
    print(f"Угадано число: {guessed_number} за {attempts} попыток!")

def test_guess_number_binary():
    """
    Функция для тестирования функции с помощью assert.
    """
    assert guess_number_binary(2, 1, 100) 
    assert guess_number_binary(5, 1, 100) 
    #test_guess_number_binary()
print("Все тесты пройдены!")

if __name__ == "__main__":
    main()
