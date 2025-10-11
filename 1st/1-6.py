class Person:
    name = 'JD'
    age = 24
    __height: float

    def __init__(self, name, age, height):
        self.name = name
        self.age = age
        self.__height = height

    def info(self):
        return f'Name: {self.name}, Age: {self.age}, Height: {self.__height}m'

class Student(Person):
    grade = 'B'

    def __init__(self, name, age, height, grade):
        super().__init__(name, age, height)
        self.grade = grade

    def info(self):
        return f'Name: {self.name}, Age: {self.age}, Grade: {self.grade}'