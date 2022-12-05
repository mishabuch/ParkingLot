from parking_lot.utils.constants import VehicleType
from parking_lot.utils.utils import get_unique_vehicle_license_id


# The Vehicle class represents a vehicle that can be parked
# It has the unique id - which is the license number of the vehicle or can be the number plate
# The vehicle_type can be car, SUV, bus, truck, scooter or motorcycle

class Vehicle:
    def __init__(self, vehicle_type: VehicleType):
        self.vehicle_license_id = get_unique_vehicle_license_id()
        self.vehicle_type = vehicle_type


class Motorcycle(Vehicle):
    def __init__(self):
        super().__init__(VehicleType.Motorcycle)


class Scooter(Vehicle):
    def __init__(self):
        super().__init__(VehicleType.Scooter)


class Car(Vehicle):
    def __init__(self):
        super().__init__(VehicleType.Car)


class Suv(Vehicle):
    def __init__(self):
        super().__init__(VehicleType.Suv)


class Bus(Vehicle):
    def __init__(self):
        super().__init__(VehicleType.Bus)


class Truck(Vehicle):
    def __init__(self):
        super().__init__(VehicleType.Truck)
