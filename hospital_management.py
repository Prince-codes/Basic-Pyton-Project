import mysql.connector as con

# Connect to the database
db = con.connect(
    host="localhost",
    user="root",
    password="1234"
)
cursor = db.cursor()
cursor.execute("create database if not exists hospital_management;")
cursor.execute("use hospital_management;")
cursor.execute("create table if not exists patients(patient_id int auto_increment primary key,name varchar(32),age int(2),gender varchar(10),reason varchar(50));")
cursor.execute("create table if not exists bills(name varchar(32),patient_id int(5),amount int(12));") 

# Add new patient
def add_patient():
 while True:
  try:
    print("--------------------ADMITTING PATIENTS------------------------------")
    print()
    name = input("Enter patient name: ")
    age = int(input("Enter patient age: "))
    gender = input("Enter patient gender: ")
    reason = input("Enter patient diagnosis: ")
    cursor.execute("INSERT INTO patients (name,age,gender,reason) VALUES (%s, %s, %s, %s)", (name, age, gender,reason))
    cursor.execute("SELECT * FROM patients WHERE name = %s", (name,))
    a=cursor.fetchone()
    print()
    print("Patient added successfully")
    print(f" ID - {a[0]}            NAME-{a[1]} ")
    print()
    db.commit()
    r=input("Press Y to Add Another Entry\nPress Any key to Exit\nEnter your Choice: ")
    if r.upper()=='Y':
            continue
    else:
            print("-----------------------------------------------------------------")
            break
  except:
       
        print("\n An Error occured Try again")
        r=input("Y.To Add Another Entry \nAny. To Exit \nEnter your choice: ")
        if r.upper()=='Y':
            continue
        else:
            print("-----------------------------------------------------------------")
            break
# Update patient status
def update_patient_status():
    while True:
        try:
            print("-----------------MODIFYING PATIENT STATUS----------------------------\n")
            patient_id = int(input("Enter patient ID: "))
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            patient=cursor.fetchone()
            if patient:
                reason  = input("Enter new diagnosis: ")
                print()
                cursor.execute("UPDATE patients SET reason=%s WHERE patient_id=%s", (reason, patient_id))
                print(f"Patient status has been successfully updated for patient ID: {patient_id}.")
                print()
                db.commit()

            else:
                print()
                print(" Patient Not Found, Retry ...")
                print("-------------------------------------------------")
                print()
            r=input("Y.To Add Another Entry \nAny. To Exit \nEnter your choice: ")
            if r.upper()=='Y':
                continue
            else:
                print("-----------------------------------------------------------------")
                break            

        except Exception as e :

            print(f"Error Occured.....")
            print()
            
            r=input("Y.To Retry \nAny. To Exit \nEnter your choice: ")
            if r.upper()=='Y':
                continue
            else:
                print("-----------------------------------------------------------------")
                break
# Discharge patient
def discharge_patient():
    while True:
        try:
            print()
            print("---------------------------DISCHARGING PATIENT-------------------------------") 
            print()
            patient_id = int(input("Enter patient ID: "))
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            patient=cursor.fetchone()
            if patient:
                cursor.execute("DELETE FROM patients WHERE patient_id=%s", (patient_id,))
                print(f"\nPatient {patient[1]} discharged successfully")
                
                db.commit()

            else:
                print("Patient Not Found... Try again!")
            print()
            r=input("Y.To Add Another Entry \nAny. To Exit \nEnter your choice: ")
            if r.upper()=='Y':
                    continue
            else:
                    print("-----------------------------------")
                    print()
                    break            
        except Exception as e:
            print("Error Occured Try again")

            r=input("Y.To Retry \nAny. To Exit \nEnter your choice: ")
            if r.upper()=='Y':
                continue
            else:
                print("-----------------------------------------------------------------")
                break
def show_patients():
            print('''
            ---------------------------DISPLAYING PATIENTS----------------------------------------
            ''')
            cursor.execute("SELECT * FROM patients")
            patients=cursor.fetchall()
            if not patients:
                print("No Records Found.....")
            else:
                print("ID\tNAME\tAGE\tGENDER\tREASON")
                print("-----------------------------------------------------")        
                for patient in patients:
                    print(f"{patient[0]} \t{patient[1]} \t{patient[2]} \t{patient[3]} \t{patient[4]}")
                    print("-----------------------------------------------")

