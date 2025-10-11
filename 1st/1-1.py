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
