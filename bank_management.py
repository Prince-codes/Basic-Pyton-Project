import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",

)
#Making Cursor
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS bank_management")
cursor.execute("USE bank_management")
# Create a table to store account information
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (account_no INT PRIMARY KEY AUTO_INCREMENT , name VARCHAR(255), dob DATE, pan_no VARCHAR(20), address VARCHAR(255), phone_no VARCHAR(15), nominee_name VARCHAR(255), balance DECIMAL(10, 2))")

# Function to open a new account
def open_account():
    print()
    name = input("Enter your name: ").upper()
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    pan_no = input("Enter your PAN number: ").upper()
    address = input("Enter your address: ").upper()
    phone_no = input("Enter your phone number: ")
    nominee_name = input("Enter nominee name: ").upper()
    print()
    
    cursor.execute("INSERT INTO accounts (name, dob, pan_no, address, phone_no, nominee_name, balance) VALUES ( %s, %s, %s, %s, %s, %s, 0)", (name, dob, pan_no, address, phone_no, nominee_name))
    db.commit()
    
    cursor.execute("SELECT * FROM accounts WHERE name=%s",(name,))
    user=cursor.fetchone()
    print()
    print(f"Account opened successfully Your account number {user[0]}")
    print()
    
# Function to deposit amount
def deposit():
    print()
    account_no = int(input("Enter your account number: "))
    print()
    amount = float(input("Enter the deposit amount: "))

    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_no = %s", (amount, account_no))
    db.commit()
    print("\nDeposit successful.\n")

# Function to withdraw amount
def withdraw():
    print()
    account_no = int(input("Enter your account number: "))
    amount = float(input("Enter the withdrawal amount: "))

    cursor.execute("SELECT balance FROM accounts WHERE account_no = %s", (account_no,))
    result = cursor.fetchone()

    if result:
        balance = result[0]
        if balance >= amount:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_no = %s", (amount, account_no))
            db.commit()
            print()
            print("\nWithdrawal successful.\n")
        else:
            print("\nInsufficient funds.\n")
    else:
        print("\nAccount not found.\n")

# Function for balance inquiry
def balance_enquiry():
    print()
    account_no = int(input("Enter your account number: "))
    cursor.execute("SELECT balance FROM accounts WHERE account_no = %s", (account_no,))
    result = cursor.fetchone()

    if result:
        balance = result[0]
        print(f"Your account balance is: ₹{balance}")
    else:
        print("\nAccount not found.\n")

# Function for listing all account holders
def all_account_holders():
    cursor.execute("SELECT * FROM accounts")
    results = cursor.fetchall()

    if results:
        print()
        print("All Account Holders : \n")
        for row in results:
            print(f"Account No: {row[0]} | Name: {row[1]} | Balance: ${row[7]}")
    else:
        print("\nNo accounts found.\n")

# Function for closing a bank account
def close_account():
    print()
    account_no = int(input("Enter the account number to close: "))
    
    cursor.execute("DELETE FROM accounts WHERE account_no = %s", (account_no,))
    db.commit()
    print("\nAccount closed successfully.\n")


# Function for modifying bank account details
def modify_account():
    try:
        print()
        account_no = int(input("Enter the account number to modify: "))
        print()

        select_query="SELECT * FROM accounts WHERE account_no= %s"
        cursor.execute(select_query,(account_no,))
        user=cursor.fetchone()

        if user is None:
            print("\nAccount not Found........\n")
            return
        
        print(f"Editing details for USER with Account Number {account_no} : ")
        print("\n**If you Don't want to Edit the part leave empty & Proceed with next !\n")

        temp=input(f"Enter new first name (currently: {user[1]}): ")
        if temp:
            name=temp
        else:
            name=user[1]
        
        temp= input(f"Enter new date of birth in this format (YYYY-MM-DD) (currently: {user[2]}): ")
        if temp:
            dob=temp
        else:
            dob=user[2]

        temp= input(f"Enter new PAN (currently: {user[3]}): ").upper()
        if temp:
            pan=temp
        else:
            pan=user[3]

        temp= input(f"Enter new address (currently: {user[4]}): ")
        if temp:
            address=temp
        else:
            address=user[4]
        
        temp=input(f"Enter new contact number (currently: {user[5]}): ")
        if temp:
            contact_no=temp
        else:
            contact_no=user[5]

        temp=input(f"Enter new nominee name (currently: {user[6]}): ")
        if temp:
            n_name=temp
        else:
            n_name=user[6]

        update_query = """UPDATE accounts SET 
                        name = %s,  
                        dob = %s,
                        pan_no = %s,
                        address = %s, 
                        phone_no = %s,
                        nominee_name = %s
                        WHERE account_no = %s """
                        
        cursor.execute(update_query, (name, dob,pan, address, contact_no,n_name, account_no))
        db.commit()
        print(f"User details for Aaccount Number {account_no} updated successfully.")
    except Exception as e:
        print(e)
        print("Invalid Inputs\nTry again\n")
        ch=input("Press Y to Re-Enter Details\nPress N to to quit\nChoose your option: ")
        if ch.lower()=="y":
           modify_account()
# user Portal

def user_login():
    while True:
        print("\n---------------------------------------------------")
        print("                      USER PANEL                  ")
        print("---------------------------------------------------\n")
        print("ENTER 1 : To Deposit")
        print("ENTER 2 : To Withdraw")
        print('ENTER 3 : To Balance Enquiry')
        print("ENTER 0 : TO EXIT\n")
        try:
            ch=int(input("Enter your choice:"))
            if ch==1:
                deposit()
            elif ch==2:
                withdraw()
            elif ch==3:
                balance_enquiry()
            elif ch==0:
                print("")
                break
            else:
                print("\nInvalid Choice.....\n")
        except:
            print("\nInvalid choice")
            print()
            continue

#Admin Portal            
def admin_login():
    while True:
        print("\n---------------------------------------------------")
        print("                      ADMIN PANEL                  ")
        print("---------------------------------------------------\n")
        try:
            print()
            print("ENTER 1 : OPEN NEW ACCOUNT")
            print("ENTER 2 : SEE ALL REGESTERED ACCOUNT")
            print("ENTER 3 : EDIT ACCOUNT DETAIL")
            print("ENTER 4 : CLOSE ACCOUNT")
            print("ENTER 0 : EXIT")
            print()

            ch=int(input("Enter Your choice : "))
            print()

            if ch==1:
                open_account()

            elif ch==2:
                all_account_holders()

            elif ch==3:
                modify_account()

            elif ch==4:
                close_account()

            elif ch==0:
                print("\nThank you for using...\n")
                break
            else:
                print("\nInvalid Choice.....\n")

        except Exception as e:
            print(e)
            print("\nInvalid choice")
            print()
            

#Main Program-----------------------------------------------------------
print("---------------------------------------------------")
print("                 BANK MANAGEMENT                   ")
print("---------------------------------------------------")
while True:
    print()
    print("ENTER 1 : Admin Login")
    print("ENTER 2 : User Login")
    print("ENTER 0 : TO EXIT\n")

    ch=int(input("Enter your Choice: "))
    print()

    if ch==1:
        admin_login()
    elif ch==2:
        user_login()
    elif ch==0:
        print()
        break
    else:
        print("\nInvalid choice")
        print()
# Close the database connection
db.close()