# Process bill
def bill_processing():
    while True:
        try:
            print()
            patient_id = int(input("Enter patient ID: "))
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            patient=cursor.fetchone()
            name=patient[1]
            amount = float(input("Enter bill amount: "))
            cursor.execute("INSERT INTO bills (name,patient_id, amount) VALUES (%s,%s, %s)", (name,patient_id, amount))
            print(f"\nBill Processed for {name}.")
            print("")
            db.commit()
            r=input("Y.To Add Another Entry \nAny. To Exit \nEnter your choice: ")
            if r.upper()=='Y':
                    continue
            else:
                print("\n Exitting...")
                break
        except Exception as e:
            print("......Error Occured Try again......")

            r=input("Y.To Retry \nAny. To Exit \nEnter your choice: ")
            if r.upper()=='Y':
                continue
            else:
                print("-----------------------------------------------------------------")
                break

           

def admin_login():
    while True:
     try:
        print('''
------------------------------------------------------------------------------------------------
                                            ADMIN LOGIN                                        
------------------------------------------------------------------------------------------------
        ''')
        print("1. Admit new patient")
        print("2. Edit patient details")
        print("3. Manage billing")
        print("4. Release patient")
        print("5. List Patients")
        print("6. Exit Session")
        choice = input("Enter choice: ")
        if choice == '1':
            add_patient()
        elif choice == '2':
            update_patient_status()
        elif choice == '4':
            discharge_patient()
        elif choice == '3':
            bill_processing()
        elif choice == '5':
            show_patients()
        elif choice=='6':
            break
        else:
            print("\n \tInvalid choice")
            continue
     except:
            print("......Try again......")
            continue
          

# View patient status
def view_patient_status():
    while True:
        try:
            print()
            print("-----------------------PATIENT STATUS--------------------------------")
            print()
            patient_id = int(input("Enter patient ID: "))
            cursor.execute(f"SELECT * FROM patients WHERE patient_id = {patient_id}")
            patient_data=cursor.fetchone()
            print()
            if patient_data:
                print(f"Patient ID | {patient_data[0]} |")
                print(f"Name | {patient_data[1]} |")
                print(f"Age | {patient_data[2]} |")
                print(f"Gender | {patient_data[3]} |")
                print(f"Admit Reason | {patient_data[4]} |")  
                print()           
            else:
                print()
                print(f"No Patient Found.......")
                print()
            r=input("Y.To Add Another Entry \nAny. To Exit \nEnter your choice: ")
            if r.upper()=='Y':
                    continue
            else:
                print()
                break
        except:
            print("Try again.......")

            r=input("Y.To Retry \nAny. To Exit \nEnter your choice: ")
            if r.upper()=='Y':
                continue
            else:
                print("-----------------------------------------------------------------")
                break
        
        
# View bill amount
def view_bill_amount():
    while True:
        try:
            print("-----------------------------BILL AMOUNT--------------------------------")
            patient_id = int(input("Enter patient ID: "))
            cursor.execute("SELECT * FROM bills WHERE patient_id=%s", (patient_id,))
            amount = cursor.fetchone()
            if amount:
                print(f'''
                =====================================================
                                 HOSPITAL BILL                     
                =====================================================
                            Patient Information                              
                        Name: {amount[0]}                               
                        ID:   {amount[1]}                               
                                                                   
                                                                   
                       Amount to be Paid :  ₹{amount[2]}               
                =====================================================

                

''')
                print()
            else:
                print("Bill not found")
                print()
            r=input("Y.To Search Another Entry \nAny. To Exit \nEnter your choice: ")
            if r.upper()=='Y':
                    continue
            else:
                print()
                break   
        except Exception as e:
            print(" Try Again....")
            print()
            r=input("Y.To Retry \nAny. To Exit \nEnter your choice: ")
            if r.upper()=='Y':
                continue
            else:
                print("-----------------------------------------------------------------")
                break

    


def user_login():
 while True: 
  try:
    print("""
-------------------------------------------------------------------------
                               USER  LOGIN
-------------------------------------------------------------------------
    """)
    print("1. Chech Patient Condition")
    print("2. Display billing Amount")
    print("3. Exit")
    choice = input("\n Enter choice: ")
    if choice == '1':
        view_patient_status()
    elif choice == '2':
        view_bill_amount()
    elif choice == '3':
        print("----------------------------------------------------")
        print()
        break
    else:
       print("\n Invalid choice")
       continue
  except :
      print("Try Again......")
      continue
  

#MAIN PROGRAM
def main_menu():
    while True:
        try:
            print('''
-----------------------------------------------------------------------------------------
                                HOSPITAL MANAGEMENT
-----------------------------------------------------------------------------------------
            ''')
            print("1. Admin login")
            print("2. User login")
            print("3. Exit")
            choice = input("Enter choice: ")
            if choice == '1':
             admin_login()
            elif choice == '2':
                user_login()
            elif choice == '3':
                break
            else:
                print("Invalid choice")
        except:
            print("......Try Again......")

# Initialize the application
main_menu()
# Close the database 
db.close()