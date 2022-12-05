from datetime import datetime

from parking_lot.exceptions.NoSlotAvailableException import NoSlotAvailableException
from parking_lot.exceptions.VehicleNotAllowedException import VehicleNotAllowedException
from parking_lot.parking_ticket import ParkingTicket
from parking_lot.utils.constants import FeeModels, VehicleType, ParkingSlotType, ParkingTicketStatus
from parking_lot.utils.utils import get_parking_slot_type_from_vehicle_type, initialize_empty_parking_spots, \
    get_duration_in_hours, get_unique_receipt_id


# The Parking Lot class is the crux of the parking lot system
# It has only one instance at a time - i.e follows a Singleton pattern
# It offers functionality of parking a vehicle, remove/unpark a vehicle and generate tickets when a vehicle is unparked
# It also keeps track of the empty parking slots, occupied slots, active tickets.
# Each parking slot follows a fee model according to the type and capacity of the parking lot.

class ParkingLot:
    instance = None

    class __ParkingLot:
        def __init__(self, name, max_small_parking_slots, max_medium_parking_slots, max_large_parking_slots,
                     fee_model_type: FeeModels):
            self.name = name
            self.__max_large_parking_slots = max_large_parking_slots
            self.__max_medium_parking_slots = max_medium_parking_slots
            self.__max_small_parking_slots = max_small_parking_slots
            self.__fee_model_type = fee_model_type
            self.small_parking_slots_count = 0
            self.medium_parking_slots_count = 0
            self.large_parking_slots_count = 0
            self.__parking_slots = initialize_empty_parking_spots(max_small_parking_slots,
                                                                  max_medium_parking_slots,
                                                                  max_large_parking_slots)
            self.__occupied_slots = {}
            self.__active_tickets = {}

    def __init__(self, name, max_small_parking_slots, max_medium_parking_slots, max_large_parking_slots,
                 fee_model_type: FeeModels):
        if not ParkingLot.instance:
            ParkingLot.instance = ParkingLot.__ParkingLot(name, max_small_parking_slots, max_medium_parking_slots,
                                                          max_large_parking_slots,
                                                          fee_model_type)
        else:
            ParkingLot.instance.name = name
            ParkingLot.instance.__max_large_parking_slots = max_large_parking_slots
            ParkingLot.instance.__max_medium_parking_slots = max_medium_parking_slots
            ParkingLot.instance.__max_small_parking_slots = max_small_parking_slots
            ParkingLot.instance.__fee_model_type = fee_model_type
            ParkingLot.instance.small_parking_slots_count = 0
            ParkingLot.instance.medium_parking_slots_count = 0
            ParkingLot.instance.large_parking_slots_count = 0
            ParkingLot.instance.__occupied_slots = {}
            ParkingLot.instance.__active_tickets = {}
            ParkingLot.instance.__parking_slots = initialize_empty_parking_spots(max_small_parking_slots,
                                                                                 max_medium_parking_slots,
                                                                                 max_large_parking_slots)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    # This method checks if an empty parking slot is available for a vehicle according to its type/size
    # It checks if the vehicle type is allowed (raises an Exception if not), and if allowed has space to park.
    # Returns a boolean value

    def __check_if_parking_slot_available(self, vehicle_type):
        if vehicle_type == VehicleType.Motorcycle or vehicle_type == VehicleType.Scooter:
            if self.__max_small_parking_slots == 0:
                raise VehicleNotAllowedException(f'{vehicle_type.value} is not allowed in this parking lot')
            else:
                return self.small_parking_slots_count >= self.__max_small_parking_slots
        if vehicle_type == VehicleType.Car or vehicle_type == VehicleType.Suv:
            if self.__max_medium_parking_slots == 0:
                raise VehicleNotAllowedException(f'{vehicle_type.value} is not allowed in this parking lot')
            else:
                return self.medium_parking_slots_count >= self.__max_medium_parking_slots
        if vehicle_type == VehicleType.Bus or vehicle_type == VehicleType.Truck:
            if self.__max_large_parking_slots == 0:
                raise VehicleNotAllowedException(f'{vehicle_type.value} is not allowed in this parking lot')
            else:
                return self.large_parking_slots_count >= self.__max_large_parking_slots
        return False

    # Based on the Vehicle type, this method returns
    # the first available empty parking spot for the vehicle type
    def __get_empty_parking_spot(self, vehicle_type):
        assigned_slot = None
        parking_slot_type = get_parking_slot_type_from_vehicle_type(vehicle_type)
        available_slots = self.__parking_slots.get(parking_slot_type.value)
        for slot in available_slots:
            if not slot.is_occupied:
                assigned_slot = slot
                break
        return assigned_slot

    # This method updates an active ticket for a vehicle when it is unparked.
    # It updates the amount charged, the out time, the payment receipt  and status for the vehicle ticket.
    def __update_ticket(self, out_time, parking_slot_type, vehicle_license_id):
        ticket = self.__active_tickets[vehicle_license_id]
        duration_of_vehicle_park = get_duration_in_hours(ticket.in_time, out_time)
        ticket.out_time = out_time
        ticket.status = ParkingTicketStatus.Paid
        ticket.amount = self.__fee_model_type.get_pricing_for_vehicle(parking_slot_type.value,
                                                                      duration_of_vehicle_park)
        ticket.receipt_id = get_unique_receipt_id()
        return ticket

    # This method takes care of incrementing the occupied slot count (according to vehicle type) when
    # a vehicle is parked in the lot
    def __increment_occupied_parking_slots(self, vehicle_type):
        if vehicle_type == VehicleType.Suv or vehicle_type == VehicleType.Car:
            self.medium_parking_slots_count += 1
        elif vehicle_type == VehicleType.Scooter or vehicle_type == VehicleType.Motorcycle:
            self.small_parking_slots_count += 1
        elif vehicle_type == VehicleType.Bus or vehicle_type == VehicleType.Truck:
            self.large_parking_slots_count += 1

    # This method takes care of decrementing the occupied slot count (according to vehicle type) when
    # a vehicle is unparked/removed from the lot
    def __decrement_occupied_parking_slots(self, parking_slot_type):
        if parking_slot_type == ParkingSlotType.Small:
            self.small_parking_slots_count -= 1
        elif parking_slot_type == ParkingSlotType.Medium:
            self.medium_parking_slots_count -= 1
        elif parking_slot_type == ParkingSlotType.Large:
            self.large_parking_slots_count -= 1

    # This method 'parks' the vehicle in the parking lot.
    # It first checks if a slot is available for the vehicle. If yes, it assigns the slot to
    # the vehicle and generates a ticket for the parked vehicle.
    # Returns the ticket
    def park_vehicle(self, vehicle_license_id, vehicle_type):
        try:
            if self.__check_if_parking_slot_available(vehicle_type):
                print('No space available')
                raise NoSlotAvailableException()
            else:
                slot = self.__get_empty_parking_spot(vehicle_type)
                if slot.slot_id:
                    slot.assign_vehicle_to_spot(vehicle_license_id)
                    ticket = ParkingTicket(slot.slot_id, vehicle_license_id)
                    self.__active_tickets[vehicle_license_id] = ticket
                    self.__occupied_slots[vehicle_license_id] = slot
                    self.__increment_occupied_parking_slots(vehicle_type)
                    print(f'Parking Ticket for Vehicle License ID {vehicle_license_id}, type {vehicle_type.value}:')
                    print(f'\tTicket Number: {ticket.ticket_id}')
                    print(f'\tSpot Number: {ticket.parking_slot_id}')
                    print(f'\tEntry Date-time: {ticket.in_time.strftime("%d-%a-%Y %H:%M:%S")}\n')
                    return ticket
                else:
                    print('No space available')
                    raise NoSlotAvailableException()
        except NoSlotAvailableException as e:
            raise e

    # This method 'unparks' or removes the vehicle from the parking lot.
    # It updates the occupied slot and makes it free. It calculates the charges for the parked time
    # based on the Fee Model and the out time, and updates the ticket accordingly
    # Returns the updated ticket
    def remove_vehicle(self, vehicle_license_id, out_time=datetime.now()):
        try:
            # Get the slot assigned to the given vehicle
            slot = self.__occupied_slots.get(vehicle_license_id)
            if slot:
                slot.remove_vehicle_from_slot()
                del self.__occupied_slots[vehicle_license_id]
                self.__decrement_occupied_parking_slots(slot.parking_slot_type)

                # Get Ticket details, update them and calculate total amount
                ticket = self.__update_ticket(out_time, slot.parking_slot_type, vehicle_license_id)
                print(
                    f'Parking Receipt for Vehicle License ID {vehicle_license_id}, slot type {slot.parking_slot_type.value}:')
                print(f'\tReceipt Number: R-{ticket.receipt_id}')
                print(f'\tEntry Date-time: {ticket.in_time.strftime("%d-%a-%Y %H:%M:%S")}')
                print(f'\tExit Date-time: {out_time.strftime("%d-%a-%Y %H:%M:%S")}')
                print(f'\tFees: {ticket.amount}\n')
                del self.__active_tickets[vehicle_license_id]
                return ticket
            else:
                print(f'Vehicle {vehicle_license_id} is not parked')
        except Exception as e:
            print(e)
            raise e

    # Returns the Occupied Slots
    # Occupied Slots is a dict with the vehicle_license_id as the key and the slot as the value
    def get_occupied_slots(self):
        return self.__occupied_slots

    # Returns the Active Tickets
    # Active Tickets is a dict with the vehicle_license_id as the key and the ticket as the value
    def get_active_tickets(self):
        return self.__active_tickets
