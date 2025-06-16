
import time
from time import perf_counter

class Timer:
    def __enter__(self):
        self.start = perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = perf_counter()
        self.elapsed = self.end - self.start
        print(f"Время выполнения: {self.elapsed:.6f} секунд")



def fibonacci_generator(n):
    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b

# Пример использования
if __name__ == "__main__":
    n = 1_000_000  # Количество чисел Фибоначчи для генерации
    
    with Timer():
        # Генерируем и потребляем все числа Фибоначчи
        fib_gen = fibonacci_generator(n)
        list(fib_gen)  # Потребляем генератор, чтобы измерить полное время выполнения