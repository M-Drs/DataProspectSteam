def fibonacci(limit):
    a, b = 0, 1
    for _ in range(limit):
        yield a
        a, b = b, a + b

for num in fibonacci(1):
    print(num)

# def numbers():
#     yield from [1, 2, 3, 4, 5]

# for num in numbers():
#     print(num)

def infinite_count():
    n = 0
    while True:
        yield n
        n += 1

gen = infinite_count()
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2


def decorator(func):
    def wrapper():
        print("Before the function call")
        func()
        print("After the function call")
    return wrapper

@decorator
def say_hello():
    print("Hello!")


