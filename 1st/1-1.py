def triangle(a, b, c) -> str:
    if not all(isinstance(x, (int, float)) and x > 0 for x in (a, b, c)):
        return 'Error: sides must be positive numbers'
    a, b, c = sorted((a, b, c))
    if a + b <= c:
        return 'Not a triangle'
    t = 'Equilateral' if a == b == c else 'Isosceles' if a == b or b == c else 'Scalene'
    s = a * a + b * b - c * c
    angle = 'Right' if s == 0 else 'Acute' if s > 0 else 'Obtuse'
    return f'{t}, {angle}'


print(triangle(5, 4, 3))  # Scalene, Right
print(triangle(2, 2, 3))  # Isosceles, Acute
print(triangle(1, 1, 1))  # Equilateral, Acute
print(triangle(2, 1, 3))  # Not a triangle