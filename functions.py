from classes import Customer, Dish, Restaurant, Table, Chef, Waiter, Receipt, Delivery, Reservation
import random

def create_restaurants():
    """
    Creates and initializes three sample restaurants with staff, menu, and tables.
    Returns a list of Restaurant objects.
    """
    restaurants = []
    gourment_heven = Restaurant("Gourmet Haven", "Downtown", 4.5, "A fine dining experience with a diverse menu and exceptional service.")
    sushi_world = Restaurant("Sushi World", "Midtown", 4.2, "Authentic Japanese cuisine with a modern twist.")
    pizza_paradise = Restaurant("Pizza Paradise", "Uptown", 4.0, "Best pizzas in town with a variety of toppings.")

    waiter_alex = Waiter("Alex", employee_id=103)
    waiter_juliette = Waiter("Juliette", employee_id=104)
    waiter_mark = Waiter("Mark", employee_id=106)
    chef_john = Chef("John", employee_id=107)
    chef_emily = Chef("Emily", employee_id=108)
    chef_maria = Chef("Maria", employee_id=105)

    restaurants.append(gourment_heven)
    restaurants.append(sushi_world)
    restaurants.append(pizza_paradise)

    # Restaurant 1: Gourmet Haven
    # Add staff members
    restaurants[0].add_staff(waiter_alex)
    restaurants[0].add_staff(chef_maria)

    # Add dishes to the menu
    restaurants[0].add_dish(Dish("Spaghetti Carbonara", 12.99, "Main Course"))
    restaurants[0].add_dish(Dish("Caesar Salad", 8.99, "Appetizer"))
    restaurants[0].add_dish(Dish("Tiramisu", 6.99, "Dessert"))

    # Add tables
    restaurants[0].add_table(Table(1, 4))
    restaurants[0].add_table(Table(2, 2))
    restaurants[0].add_table(Table(3, 6))

    # Restaurant 2: Sushi World
    # Add staff members
    restaurants[1].add_staff(waiter_juliette)
    restaurants[1].add_staff(chef_emily)

    # Add dishes to the menu
    restaurants[1].add_dish(Dish("California Roll", 10.99, "Appetizer"))
    restaurants[1].add_dish(Dish("Dragon Roll", 15.99, "Main Course"))
    restaurants[1].add_dish(Dish("Mochi Ice Cream", 5.99, "Dessert"))

    # Add tables
    restaurants[1].add_table(Table(1, 4))
    restaurants[1].add_table(Table(2, 2))
    restaurants[1].add_table(Table(3, 6))

    # Restaurant 3: Pizza Paradise
    # Add staff members
    restaurants[2].add_staff(waiter_mark)
    restaurants[2].add_staff(chef_john)

    # Add dishes to the menu
    restaurants[2].add_dish(Dish("Margherita Pizza", 12.99, "Main Course"))
    restaurants[2].add_dish(Dish("Caesar Salad", 8.99, "Appetizer"))
    restaurants[2].add_dish(Dish("Tiramisu", 6.99, "Dessert"))

    # Add tables
    restaurants[2].add_table(Table(1, 4))
    restaurants[2].add_table(Table(2, 2))
    restaurants[2].add_table(Table(3, 6))

    return list(restaurants)

def reserve_table(restaurant: Restaurant, customer: Customer, table_number: int):
    """
    Reserves a table for a customer if available.
    Returns a confirmation message or error if table is occupied or doesn't exist.
    """
    for table in restaurant.get_tables():
        if table.get_table_number() == table_number:
            if table.get_availability():
                return customer.assign_table(table)
            else:
                return f"Table {table_number} is currently occupied. Please choose another table."
    return f"Table {table_number} does not exist in {restaurant.get_name()}."

def place_order(restaurant: Restaurant, customer: Customer, dish_name: str, number_of_dishes: int):
    """
    Places an order for a dish if it exists on the menu.
    Returns a confirmation message or error if dish not found.
    """
    for dish in restaurant.get_menu():
        if dish.get_name() == dish_name:
            return customer.place_order(dish, number_of_dishes)
    return f"{dish_name} is not available on the menu at {restaurant.get_name()}."

def generate_receipt(customer: Customer, number_of_dishes: int):
    """
    Generates a receipt for the customer's order.
    Returns the formatted receipt string.
    """
    receipt = Receipt(customer, number_of_dishes)
    return receipt.get_receipt()

def show_menu(restaurant: Restaurant):
    """
    Displays the menu of the restaurant.
    """
    print(f"{restaurant.get_name()} Menu:\n")
    restaurant.show_menu()

def show_staff(restaurant: Restaurant):
    """
    Returns a string listing all staff members in the restaurant.
    """
    staff_members = restaurant.get_staff()
    if not staff_members:
        return "There are no staff members available."
    staff_str = f"Staff at {restaurant.get_name()}:\n"
    for staff in staff_members:
        staff_str += f"- {staff.get_name()} (ID: {staff.get_staff_id()}, Role: {staff.get_role()})\n"
    return staff_str

def show_waiters(restaurant: Restaurant):
    """
    Returns a string listing all waiters in the restaurant.
    """
    waiters = [staff for staff in restaurant.get_staff() if "Waiter" in staff.perform_duty()]
    if not waiters:
        return "There are no waiters available."
    waiters_str = ""
    for waiter in waiters:
        waiters_str += f"- {waiter.get_name()} (ID: {waiter.get_employee_id()})\n"
    return waiters_str

def get_the_number_of_tables(restaurant: Restaurant):
    """
    Returns the number of tables in the restaurant.
    """
    return len(restaurant.get_tables())

def show_tables(restaurant: Restaurant):
    """
    Returns a string listing all tables and their availability.
    """
    tables = restaurant.get_tables()
    if not tables:
        return "There are no tables available."
    tables_str = f"Tables at {restaurant.get_name()}:\n"
    for table in tables:
        availability = "Available" if table.get_availability() else "Occupied"
        tables_str += f"- Table {table.get_table_number()} (Capacity: {table.get_capacity()}) - {availability}\n"
    return tables_str

def create_customer(name: str, customer_id: int):
    """
    Creates a new Customer object.
    """
    return Customer(name, customer_id)

def create_delivery_order(customer: Customer, address: str):
    """
    Creates a delivery order for the customer.
    """
    customer.set_address(address)
    delivery = Delivery(customer)
    print(delivery.place_delivery())
    return delivery

def make_reservation(waiter_id: int, customer: Customer):
    """
    Makes a reservation for the customer with the specified waiter.
    """
    reservation = Reservation(customer, customer.get_table())
    print(reservation.make_reservation()+f" Waiter ID: {waiter_id}")

def assign_waiter_to_customer(restaurant: Restaurant, customer: Customer):
    """
    Assigns the first available waiter to the customer.
    Returns a confirmation message.
    """
    waiter = None
    for staff in restaurant.get_staff():
        if isinstance(staff, Waiter):
            waiter = staff
            break
        if waiter:
            break
    if waiter:
        return f"Waiter {waiter.get_name()} (ID: {waiter.get_employee_id()}) has been assigned to table {customer.get_table_number()}.\n"
    else:
        return "No waiter found."