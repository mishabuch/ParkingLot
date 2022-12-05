from parking_lot.utils.constants import ParkingSlotType


# The Parking Slot class represents each parking slot in the parking lot.
# It is represented by a unique slot it, a vehicle license id assigned to it if a vehicle is parked in the spot
# The parking slot type represents is the slot is of Small, Medium or Large size.
# Small spot is used to park scooters/motorcycles, medium slot is used to park cars/SUVs and
# Large spot is used to park Bus/Trucks
# It also has an is_occupied flag which represents if the slot is empty or not.

class ParkingSlot:
    def __init__(self, parking_slot_id, parking_slot_type: ParkingSlotType):
        self.slot_id = parking_slot_id
        self.parking_slot_type = parking_slot_type
        self.is_occupied = False
        self.__vehicle_licence_id = None

    def assign_vehicle_to_spot(self, vehicle_licence_id):
        self.__vehicle_licence_id = vehicle_licence_id
        self.is_occupied = True

    def remove_vehicle_from_slot(self):
        self.__vehicle_licence_id = None
        self.is_occupied = False

    def get_vehicle_license_id(self):
        return self.__vehicle_licence_id


# Small, Medium and Large Slots are types of Parking slots, differentiated by their sizes.
# As a separate class, we can add fucntionality particular to a slot size.
class SmallSlot(ParkingSlot):
    def __init__(self, parking_slot_id):
        super().__init__(parking_slot_id, ParkingSlotType.Small)


class MediumSlot(ParkingSlot):
    def __init__(self, parking_slot_id):
        super().__init__(parking_slot_id, ParkingSlotType.Medium)


class LargeSlot(ParkingSlot):
    def __init__(self, parking_slot_id):
        super().__init__(parking_slot_id, ParkingSlotType.Large)
