def fib(n: int):
    a, b = 1, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


print(*fib(20), sep=', ')
