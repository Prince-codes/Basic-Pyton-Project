import mysql.connector as con
import time 
# Establish a MySQL connection
conn = con.connect(
    host="localhost",
    user="root",
    password="1234",
)

# Create a cursor object
cursor = conn.cursor()
cursor.execute("Create database if not exists library_management")
cursor.execute("use library_management")
cursor.execute("create table if not exists books(book_id int auto_increment primary key  ,title varchar(35),author varchar(25),available_copies int(2))")
cursor.execute("create table if not exists borrowed_books(user_id int(2),book_id int(2))")
cursor.execute("create table if not exists returned_books(user_id int(2),book_id int(2))")
cursor.execute("create table if not exists users(name VARCHAR(255) NOT NULL,user_id int primary key auto_increment)")

#USER FUNCTIONS

# Function to display all books
def display_books():
    print("\n---------------------------\n")
    print("Books\n")
    # Retrieve and display all books from the database
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    for book in books:
        print(f"Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Available Copies: {book[3]}")
        print()
    print("---------------------------\n")

# Function to search for books by title
def search_books():
    print("\n------------------------\n")
    title = input("Enter the title of the book to search: ")
    # Search for books with the given title in the database
    cursor.execute("SELECT * FROM books WHERE title = %s", (title,))
    books = cursor.fetchall()
    if books:
        for book in books:
            print(f"Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Available Copies: {book[3]}")
    else:
        print("Book not found.")
    print("---------------------------\n")
# Function to borrow books
def borrow_books():
    print("\n--------------------------\n")
    user_id = input("Enter your user ID: ")
    cursor.execute("select name from users where user_id=%s",(user_id,))
    print()
    a=cursor.fetchone()
    if a==None:
        print("Id doesnt exist")
        pass
    else:
        print(f'Welcome {a[0]}')
        book_id = input("Enter the book ID you want to borrow: ")
        print()
        try:
            # Check if the book is available
            cursor.execute("SELECT available_copies FROM books WHERE book_id = %s", (book_id,))
            available_copies = cursor.fetchone()[0]
            if available_copies==None:
                print("Sorry book doesnt exist...")
                pass
            else:
                if available_copies > 0:
                    # Borrow the book
                    cursor.execute("INSERT INTO borrowed_books (user_id, book_id) VALUES (%s, %s)", (user_id, book_id))
                    cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s", (book_id,))
                    conn.commit()
                    print("Book successfully borrowed.")
                else:
                    print("Sorry, the book is not available for borrowing.")
        except:
            print("Book id doesnt Exist...")
            print(f"try again {a[0]}...")
    print('--------------------------------------------\n')       

# Function to return books
def return_books():
    user_id = input("Enter your user ID: ")
    print()
    cursor.execute("select name from users where user_id=%s",(user_id,))
    a=cursor.fetchone()
    if a==None:
        print("Id doesnt exist")
        pass
    else:
        print(f'Welcome {a[0]}')
        book_id = input("Enter the book ID you want to return: ")
        print()
        # Check if the user has borrowed the book
        cursor.execute("SELECT * FROM borrowed_books WHERE user_id = %s AND book_id = %s", (user_id, book_id))
        if cursor.fetchone():
            # Return the book
            cursor.execute("DELETE FROM borrowed_books WHERE user_id = %s AND book_id = %s", (user_id, book_id))
            cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE book_id = %s", (book_id,))
            conn.commit()
            print("Book successfully returned.")
        else:
            print("You have not borrowed this book.")

    print('------------------------------------\n')       


# Function for the public user portal
def public_portal():
   
        # Display options for the public user
        print("--------------------------------------------------------------------------------------------\n")
        print(''' 
 __    __       _______. _______ .______      
|  |  |  |     /       ||   ____||   _  \     
|  |  |  |    |   (----`|  |__   |  |_)  |    
|  |  |  |     \   \    |   __|  |      /     
|  `--'  | .----)   |   |  |____ |  |\  \----.
 \______/  |_______/    |_______|| _| `._____|
                                              
                                                        
''')
        print("\n------------------------------------------------------------------------------------------\n")
        while True:    
            print("1. Display Books")
            print("2. Search Books")
            print("3. Borrow Books")
            print("4. Return Books")
            print("5. Exit")
            print()
            choice = input("Enter your choice: ")

            # Perform actions based on user choice
            if choice == "1":
                display_books()
            elif choice == "2":
                search_books()
            elif choice == "3":
                borrow_books()
            elif choice == "4":
                return_books()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
                print('------------------------------------\n')       


#Admin Functions

