# importing module
import mysql.connector as con
import time


# Establishing Connection to MySQL
db = con.connect(
    host="localhost",
    user="root",
    password="1234",
    
)


#Making cursor
cursor = db.cursor()
#Creating Databse
cursor.execute("create database if not exists hotel_management")
#using Hotel management Database
cursor.execute("use hotel_management")
# Create a table to store customer records
cursor.execute("CREATE TABLE IF NOT EXISTS customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), room_number INT UNIQUE, total_amount DECIMAL(10, 2))")


# Function to book a room
def booking():
    while True:
        try:
            print("\n----------------------BOOKING------------------------------")
            print()
            name = input("Enter customer name: ")
            room_number = int(input("Enter room number: "))
            total_amount = float(input("Enter total amount: "))
            print()
            cursor.execute("INSERT INTO customers (name, room_number, total_amount) VALUES (%s, %s, %s)", (name, room_number, total_amount))
            db.commit()
            print("\nThank You.............")
            print()
            print("Booking successful!\n")
            print()
            print("Enter y to Enter Another Entry")
            print("Enter any other Key To exit.")
            ch=input("Enter your choice : ")
            if ch.lower()=="y":
                print()
                continue
            else:
                print()
                break
        except:
            print("Invalid Choice....!")
            print("Try Again")
            print("------------------------")
            continue


# Function to get Room information
def room_info():
    try:
        print("\n------------------------ROOM INFORMATION------------------------")
        print()
        room_number = int(input("Enter room number: "))
        cursor.execute("SELECT * FROM customers WHERE room_number = %s", (room_number,))
        result = cursor.fetchone()
        if result:
            print(f"Customer Name: {result[1]} | Room Number: {result[2]} | Total Amount: {result[3]}")
            print()
        else:
            print()
            print("Room not booked.")
            print()
    except:
        print("Invalid Choice....")
        print()
        print("Press y to continue")
        print("\nPress any other button to break")
        ch=input(" \nEnter your choice")
        if ch=="y":
            restaurant()
        else:
            pass


# Function for ordering Food from the restaurant
def restaurant():
    #menu 
    print("\n----------------------MENU-----------------------------\n")
    menu = {"1": ("Burger", 299.99),
             "2": ("Pizza-Medium", 599.99),
               "3": ("Pasta", 199.99),
               "4":("Veg Thali",149.95),
               "5":("Non Veg Thali",249.99),
               "6":("Soft Drink",69.99),
               "7":("Fried rice",99.99),
               "8":("Chowmein",70.00),
               "9":("Manchurian",140.00),
               "10":("Ice-creams",120.00),
               "11":("Sweets",99.99),
               "12":("Chicken-Tikka",349.00),
               "13":("Handi Mutton",399.00)
               }
    #Showing Foods menu
    print()
    for item, (name, price) in menu.items():
        print(f"{item}. {name} - ₹{price}")
    print()
    try:
        order = input("Enter the item number to order: ")
        quantity = int(input("Enter quantity: "))
        print()
        room=int(input("Enter your Room Number: "))
        print("Foods will be delivered to your Room...")
        print()

        total_price = menu[order][1] * quantity
        cursor.execute(f"update customers set total_amount=total_amount+{total_price} where room_number={room}")
        db.commit()

        print(f"Order placed: {menu[order][0]} | Quantity: {quantity} | Total Price: ₹{total_price}")
        print("\nThe Amount will be added to Room Booking Fees....\n")
        print("Happy Meal\n")
        print()
    except:
        print("Invalid Choice....")
        print()
        print("Press y to continue")
        print("Press any other button to break")
        ch=input(" \nEnter your choice: ")
        print()
        if ch=="y":
            restaurant()
        else:
            pass


# Function for payment
def payment():
    try:
        print("\n-----------------------------CHECKOUT---------------------------------------")
        print()
        room_number = int(input("Enter room number for payment: "))
        cursor.execute("SELECT total_amount FROM customers WHERE room_number = %s", (room_number,))
        result = cursor.fetchone()

        if result:
            total_amount = result[0]
            print()
            print(f"Total Amount to Pay: ₹{total_amount}")
            print()
            print("Press Yes to Proceed with Payment")
            print("Press any key to exit")
            print()
            u=input("\nEnter your Choice: ")
            print()
            if u.lower()=="yes":
                print("Transaction in Progress...")
                time.sleep(1)
                print("Done")
                time.sleep(1)
                print("Thanks for Visiting")
                print()
                cursor.execute(f"delete from customers where room_number={room_number}")
                print()
                db.commit()
        else:
            print("\nRoom not found.\n")
    except:
        print("Invalid Choice....")
        print()
        print("Press y to continue")
        print("\nPress n to break")
        ch=input(" \nEnter your choice")
        if ch=="y":
            payment()
        else:
            pass


# Function to record customer details
def record():
    cursor.execute("SELECT * FROM customers")
    results = cursor.fetchall()
    if results:
        print("\nCustomer Records:")
        for row in results:
            print(f"ID: {row[0]} | Name: {row[1]} | Room Number: {row[2]} | Total Amount: {row[3]}")
        print()
    else:
        print("\nNo records found.\n")


#USER LOGIN PORTAL
def user_login():
    while True:
        print("\n-----------------------------------------------------------------")
        print("                           USER PORTAL                           ")
        print("-----------------------------------------------------------------\n")
        print("1.Get Room Info")
        print("2.Restaurant")
        print("3.To Checkout")
        print("0.Exit")
        try:
            print()
            ch=int(input("Enter your Choice: "))
            if ch==1:
                room_info()
            elif ch==2:
                restaurant()  
            elif ch==0:
                print("Logging out")
                print()
                break
            elif ch==3:
                payment()
            else:
                print("Invalid Choice")
                print()
        except Exception as e:
            print("Invalid Choice\nTry Again..\n")
            print()
            continue


#ADMIN LOGIN PORTAL
def admin_login():
    while True:
        print("\n-------------------------------------------------------------")
        print("                       ADMIN LOGIN                           ")
        print("-------------------------------------------------------------")
        print()
        print("1.Book Room")
        print("2.To show Records")
        print("0.Exit\n")
        try:
            ch=int(input("Enter your Choice: "))
            print()
            if ch==1:
                booking()
            elif ch==2:
                record()
            elif ch==0:
                print("Logging out")
                time.sleep(1)
                print("Thank you...")
                time.sleep(1)
                print("  ")
                break
            else:
                print()
                print("Invalid choice\n")

        except:

            print("\nInvalid Choice...!\n")
            continue


# Main program 
while True:
    print("\n-----------------------------------------------------------------------------------------")
    print("|                                 HOTEL MANAGEMENT SYSTEM                               |")
    print("-----------------------------------------------------------------------------------------")
    print()
    print("1.Admin Login")
    print("2.User Login")
    print("0.Exit\n")
    try:
        choice=int(input("Enter your choice: "))
        print()
        if choice==1:
            admin_login()

        elif choice==2:
            user_login()

        elif choice==0:
            print("Thanks for visiting...\n")
            break
        else:
            print("\nInvalid Choice.....")
            print("Try Again!\n")
            print()
            continue
    except:
        print("Try Again!")
        continue 


#closing Databse connection   
db.close()
