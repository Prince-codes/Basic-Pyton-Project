#importing module
import mysql.connector as con

# Making connection to MYSql
db = con.connect(
    host="localhost",
    user="root",
    password="1234",
    
)

#Making cursor for database
cursor = db.cursor()
# Creating Database If Not Exists
cursor.execute("create database if not exists employee_management")
cursor.execute("use employee_management")

# Creating table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        phone_number VARCHAR(15),
        date_of_birth DATE,
        address VARCHAR(255),
        post VARCHAR(50),
        salary INT
    )
""")

# Function to add an employee
def add_employee():
    print()
    name=input("Enter Employee Name: ")
    phone_number=int(input("Enter Phone Number: "))
    date_of_birth=input("Enter Date of Birth (YYYY-MM-DD) : ")
    address=input("Enter Address : ")
    post=input("Enter employee Post : ")
    salary=int(input("Enter employee Salary: "))
    print()
    # Inserting values into the table
    sql = "INSERT INTO employees (name, phone_number, date_of_birth, address, post, salary) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (name, phone_number, date_of_birth, address, post, salary)
    cursor.execute(sql, values)
    db.commit()
    print("employee added successfully")
    print()
    

# Function to check an employee
def check_employee():
    print()
    employee_id=int(input("Enter employee ID: "))
    cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
    result = cursor.fetchone()
    if result:
        print("\nEMPLOYEE FOUND....\n")
        print("EMP_id \t Name\t Phone_no\t Date of Birth\t Address\t Post\t Salary")
        print(result[0],result[1],result[2],result[3],result[4],result[5],result[6],sep='\t')
        print()  
    else:
        print("\nEmployee not found\n")

# Function to display all employees
def display_employees():
    
    print()
    cursor.execute("SELECT * FROM employees")
    results = cursor.fetchall()
    try:
        if results:
            print("E_id \t Name\t Phone_no\t Date of Birth\t Address\t Post\t Salary")
            for result in results:
                print(result[0],result[1],result[2],result[3],result[4],result[5],result[6],sep='\t')
                    
            print()
            
        else:
            print("No employees found !")
    except Exception as e:
        print(e)
        
# Function to update an employee
def update_employee():
    try :
        print()
        employee_id = int(input("Enter employee ID: "))
        
        # Check if the employee_id exists in the database
        cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
        
        employee = cursor.fetchone()  # Fetches one row if the ID exists
        
        if employee is None:
            print("employee not found")
            return
        print(f"Editing details for employee with employee id {employee_id}:")

        print("\n**If You dont Want To Edit the part leave it Empty & Proceed with next !\n")

        temp=input(f"Enter new Name (currently: {employee[1]}): ")
        if temp:
            first_name=temp
        else:
            first_name=employee[1]
            
        temp= input(f"Enter new Phone Number (currently: {employee[2]}): ")
        if temp:
            phone_no =temp
        else:
            phone_no=employee[2]
            
        temp= input(f"Enter new date of birth in this format (YYYY-MM-DD) (currently: {employee[3]}): ")
        if temp:
            dob=temp
        else:
            dob=employee[3]

        temp= input(f"Enter new address (currently: {employee[4]}): ")
        if temp:
            address=temp
        else:
            address=employee[4]
            
        temp=input(f"Enter new Post (currently: {employee[5]}): ")
        if temp:
            po=temp
        else:
            po=employee[5]
        
        temp=int(input(f"Enter new Salary (currently: {employee[6]}): "))
        if temp:
            salary=temp
        else:
            salary=employee[6]
                
        update_query = """UPDATE employees SET 
                            name = %s,  
                            phone_number = %s, 
                            date_of_birth = %s, 
                            address = %s, 
                            post = %s,
                            salary = %s 
                            WHERE employee_id = %s """
                            
        cursor.execute(update_query, (first_name, phone_no, dob, address,po, salary, employee_id))
        db.commit()
        print()
        print(f"employee details for Employee Id {employee_id} updated successfully.")
        print()
    
    except Exception as e:
         print(e)
         print()
         print("Invalid Inputs\nTry again\n")
         ch=input("Press Y to Re-Enter Details\nPress N to to quit\nChoose your option: ")
         if ch.lower()=="y":
           update_employee()


# Function to remove an employee
def remove_employee():
    employee_id=int(input("Enter Employee ID: "))
    print()
    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    db.commit()
    print("\nEmployee removed successfully\n")


# Function to search for an employee
print("\n--------------------------------------------------------------------------")
print('''
                                EMPLOYEE MANAGEMENT
''')
print("----------------------------------------------------------------------------\n")
while True:
        print()
        print("ENTER 1 : ADD employee")
        print("ENTER 2 : VIEW EPLOYEE")
        print("ENTER 3 : FIND EMPLOYEE")
        print("ENTER 4 : MODIFY EMPLOYEE DETAIL")
        print("ENTER 6 : REMOVE EMPLOYEE")
        print("ENTER 0 : TO EXIT")
        print()
        
        
        try:
            ch=int(input("Enter Your choice: "))
            if ch==1:
                add_employee()
            elif ch==2:
                display_employees()
            
            elif ch==3:
                check_employee()
                
            elif ch==4:
                update_employee()
                            
            elif ch==6:
                remove_employee()
            
            elif ch==0:
                print()
                print("THANK YOU FOR USING............\n")
                break
            else:
                print("\nInvalid Choice..........")
                print("Try Again.....")
                print()
        except:
            print("Invalid Choice.....")
            print("Try again..........")
            print()


# Close the database connection
db.close()