# Parking Lot 
This project is for coming up with a generic parking lot which can be used for different areas, buildings and utilities like Malls, Airports, Stadiums etc.

### Class Diagram of the Parking Lot
![Parking Lot Class Diagram](https://drive.google.com/uc?id=1OpeT1mbyGGbwoKwwfmmw2s71npXgcd6w)  

### Project Structure
The Parking Lot project contains following file structure
* parking_lot
    * parking_lot.py
    * parking_slot.py
    * parking_ticket.py
    * vehicle.py
    * FeeModels
        * Airport Fee Model
        * Mall Fee Model
        * Stadium Fee Model
    * Exceptions
        * NoSlotAvailableException
        * VehicleNotAllowedException
* tests
    * test_scenarios_from_project_requirement_doc
        * Multiple files representing 4 the scenarios in the project description doc
    * test_airport_fee_model.py
    * test_mall_fee_model.py
    * test_parking_lot.py
    * test_parking_slot.py
    * test_stadium_fee_model.py

### Running / Testing the parking Lot
All testing of the Parking Lot system is done through Unit tests. In order to run the tests, you can run 'python -m unittest' from inside the ParkinLot directory on the terminal. This would automatically detect all the 30 tests and run them.
To run any individual test file, run the command 'python -m unittest path/to/file'
Code Coverage focus is on testing all the functionalities of the Parking Lot, and covering corner cases, rather than just focusing on Line Coverage. Code Coverage is 94%.

- Each file under the folder tests/test_scenarios_from_project_requirement_doc/ represents tests for a scenario mentioned in the Problem Statement. i.e Scenario 1,2,3 and 4
- Other files under tests/ are general unit tests, which verify the functionalities of each class files and fell models.

#### Assumptions:
- A smaller vehicle cannot be parked in a larger slot, even when slots for smaller vehicles are full, and slots for larger vehicles are free.
- There is only one entry and exit to the parking slot, hence multiple vehicles cannot enter or exit at the same time.
- We assume that the ticket charges are paid for when the vehicle is unparked.

#### Note:
In the test scenarios mentioned in the project writeup, the last scenario for an Airport parking lot, the list of max vehicles allowed says Buses/Trucks: 100 spots. But the Airport fee model doesnot allow any Bus/Truck parking. Here, I assume that Bus/Trucks are not allowed and ignore the 100 spots.
