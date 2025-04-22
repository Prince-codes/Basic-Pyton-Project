#importing modules
import mysql.connector as con
import time as titan

# Establishing MySQL connection
db = con.connect(
    host="localhost",
    user="root",
    password="1234",
)

cur= db.cursor()
c=0

#Creating database if not Exists
query="CREATE DATABASE IF NOT EXISTS school_management"
cur.execute(query)
cur.execute("USE school_management")

#creating student table
cur.execute("CREATE TABLE IF NOT EXISTS students (admission_no INT AUTO_INCREMENT PRIMARY KEY,first_name VARCHAR(255),last_name VARCHAR(255),class VARCHAR(50),dob DATE,address VARCHAR(255),contact_no VARCHAR(15))")
cur.execute("CREATE TABLE IF NOT EXISTS left_students (admission_no INT AUTO_INCREMENT PRIMARY KEY,first_name VARCHAR(255),last_name VARCHAR(255),class VARCHAR(50),dob DATE,address VARCHAR(255),contact_no VARCHAR(15))")


#Creating Table for Teacher
cur.execute("CREATE TABLE IF NOT EXISTS teachers ( teacher_id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(50),last_name VARCHAR(50),contact_number VARCHAR(15),qualification VARCHAR(100),subjects VARCHAR(100),designation VARCHAR(50))")
cur.execute("CREATE TABLE IF NOT EXISTS left_teachers ( teacher_id INT PRIMARY KEY, first_name VARCHAR(50),last_name VARCHAR(50),contact_number VARCHAR(15),qualification VARCHAR(100),subjects VARCHAR(100),designation VARCHAR(50))")

#----------------------------FUNCTION RELATED TO STUDENT PANEL--------------------------------


#Register Student
def register_student():
    print()
    print("---------------------------STUDENT REGISTERATION--------------------------------------\n")
    global c
    try:
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        class_name = input("Enter class: ")
        dob = input("Enter date of birth (YYYY-MM-DD): ")
        address = input("Enter address: ")
        contact_no = input("Enter contact number: ")
        print()

        insert_query = "INSERT INTO students (first_name, last_name, class, dob, address, contact_no) VALUES (%s, %s, %s, %s,%s,%s)"
        cur.execute(insert_query, (first_name, last_name, class_name, dob, address, contact_no))
        c=0
        db.commit()

        print("\nStudent registered successfully.\n")
    except:
        print("Invalid Inputs\nTry again\n")
        ch=input("Press Y to Re-Enter Details\nPress N to to quit\nChoose your option: ")
        if ch.lower()=="y":
            register_student()


#Edit Detail Of Existing student
def edit_student():
    print("------------------------------------EDITING STUDENT DATA-------------------------------------\n")
    global first_name, last_name, class_name, dob, address, contact_no
    first_name= last_name= class_name= dob= address= contact_no=""
    try:
        print()
        admission_no = int(input("Enter Admission Number of the student to edit: "))
        print()
        
        select_query = "SELECT * FROM students WHERE admission_no = %s"
        cur.execute(select_query, (admission_no,))
        student = cur.fetchone()

        if student is None:
            print("Student not found.")
            return

        print(f"Editing details for student with Admission Number {admission_no}:")
        print("**If You dont Want To Edit the part it leave Empty & Proceed with next !")
        
        temp=input(f"Enter new first name (currently: {student[1]}): ")
        if temp:
            first_name=temp
        else:
            first_name=student[1]
        temp= input(f"Enter new last name (currently: {student[2]}): ")
        if temp:
            last_name=temp
        else:
            last_name=student[2]
        temp= input(f"Enter new class (currently: {student[3]}): ")
        if temp:
            class_name =temp
        else:
            class_name=student[3]
        temp= input(f"Enter new date of birth in this format (YYYY-MM-DD) (currently: {student[4]}): ")
        if temp:
            dob=temp
        else:
            dob=student[4]
        temp= input(f"Enter new address (currently: {student[5]}): ")
        if temp:
            address=temp
        else:
            address=student[5]
        temp=input(f"Enter new contact number (currently: {student[6]}): ")
        if temp:
            contact_no=temp
        else:
            contact_no=student[6]

        update_query = """UPDATE students SET 
                        first_name = %s, 
                        last_name = %s, 
                        class = %s, 
                        dob = %s, 
                        address = %s, 
                        contact_no = %s 
                        WHERE admission_no = %s """
                        
        cur.execute(update_query, (first_name, last_name, class_name, dob, address, contact_no, admission_no))
        db.commit()
        print(f"Student details for Admission Number {admission_no} updated successfully.")
    except:
        print("Invalid Inputs\nTry again\n")
        ch=input("Press Y to Re-Enter Details\nPress N to to quit\nChoose your option: ")
        if ch.lower()=="y":
           edit_student()


