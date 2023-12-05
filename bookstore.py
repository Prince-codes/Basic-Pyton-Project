import mysql.connector as con
import random as r

# Function to establish a connection to the MySQL database

connection = con.connect(host='localhost',user='root',passwd='1234')
cursor=connection.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS book;')
cursor.execute('USE book;')


cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255)
        );
    """)

connection.commit()
# Function to add a new record to the database
def add_record(connection, title, author):
    print()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (  title, author) VALUES (%s, %s)", ( title, author))
    connection.commit()
    print("Record added successfully.")
    print()

# Function to display all records in the database
def display_records(connection):
    print()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    records = cursor.fetchall()
    print("-----------------BOOKS---------------")
    for record in records:
        print(f"Book_ID: {record[0]} | Title: {record[1]} | Author: {record[2]}  |")
        print()
    print()


# Function to modify a record in the database
def modify_record():
    print()
    try:
        book_id = int(input("Enter Book_ID to modify: "))
        new_title = input("Enter new Title: ")
        new_author = input("Enter new Author: ")
        cursor = connection.cursor()
        # Validate if the book_id exists before updating
        cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
        existing_book = cursor.fetchone()
        if existing_book:
            cursor.execute("UPDATE books SET title = %s, author = %s WHERE book_id = %s", (new_title, new_author, book_id))
            print("Record modified successfully.")
            connection.commit()
        else:
            print("Book with ID {} not found.".format(book_id))
    except ValueError:
        print("Invalid input. Please enter a valid Book ID.")
    except Exception as e:
        print("An error occurred:", e)
        print()

    
# Function to delete a record from the database
def delete_record(connection, book_id):
    print()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
    connection.commit()
    print("Record deleted successfully.")
    print()


# Function to search for a record by roll number
def search_record(connection, book_id):
    print()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
    record = cursor.fetchone()
    if record:
        print(f"Book_ID: {record[0]} | Title: {record[1]} | Author: {record[2]}  |")
    else:
        print("Record not found.")
    print()


# Main function to execute the program
while True:
        print()
        print("       \t  WELCOME TO BOOK STORE \t   ")
        print("\n1. Add new record.")
        print("2. Display records")
        print("3. Modify record.")
        print("4. Delete record.")
        print("5. Search record by Book ID.")
        print("6. Exit")
        try:
            choice = input("\n Enter your choice: ")
            
            if choice == '1':
                title = input("Enter Title: ")
                author = input("Enter Author: ")

                add_record(connection,  title, author)

            elif choice == '2':
                display_records(connection)

            elif choice == '3':
                modify_record()

            elif choice == '4':
                
                book_id = int(input("Enter Book_ID to delete: "))
                delete_record(connection, book_id)

            elif choice == '5':
                book_id = int(input("Enter Book_ID to search: "))
                search_record(connection, book_id)

            elif choice == '6':
                break

            else:
                print("Invalid choice. Please enter a valid option.")
        except:
            print("Invalid Choice \nTry Again....\n")
            continue

connection.close()



