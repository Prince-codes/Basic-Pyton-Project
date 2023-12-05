import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234"
 
)

#MAking Database
cursor = db.cursor()
cursor.execute("create database if not exists event_management")
cursor.execute("use event_management")

# Creating tables
cursor.execute("CREATE TABLE IF NOT EXISTS events (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS bookings (id INT AUTO_INCREMENT PRIMARY KEY, event_id INT, user_id INT, FOREIGN KEY (event_id) REFERENCES events(id), FOREIGN KEY (user_id) REFERENCES users(id), date DATE, location VARCHAR(255))")


# Function to manage events in admin panel
def manage_events():
    print()
    
    while True:
        try:
            print("\n1. Add Event")
            print("2. View All Events")
            print("3.Exit\n")
            choice = int(input("Enter your choice: "))
            print()

            if choice == 1:
                name = input("Enter event name: ")
                cursor.execute("INSERT INTO events (name) VALUES (%s)", (name,))
                db.commit()
                print("Event added successfully!")

            elif choice == 2:
                cursor.execute("SELECT * FROM events")
                events = cursor.fetchall()

                if not events:
                    print("No events available.")
                else:
                    print("All Events:")
                    for event in events:
                        print(f"Event ID: {event[0]}, Name: {event[1]}")
            elif choice==3:
                print()
                print("Thank You.........\n")
                break
        except:
            print("\nError Occured......\n")
    
          
        
# Function to manage event bookings in admin panel
def manage_event_bookings():
    print()

    while True:
        
        try:
            event_id = input("Enter Event ID: ")
            cursor.execute("SELECT * FROM bookings WHERE event_id = %s", (event_id,))
            bookings = cursor.fetchall()

            if not bookings:
                print()
                print("No bookings for this event.\n")
                break
            else:
                print("\nEvent Bookings:\n")
                for booking in bookings:
                    print(f"Booking ID: {booking[0]}, Event ID: {booking[1]}, User ID: {booking[2]}, Date: {booking[3]}, Location: {booking[4]}")
                print()
                break
        except :
            print("Error  Try Again .........")
            continue
    
    
    
# Function for user registration
def register_user():
    print()
    username = input("Enter your USERNAME Want to keep : ")
    password = input("Enter your password Want to keep : ")
    print()
    while True:
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            print(f"Registration successful!  Your username : {username} & your password : {password}. \n")
            break
        except :
            print()
            print("Error Occurred....")
            print("Try Again...........\n")
            


# Function for user login
def login_user():
    print()
    username = input("Enter your username : ")
    password = input("Enter your password : ")
    print()

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        print("\nLogin successful!\n")
        return user[0]
    else:
        print("Invalid credentials. Please try again.")
        return None

# Function for user to view all events
def view_all_events():
    print()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    try:
        if not events:
            print("\nNo events available.\n")
        else:
            print("\nAll Events :\n")
            for event in events:
                print(f"Event ID: {event[0]}, Name: {event[1]}")
            print()
    except :
        print("\nError Occured ....\n")

# Function for user to book an event
def book_event(user_id):
    print()
    while True:
        try:
            view_all_events()
            
            event_id = input("Enter the Event ID you want to book: ")
            date = input("Enter event date (YYYY-MM-DD): ")
            location = input("Enter event location: ")

            cursor.execute("INSERT INTO bookings (event_id, user_id,date,location) VALUES (%s, %s, %s, %s)", (event_id, user_id,date,location))
            db.commit()
            
            print("\nBooking successful!\n")
            
        except :
            print("Error Try again........")
            
        r=input("Enter Y to preceed X to exit    :")
        if r=='y' or r=='Y':
            continue
        else:
            break
     
     
#User Portal Defining        
def user_login():
    
    while True:
        try:
            print()
            print("""
------------------------------------------------------------------
                    USER PORTAL
------------------------------------------------------------------      
                """)
            print()
            print("ENTER 1. : TO Register")
            print("ENTER 2. : TO Login")
            print("ENTER 0. : TO Exit\n")
            
            user_choice = int(input("Enter your choice: "))
            print()
            
            if user_choice == 1:
                register_user()
            
            elif user_choice == 2:
                
                user_id = login_user()
                
                if user_id is not None:
                    
                    while True:
                        print("\nUser Options:\n")
                        print("ENTER 1. : To View All Events")
                        print("ENTER 2. : To Book Event")
                        print("ENTER 0. : To Exit\n")
                        
                        user_option = int(input("Enter your choice : "))
                        print()
                        
                        if user_option == 1:
                            view_all_events()
                            
                        elif user_option == 2:
                            book_event(user_id)
                        
                        elif user_option==0:
                            print("Thank You...........")
                            break
                        else:
                            print("Wrong Input......")

            
                
            elif user_choice==0:
                break
            
        except :
            print("Error try again ........")
             
#Admin Portal Defining             
def admin_login():
    while True:
        
        try:
            print()
            print("""
------------------------------------------------------------------
                        ADMIN
------------------------------------------------------------------      

                """)
            print()
            print("1. Manage Events")
            print("2. Manage Event Bookings")
            print("0. Exit\n")
            
            admin_choice = input("Enter your choice: ")

            if admin_choice == "1":
                manage_events()
                
            elif admin_choice == "2":
                manage_event_bookings()
                
            elif admin_choice=="0":
                break
            
        except :
            print("Error try again ............") 
               
# Main program
while True:
    try:
        print()
        print("""
------------------------------------------------------------------
                    EVENT MANAGEMENT
------------------------------------------------------------------      
                """)  
        
        print("\n1. Admin Panel")
        print("2. User Panel")
        print("3. Exit\n")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            admin_login()
        elif choice == "2":
                user_login()

        elif choice == "3":
            print("Exiting program........")
            print("Thank You........")
            break
        
    except :
        print("Error try again ..........")
     
# Close the database connection
db.close()