# Function for the admin portal
def admin_portal():
    
        # Display options for the admin
        print("---------------------------------------------------------------------------------------\n")
        print(''' 
     ___       _______  .___  ___.  __  .__   __. 
    /   \     |       \ |   \/   | |  | |  \ |  | 
   /  ^  \    |  .--.  ||  \  /  | |  | |   \|  | 
  /  /_\  \   |  |  |  ||  |\/|  | |  | |  . `  | 
 /  _____  \  |  '--'  ||  |  |  | |  | |  |\   | 
/__/     \__\ |_______/ |__|  |__| |__| |__| \__| 
                                                  
              ''')
        print("\n--------------------------------------------------------------------------------------\n")
        
        while True:
            print("1. Display Users")
            print("2. Books Borrowed")
            print("3. Books Returned")
            print("4. Add New Users")
            print("5. Add Books")
            print("0. Exit")
            choice = input("Enter your choice: ")

            # Perform admin actions based on choice
            if choice == "1":
                show_users()
            elif choice == "2":
                count_borrowed_books()
            elif choice == "3":
                count_returned_books()
            elif choice == "4":
                add_new_user()
            elif choice=="5":
                add_books()
            elif choice == "0":
                print(" ")
                break
            else:
                print("Invalid choice. Please try again.")

                print('------------------------------------\n')       


# Function to count the number of users
def show_users():
    print("\n---------------------------\n")
    # Retrieve and display the number of users from the database
    cursor.execute("SELECT * FROM users")
    count = cursor.fetchall()
    print("User ID \t User_Name")
    for user in count:
        print(f"{user[1]}\t\t{user[0]}")
    print("---------------------------------\n")

# Function to count the number of borrowed books
def count_borrowed_books():
    print("\n---------------------------\n")
    # Retrieve and display the number of books borrowed from the database
    cursor.execute("SELECT COUNT(*) FROM borrowed_books")
    count = cursor.fetchone()[0]
    print(f"Total number of books borrowed: {count}")
    print('--------------------------\n')
# Function to count the number of returned books
def count_returned_books():
    print("\n---------------------------\n")
    # Retrieve and display the number of books returned from the database
    cursor.execute("SELECT COUNT(*) FROM borrowed_books")
    count_borrowed = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM returned_books")
    count_returned = cursor.fetchone()[0]
    print(f"Total number of books returned: {count_returned}/{count_borrowed}")
    print("---------------------------------------\n")
# Function to add a new user
def add_new_user():
    print("\n---------------------------\n")
    while True:
        name = input("Enter the name of the new user: ")
        if name=='':
            print("Blank input please retry....!")
            continue
        print()
        try:
        # Add the new user to the database
            cursor.execute("INSERT INTO users (name) value (%s)", (name,))
            conn.commit()
            print()
            print("New user added successfully.")
            print("Here is a preview!")
            print()
            cursor.execute("select * from users")
            users=cursor.fetchall()
            print("User ID \t User_Name")
            for user in users:
                print(f"{user[1]}\t\t{user[0]}")
            print()
            print("Press 1.To add new entry")
            print("Press 2.To exit")
            ch=input("Enter your Choice: ")
            if ch=="1":
                continue
            elif ch=="2":
                break
            else:
                print("Invalid choice....try again")
                continue
        except:
            print("Fill the Details properly")
            continue
    print("---------------------------------------\n")
def add_books():
    print("\n---------------------------\n")
    while True:
        try:
            book_name=input("Enter book name: ")
            author=input("Enter Author Name: ")
            copies=int(input("Enter Copies Count: "))
            cursor.execute("insert into books(title,author,available_copies) values(%s,%s,%s)",(book_name,author,copies))
            conn.commit()
            print("Added Successfully")
            print("Here is a preview")
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()
            for book in books:
                print(f"Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Available Copies: {book[3]}")
        
            print("Press 1.To add new entry")
            print("Press 2.To exit")
            ch=input("Enter your Choice: ")
            if ch=="1":
                continue
            elif ch=="2":
                break
            else:
                print("Invalid choice....try again")
                continue
        except:
            print("fill details properly")
            continue
    print("---------------------------------\n")
# Display options for the main portal
print("---------------------------------------------------------------------------------------------\n")
print('''
 __       __  .______   .______          ___      .______     ____    ____ 
|  |     |  | |   _  \  |   _  \        /   \     |   _  \    \   \  /   / 
|  |     |  | |  |_)  | |  |_)  |      /  ^  \    |  |_)  |    \   \/   /  
|  |     |  | |   _  <  |      /      /  /_\  \   |      /      \_    _/   
|  `----.|  | |  |_)  | |  |\  \----./  _____  \  |  |\  \----.   |  |     
|_______||__| |______/  | _| `._____/__/     \__\ | _| `._____|   |__|     
                                                                            ''')
print("\n--------------------------------------------------------------------------------------------\n")

while True:
        
        print("1. Public Portal")
        print("2. Admin Portal")
        print("3. Exit")
        portal_choice = input("Enter your choice: ")

        # Navigate to different portals based on user choice
        if portal_choice == "1":
            print('------------------------------------\n')
            for i in range(1,4):
                print('Loading'+"."*i)
                time.sleep(0.5)           
            public_portal()
        elif portal_choice == "2":
            print('------------------------------------\n')   
            for i in range(1,4):
                print('Loading'+"."*i)
                time.sleep(0.5)                
            admin_portal()
        elif portal_choice == "3":
            break
        else:
            
            print("Invalid choice. Please try again.")
            print('------------------------------------\n')       


# Close the cursor and connection when done
cursor.close()
conn.close()

