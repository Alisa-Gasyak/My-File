import random

def random_number_generator(count, min_val, max_val):
    for _ in range(count):
        yield random.randint(min_val, max_val)

# Пример использования:
gen = random_number_generator(5, 10, 20)
for num in gen:
    print(num)