#Delete Data of Existing Student
def delete_student():
    print()
    print("------------------------------DELETING STUDENT DATA---------------------------------\n")
    try:
        admission_no = int(input("Enter Admission Number of the student to delete: "))
        
        select_query = "SELECT * FROM students WHERE admission_no = %s"
        cur.execute(select_query, (admission_no,))
        student = cur.fetchone()

        if student is None:
            print("\nStudent not found.\n")
            return

        # Move the student to the 'Left' status and create a record in the 'left_students' table
        insert_left_query = """INSERT INTO left_students (
            admission_no, 
            first_name, 
            last_name, 
            class, dob, 
            address, 
            contact_no)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(insert_left_query, student[0:7])
        
        delete_query = "DELETE FROM students WHERE admission_no = %s"
        cur.execute(delete_query, (admission_no,))
        db.commit()
        print(f"Student with Admission Number {admission_no} has been deleted and moved to the 'Left' records.")
    except:
        print("Invalid Inputs\nTry again\n")
        ch=input("Press Y to Re-Enter Details\nPress N to to quit\nChoose your option: ")
        if ch.lower()=="y":
           delete_student()
    
#To Show all Students Data
def show_students():
    select_query = "SELECT * FROM students"
    cur.execute(select_query)
    students = cur.fetchall()

    print(f"{'Admission No':<15}{'First Name':<15}{'Last Name':<15}{'Class':<10}\t{'Date of Birth'}\t{'Address'}\t{'Contact No':<15}")
    for student in students:
        print(f"{student[0]:<15}{student[1]:<15}{student[2]:<15}{student[3]:<10}\t{student[4]}\t{student[5]}\t{student[6]}")

def left_studs():
    cur.execute("select * from left_students")
    print(f"{'Admission No':<15}{'First Name':<15}{'Last Name':<15}{'Class':<10}\t{'Date of Birth'}\t{'Address'}\t{'Contact No':<15}")
    students=cur.fetchall()
    for student in students:
        print(f"{student[0]:<15}{student[1]:<15}{student[2]:<15}{student[3]:<10}\t{student[4]}\t{student[5]}\t{student[6]}")

#-------------------------------------FUNCTION RELATED TO TEACHERS PANEL-------------------------------------

#Teacher Registration
def register_teacher():
    try:
        print()
        print("---------------------------TEACHER REGISTRATION-----------------------------\n")
        
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        contact_number = input("Enter contact number: ")
        qualification = input("Enter highest qualification: ")
        subjects = input("Enter subjects to teach (comma-separated): ")
        designation = input("Enter designation: ")
        insert_query = "INSERT INTO teachers (first_name, last_name, contact_number, qualification, subjects, designation) VALUES (%s,%s, %s, %s, %s, %s)"
        
        values = (first_name, last_name, contact_number, qualification, subjects, designation)

        cur.execute(insert_query, values)
        db.commit()
        
        print("\nTeacher registered successfully!\n")
    except:
        print("Invalid Inputs\nTry again\n")
        ch=input("Press Y to Re-Enter Details\nPress N to to quit\nChoose your option: ")
        if ch.lower()=="y":
           register_teacher()

#Edit Detail of Existing Teacher
def edit_teacher():
    print("-----------------EDITING DETAILS---------------------------")
    try:
        print()
        teacher_id = int(input("Enter the teacher ID you want to edit: "))
        print()
        
        select_query = "SELECT * FROM teachers WHERE teacher_id = %s"
        cur.execute(select_query, (teacher_id,))
        teacher = cur.fetchone()

        if teacher is None:
            print("Teacher not found.")
            return
        
        print(f"Editing details for teacher with Teacher ID {teacher_id}:")

        print("**If You dont Want To Edit the part it leave Empty & Proceed with next !")
        
        temp=input(f"Enter new first name (currently: {teacher[1]}): ")
        if temp:
            first_name=temp
        else:
            first_name=teacher[1]
        temp= input(f"Enter new last name (currently: {teacher[2]}): ")
        if temp:
            last_name=temp
        else:
            last_name=teacher[2]
        temp= int(input(f"Enter new contact_number (currently: {teacher[3]}): "))
        if temp:
            contact_number=temp
        else:
            contact_number=teacher[3]
        temp= input(f"Enter new Qualification (currently: {teacher[4]}): ")
        if temp:
            qualification=temp
        else:
            qualification=teacher[4]
        temp= input(f"Enter new Subject (currently: {teacher[5]}): ")
        if temp:
            subjects=temp
        else:
            subjects=teacher[5]
        temp=input(f"Enter new Designation (currently: {teacher[6]}): ")
        if temp:
            designation=temp
        else:
            designation=teacher[6]

        update_query = "UPDATE teachers SET first_name = %s, last_name = %s, contact_number = %s, qualification = %s, subjects = %s, designation = %s WHERE teacher_id = %s"
        values = (first_name, last_name, contact_number, qualification, subjects, designation, teacher_id)

        cur.execute(update_query, values)
        db.commit()
        print(f"Teacher with ID {teacher_id} has been updated.")
    except:
        print("Invalid Inputs\nTry again\n")
        ch=input("Press Y to Re-Enter Details\nPress N to to quit\nChoose your option: ")
        if ch.lower()=="y":
            edit_teacher()         

#Deleting existing data of Teacher
def delete_teacher():
    print("------------------------------DELETING DATA-------------------------------")
    try:    
        print()
        teacher_id = int(input("Enter Id of the Teacher to delete: "))
        
        select_query = "SELECT * FROM teachers WHERE teacher_id = %s"
        cur.execute(select_query, (teacher_id,))
        teacher = cur.fetchone()

        if teacher is None:
            print("\nTeacher not found.\n")
            return

        # Move the teacher to the 'Left' status and create a record in the 'left_teachers' table
        insert_left_query = """INSERT INTO left_teachers (
            teacher_id,
            first_name, 
            last_name, 
            contact_number, 
            qualification, 
            subjects, 
            designation)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(insert_left_query, teacher[0:7])
        
        delete_query = "DELETE FROM teachers WHERE teacher_id= %s"
        cur.execute(delete_query, (teacher_id,))
        db.commit()
        print(f"Teacher with teacher_id {teacher_id} has been deleted and moved to the 'Left' records.")

    except :
        print("Invalid Inputs\nTry again\n")
        ch=input("Press Y to Re-Enter Details\nPress N to to quit\nChoose your option: ")
        if ch.lower()=="y":
            delete_teacher()         
    
