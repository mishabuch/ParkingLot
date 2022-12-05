from datetime import datetime

from parking_lot.utils.constants import ParkingTicketStatus
from parking_lot.utils.utils import get_unique_ticket_id


# Parking Ticket represents the parking ticket issues for any vehicle parked
# It has the unique ticket id, the in time and out time of the car, the slot id and the vehicle id of the parked
# vehicle. It has the amount charged for parking when the car is unparked
# It also has the receipt id of the receipt generated on successful payment of the parking charges
# Ticket can be either ACTIVE - i.e car is parked or it can be PAID - which means car is unparked

class ParkingTicket:
    def __init__(self, parking_slot_id, vehicle_license_id):
        self.ticket_id = get_unique_ticket_id()
        self.in_time = datetime.now()
        self.out_time = None
        self.parking_slot_id = parking_slot_id
        self.vehicle_license_id = vehicle_license_id
        self.amount = 0
        self.receipt_id = None
        self.status = ParkingTicketStatus.Active
