def fibonacci_generator(count):
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b

def add_ten_generator(sequence):
    for num in sequence:
        yield num + 10

# Генерируем 10 чисел Фибоначчи с добавлением 10
fib_gen = fibonacci_generator(10)
result_gen = add_ten_generator(fib_gen)

print("Числа Фибоначчи + 10:")
for num in result_gen:
    print(num)