#To Show All Data Of Teachers
def show_teachers():

        select_query = "SELECT * FROM teachers"
        cur.execute(select_query)
        teachers = cur.fetchall()

        print(f"{'teacher_id':<15}{'First Name':<15}{'Last Name':<15}{'contact_number'}\t{'qualification'}\t\t{'subjects'}\t\t{'designation'}")
        for teacher in teachers:
            print(f"{teacher[0]:<15}{teacher[1]:<15}{teacher[2]:<15}{teacher[3]:<10}\t\t\t{teacher[4]}\t\t{teacher[5]}\t\t{teacher[6]}")
def left_teach():
    select_query = "SELECT * FROM left_teachers"
    cur.execute(select_query)
    teachers = cur.fetchall()

    print(f"{'teacher_id':<15}{'First Name':<15}{'Last Name':<15}{'contact_number'}\t{'qualification'}\t\t{'subjects'}\t\t{'designation'}")
    for teacher in teachers:
        print(f"{teacher[0]:<15}{teacher[1]:<15}{teacher[2]:<15}{teacher[3]:<10}\t\t\t{teacher[4]}\t\t{teacher[5]}\t\t{teacher[6]}")


# Main program loop
while True:
    print("-----------------------------------------------------------------------------------------------------------------------------")
    print(""" 
                                    ███████╗ ██████╗██╗  ██╗ ██████╗  ██████╗ ██╗     
                                    ██╔════╝██╔════╝██║  ██║██╔═══██╗██╔═══██╗██║     
                                    ███████╗██║     ███████║██║   ██║██║   ██║██║     
                                    ╚════██║██║     ██╔══██║██║   ██║██║   ██║██║     
                                    ███████║╚██████╗██║  ██║╚██████╔╝╚██████╔╝███████╗
                                    ╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝


                ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗███╗   ███╗███████╗███╗   ██╗████████╗
                ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝
                ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   
                ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   
                ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   
                ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝                                                     
          
          """)
    print("----------------------------------------------------------------------------------------------------------------------------")
    
    print("1. Student Panel")
    print("2. Teacher Panel")
    print("3. Exit")
    print()
    choice = int(input("Enter your choice: "))
    print()
    
    if choice == 1:
        for i in range(3):
            print("logging in"+"."*(i+1))
            titan.sleep(0.7)

        print("\n------------------------------------------------------------------------------------------------------------------\n")
        print('''
                    ███████╗████████╗██╗   ██╗██████╗ ███████╗███╗   ██╗████████╗    ██████╗  █████╗ ███╗   ██╗███████╗██╗     
                    ██╔════╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝████╗  ██║╚══██╔══╝    ██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     
                    ███████╗   ██║   ██║   ██║██║  ██║█████╗  ██╔██╗ ██║   ██║       ██████╔╝███████║██╔██╗ ██║█████╗  ██║     
                    ╚════██║   ██║   ██║   ██║██║  ██║██╔══╝  ██║╚██╗██║   ██║       ██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  ██║     
                    ███████║   ██║   ╚██████╔╝██████╔╝███████╗██║ ╚████║   ██║       ██║     ██║  ██║██║ ╚████║███████╗███████╗
                    ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝       ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
                                                                                                                               
              ''')
        print("----------------------------------------------------------------------------------------------------------------------")
        while True:
            
            print("Enter 1 : To Register Student ")
            print("Enter 2 : To Edit Details Of Existing student  ")
            print("Enter 3 : To Delete Data of Existing Student  ")
            print("Enter 4 : To Show all Students Data ")
            print("Enter 0:  To Return to Main Menu")
            print()
            try:
                ch=int(input("Enter your Choice : "))
      
                if ch==1:
                    register_student()
                    print("\n-------------------------------------------------------------------------\n")
                elif ch==2:
                    edit_student()
                    print("\n-------------------------------------------------------------------------\n")
                elif ch==3:
                    delete_student()
                    print("\n-------------------------------------------------------------------------\n")
                
                elif ch==4:
                    print("-----------------------------DISPLAYING STUDENTS DATA---------------------------------\n")
                    print("\nStudents Active :- \n")
                    show_students()
                    print()
                    print("\nStudents Left:-\n")
                    left_studs()
                    print("\n-------------------------------------------------------------------------\n")
                elif ch==0:
                    for i in range(3):
                        print("logging out"+"."*(i+1))
                        titan.sleep(0.7)
                    break
                else:
                    print("Invalid Choice")
            except Exception as e:
                print(e)
                print("\nWrong Input\nTry Again\n")
                continue


        
    elif choice==2:
        for i in range(3):
            print("logging in"+"."*(i+1))
            titan.sleep(0.7)

        print("\n-------------------------------------------------------------------------------------------\n")
        print("""

            ████████╗███████╗ █████╗  ██████╗██╗  ██╗███████╗██████╗     ██████╗  █████╗ ███╗   ██╗███████╗██╗     
            ╚══██╔══╝██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗    ██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     
               ██║   █████╗  ███████║██║     ███████║█████╗  ██████╔╝    ██████╔╝███████║██╔██╗ ██║█████╗  ██║     
               ██║   ██╔══╝  ██╔══██║██║     ██╔══██║██╔══╝  ██╔══██╗    ██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  ██║     
               ██║   ███████╗██║  ██║╚██████╗██║  ██║███████╗██║  ██║    ██║     ██║  ██║██║ ╚████║███████╗███████╗
               ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
                                                                                                                   
 """)
        print("-------------------------------------------------------------------------------------------------------")
        while True:
            print("Enter 1 : To Register new Teacher")
            print("Enter 2 : To Edit Detail of Existing Teacher")
            print("Enter 3 : To Deleting existing data of Teacher")
            print("Enter 4 : To Show All Data Of Teachers")
            print("Enter 0:  To Return to Main")
            print()
            #query
            try:
                ch=int(input("Enter your Choice : "))
                print()
                if ch==1:
                    register_teacher()
                    print("\n-------------------------------------------------------------------------\n")
                elif ch==2:
                    edit_teacher()
                    print("\n-------------------------------------------------------------------------\n")
                elif ch==3:
                    delete_teacher()
                    print("\n-------------------------------------------------------------------------\n")                
                elif ch==4:
                    print("-------------------------DISPLAYING STAFF DETAILS--------------------------------\n")
                    print("\nTeachers Active :- \n")
                    show_teachers()
                    print()
                    print("\nTeachers Left:-\n")
                    left_teach()
                    print("\n-------------------------------------------------------------------------\n")
                elif ch==0:
                    for i in range(3):
                        print("logging out"+"."*(i+1))
                        titan.sleep(0.7)
                    print('------------------------------------------')
                    break
            except:
                print("\nWrong Input\nTry Again\n")
                continue

    elif choice==3:
        print("Thanks For Using this Program")
        print("See you soon...")
        break
    
    else:
        print("Invalid Choice")
        
# Close MySQL connection
db.close()
#-------------------------------------------------DONE--------------------------------------------------