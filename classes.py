import datetime

class Staff:
    """
    Base class for all staff members in the restaurant.
    """
    def __init__(self, name: str, employee_id: int):
        self._employee_id = employee_id
        self._name = name

    def get_employee_id(self) -> int:
        return self._employee_id

    def get_name(self) -> str:
        return self._name

    def describe(self):
        return f"Staff: {self._name}, ID: {self._employee_id}"

    def perform_duty(self):
        raise NotImplementedError("Subclasses must implement perform_duty()")


class Chef(Staff):
    """
    Represents a chef in the restaurant.
    """
    def perform_duty(self):
        return f"Chef {self._name}, ID: {self._employee_id} is cooking dishes."


class Waiter(Staff):
    """
    Represents a waiter in the restaurant.
    """
    def perform_duty(self):
        return f"Waiter {self._name}, ID: {self._employee_id} is serving guests."

class Dish:
    """
    Represents a dish on the restaurant menu.
    """
    def __init__(self, name: str, price: float, category: str):
        self._name = name
        self._category = category
        self._price = price

    def get_name(self):
        return self._name

    def get_category(self):
        return self._category

    def get_price(self):
        return self._price

    def describe(self):
        return f"{self._name} ({self._category}): RM{self._price:.2f}"

class Table:
    """
    Represents a table in the restaurant.
    """
    def __init__(self, table_number: int, capacity: int):
        self._table_number = table_number
        self._capacity = capacity
        self.__available = True

    def get_table_number(self) -> int:
        return self._table_number

    def get_capacity(self) -> int:
        return self._capacity

    def get_availability(self) -> bool:
        return self.__available
    
    def occupy(self):
        self.__available = False

class Customer:
    """
    Represents a customer in the restaurant system.
    """
    def __init__(self, name: str, customer_id: int):
        self._name = name
        self._customer_id = customer_id
        self._address = None
        self.__table = None
        self.__order_history = []
        self.__has_reservation = False
        self.__balance = 0.0

    def get_customer_id(self) -> int:
        return self._customer_id
    
    def get_name(self) -> str:
        return self._name
    
    def get_table(self):
        return self.__table

    def get_table_number(self) -> int:
        return self.__table.get_table_number()

    def get_balance(self) -> float:
        return self.__balance       
    
    def get_reservation(self) -> bool:
        return self.__has_reservation
    
    def get_address(self) -> str:
        return self._address
    
    def assign_table(self, table: Table):
        self.__table = table
        table.occupy()
        return f"{self._name} has been assigned to Table {table.get_table_number()}.\n"

    def place_order(self, dish: Dish, number_of_dishes: int):
        self.__order_history.append(dish)
        self.__balance += dish.get_price() * number_of_dishes
        return f"{self._name} ordered {number_of_dishes} x {dish.get_name()}: RM{dish.get_price() * number_of_dishes:.2f}"

    def order_history(self):
        return list(self.__order_history)

    def describe(self):
        return f"Customer: {self._name}, ID: {self._customer_id}, Balance: ${self.__balance:.2f}"

    def make_reservation(self):
        self.__has_reservation = True
        return f"{self._name} has made a reservation."
    
    def set_address(self, address: str):
        self._address = address

class Receipt:
    """
    Represents a receipt for a customer's order.
    """
    def __init__(self, customer: Customer, number_of_dishes: int):
        self._customer = customer
        self._number_of_dishes = number_of_dishes

    def get_receipt(self):
        if self._customer.get_table() != None:
            table_info = self._customer.get_table_number()
        else:
            table_info = "N/A"
        receipt = f"Receipt for {self._customer.get_name()} (ID: {self._customer.get_customer_id()}) (Table: {table_info}):\n"
        receipt += "================================\n"
        receipt += "Ordered Dishes:\n"
        dishes = self._customer.order_history()
        for index in range(len(dishes)):
            dish = dishes[index]
            receipt += f"{dish.describe()} x {self._number_of_dishes[index]}\n"
        receipt += "================================\n"
        receipt += f"Total: RM{self._customer.get_balance():.2f}"
        return receipt

class Restaurant:
    """
    Represents a restaurant with staff, menu, tables, and customers.
    """
    def __init__(self, name: str, location: str, rating: float, description: str):
        self._name = name
        self._location = location
        self._rating = rating
        self._description = description
        self.__staff = []
        self.__customers = []
        self.__menu = []
        self.__tables = []

    def get_name(self):
        return self._name
    
    def get_location(self):
        return self._location
    
    def get_rating(self):
        return self._rating

    def get_description(self):
        return self._description

    def get_staff(self):
        return list(self.__staff)
    
    def get_customers(self):
        return list(self.__customers)
    
    def get_tables(self):
        return list(self.__tables)
    
    def get_menu(self):
        return list(self.__menu)

    def add_staff(self, staff_member: Staff):
        self.__staff.append(staff_member)

    def add_customer(self, customer: Customer):
        self.__customers.append(customer)

    def add_dish(self, dish: Dish):
        self.__menu.append(dish)

    def show_menu(self):
        for dish in self.__menu:
            if dish is not None:
                print(f"  - {dish.describe()}")

    def open_service(self):
        duties = [staff.perform_duty() for staff in self.__staff]
        return duties
    
    def add_table(self, table: Table):
        self.__tables.append(table)

class Reservation:
    """
    Represents a reservation made by a customer.
    """
    def __init__(self, customer: Customer, table: Table):
        self._customer = customer
        self._table = table
        self._time = self._time = datetime.datetime.now()

    def get_customer(self):
        return self._customer

    def get_table(self):
        return self._table

    def get_time(self):
        return self._time
    
    def make_reservation(self):
        self._customer.make_reservation()
        return f"Reservation for {self._customer.get_name()} at Table {self._table.get_table_number()} for {self._time.strftime('%Y-%m-%d')}"
    
class Delivery:
    """
    Represents a delivery order for a customer.
    """
    def __init__(self, customer: Customer):
        self._customer = customer
        self._address = customer.get_address()
        self._time = datetime.datetime.now() + datetime.timedelta(hours=1)  # Assuming delivery takes 1 hour

    def get_customer(self):
        return self._customer

    def get_address(self):
        return self._address

    def get_time(self):
        return self._time
    
    def place_delivery(self):
        return f"Delivery for {self._customer.get_name()} to {self._address} on {self._time.strftime('%Y-%m-%d')} at {self._time.strftime('%H:%M:%S')}\n"