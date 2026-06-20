"""
Main module for the Restaurant Management System.
This program allows users to select a restaurant, place orders (delivery, sit-in, or reservation),
and generate receipts.
"""

import functions
from tabulate import tabulate
import random
from datetime import datetime as date

if __name__ == "__main__":
    # Initialize restaurants and data
    restaurants = functions.create_restaurants()
    resto_option = int
    order_type = int
    table_number = int

    # Display restaurant information
    data = [["Options","Restaurant Names","Locations","Ratings","Descriptions"]]
    for index in range(len(restaurants)):
        restaurant = restaurants[index]
        restaurant_name = restaurant.get_name()
        location = restaurant.get_location()
        rating = restaurant.get_rating()
        description = restaurant.get_description()
        data += [[index+1,restaurant_name,location,rating,description]]

    # Print with the first row as headers and a 'fancy_grid' format
    print(tabulate(data, headers="firstrow", tablefmt="fancy_grid"))
    print("")

    # Make a reservation or place an order
    while resto_option not in [1, 2, 3]: # Loop until a valid restaurant option is selected
        try:
            resto_option = int(input("Please select a restaurant by entering the corresponding number (1-3): ")) # Prompt user to select a restaurant
            print("")
            if resto_option not in [1, 2, 3]:
                print("Invalid option. Please enter a number between 1 and 3.\n")
            else:
                selected_restaurant = restaurants[resto_option - 1] # Get the selected restaurant object
                print(f"You have selected {selected_restaurant.get_name()}.\n")

                # Get customer details
                customer_name = input("To place an order, please enter your name or enter 0 to cancel: ")
                print("")
                if customer_name == "0":
                    print("Reservation cancelled.\n")
                    continue # Skip the rest of the loop and prompt for restaurant selection again
                else:
                    customer_id = random.randint(1000, 9999)  # Generate a random customer ID
                    customer = functions.create_customer(customer_name, customer_id) # Create a new customer object
                    # Prompt user to select order type
                    while order_type not in [1, 2, 3, 4]: # Loop until a valid order type is selected
                        try: # Loop until a valid order type is selected
                            print("1- Place a delivery order")
                            print("2- Place a sit-in order")
                            print("3- Make a reservation")
                            print("4- Cancel")
                            print("")
                            order_type = int(input("Enter 1, 2, 3 or 4: ")) # Prompt user to select order type
                            print("")
                            if order_type not in [1, 2, 3, 4]:
                                print("Invalid option. Please enter 1, 2, 3 or 4.\n")
                            # Place a delivery order
                            elif order_type == 1:
                                numbers = [] # List to store the number of dishes ordered for each dish
                                user_input = "yes"
                                while user_input.lower() != "no": # Loop until the user decides to stop ordering
                                    # Delivery order
                                    functions.show_menu(selected_restaurant) # Display the menu of the selected restaurant
                                    print("")
                                    # Place an order
                                    while True: # Loop until a valid dish name is entered
                                        dish_name = input("Enter the name of the dish you want to order: ") # Prompt user to enter the name of the dish they want to order
                                        print("")
                                        if dish_name.strip() != "": # Check if the input is not empty
                                            for dish in selected_restaurant.get_menu():
                                                found = False
                                                if len(dish_name) > 4:
                                                    if dish_name in dish.get_name():
                                                        found = True
                                                        dish_name = dish.get_name()
                                                        break
                                                else:                                        
                                                    print("Please enter at least 5 characters to search for a dish.")
                                                    print("")
                                            if found:
                                                try:
                                                    number_of_dishes = int(input(f"Enter the number of {dish_name} you want to order: "))
                                                    print("")
                                                except ValueError: # Loop until a valid number of dishes is entered
                                                    print("Invalid input. Please enter a valid number.")
                                                    print("")
                                                    continue
                                                numbers.append(number_of_dishes) # Add the number of dishes ordered to the list
                                                order_confirmation = functions.place_order(selected_restaurant, customer, dish.get_name(), number_of_dishes) # Place the order and get the confirmation message
                                                print(order_confirmation)
                                                print("")
                                                user_input = input("Do you want to order another dish? (yes/no): ")
                                                print("")
                                                if user_input.lower() != "yes":
                                                    break
                                            else:
                                                print("Dish not found.")
                                                print("")
                                            break
                                        else:
                                            print("Input cannot be empty. Please enter a valid dish name.")
                                            print("")
                                # Get delivery address
                                address = input("Enter your delivery address: ")
                                print("")
                                # Generate receipt
                                receipt = functions.generate_receipt(customer,numbers) # Generate a receipt for the customer's order
                                print(receipt)
                                print("")
                                # Schedule delivery
                                delivery = functions.create_delivery_order(customer, address) # Create a delivery order for the customer
                            # Sit-in order
                            elif order_type == 2:
                                numbers = []
                                functions.show_menu(selected_restaurant) # Display the menu of the selected restaurant
                                print("")
                                # Place an order
                                while True:
                                    dish_name = input("Enter the name of the dish you want to order: ")
                                    print("")
                                    if dish_name.strip() != "":
                                        for dish in selected_restaurant.get_menu(): # Loop through the menu to find the dish that matches the user's input
                                            found = False
                                            if len(dish_name) > 4: # Check if the input is at least 5 characters long to avoid too broad search results
                                                if dish_name in dish.get_name():
                                                    found = True
                                                    dish_name = dish.get_name()
                                                    break
                                            else:                                        
                                                print("Please enter at least 5 characters to search for a dish.")
                                                print("")
                                        if found:
                                            try:
                                                number_of_dishes = int(input(f"Enter the number of {dish_name} you want to order: "))
                                                print("")
                                            except ValueError:
                                                print("Invalid input. Please enter a valid number.")
                                                print("")
                                                continue
                                            numbers.append(number_of_dishes)
                                            order_confirmation = functions.place_order(selected_restaurant, customer, dish.get_name(), number_of_dishes) # Place the order and get the confirmation message
                                            print(order_confirmation)
                                            print("")
                                            user_input = input("Do you want to order another dish? (yes/no): ")
                                            print("")
                                            if user_input.lower() != "yes":
                                                break
                                        else:
                                            print("Dish not found.")
                                            print("")
                                        break
                                    else:
                                        print("Input cannot be empty. Please enter a valid dish name.")
                                        print("")
                                print(functions.show_tables(selected_restaurant)) # Display the available tables in the restaurant
                                # Reserve a table
                                while table_number not in range(1, functions.get_the_number_of_tables(selected_restaurant) + 1): # Loop until a valid table number is entered
                                    try:
                                        table_number = int(input("Enter the table number you want to reserve: "))
                                        print("")
                                        if table_number not in range(1, functions.get_the_number_of_tables(selected_restaurant) + 1):
                                            print(f"Invalid table number. Please enter a number between 1 and {functions.get_the_number_of_tables(selected_restaurant)}.\n")
                                            print("")
                                    except ValueError:
                                        print("Invalid input. Please enter a valid number.")
                                        print("")
                                reservation_confirmation = functions.reserve_table(selected_restaurant, customer, table_number) # Reserve the table and get the confirmation message
                                # Assign a waiter to the customer
                                waiter = functions.assign_waiter_to_customer(selected_restaurant, customer) # Assign a waiter to the customer and get the waiter's information
                                print(reservation_confirmation)
                                print(waiter)
                                # Generate receipt
                                receipt = functions.generate_receipt(customer,numbers)
                                print(receipt)
                                print("")
                            # Make a reservation
                            elif order_type == 3:
                                # display tables
                                print(functions.show_tables(selected_restaurant))
                                # Reserve a table
                                while table_number not in range(1, functions.get_the_number_of_tables(selected_restaurant) + 1):
                                    try:
                                        table_number = int(input("Enter the table number you want to reserve: "))
                                        print("")
                                        if table_number not in range(1, functions.get_the_number_of_tables(selected_restaurant) + 1):
                                            print(f"Invalid table number. Please enter a number between 1 and {functions.get_the_number_of_tables(selected_restaurant)}.\n")
                                            print("")
                                    except ValueError:
                                        print("Invalid input. Please enter a valid number.")
                                        print("")
                                # Choose a reservation date
                                reservation_date = date.strptime(input("Enter the reservation date (YYYY-MM-DD): "), "%Y-%m-%d")
                                print("")
                                #choose a waiter
                                print("Available waiters:")
                                print("")
                                print(functions.show_waiters(selected_restaurant))
                                try:
                                    waiter_id = int(input("Enter the waiter ID you want to assign: "))
                                    print("")
                                except ValueError:
                                    print("Invalid input. Please enter a valid number.")
                                    print("")
                                # Display reservation confirmation
                                reservation_confirmation = functions.reserve_table(selected_restaurant, customer, table_number)
                                print(reservation_confirmation)
                                print("")
                                functions.make_reservation(waiter_id, customer)
                            elif order_type == 4:
                                print("Thank you for your interest, hope to see you soon.\n")
                                continue
                        except ValueError:
                            print("Invalid input. Please enter a valid number.\n")            
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")
    print("Thank you for using the Restaurant Management System. Goodbye!\n")
