class Car:
    price = 200000

    def __init__(self, color):
        self.color = color

print(Car.price)
Car.price = 320000
Car.name = 'TSL'
Car1 = Car('RED')
print(Car.name, Car.price, Car1.color)
Car1.color = 'BLUE'
print(Car1.color)
