class Car:
    price = 200000

    def __init__(self, color):
        self.color = color


Car.price = 320000
Car.name = 'TSL'
Car1 = Car('RED')
Car1.color = 'BLUE'
