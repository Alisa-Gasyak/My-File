import random

class RandomNumberIterator:
    def __init__(self, count, min_val, max_val):
        self.count = count
        self.min_val = min_val
        self.max_val = max_val
        self.generated = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.generated >= self.count:
            raise StopIteration
        self.generated += 1
        return random.randint(self.min_val, self.max_val)

# Пример использования:
iterator = RandomNumberIterator(5, 10, 20)
for num in iterator:
    print(num)