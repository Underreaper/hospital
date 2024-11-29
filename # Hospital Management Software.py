# Hospital Management Software

import mysql.connector

def connect_to_database(password):
    """Connects to MySQL and returns the connection and cursor."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=password
        )
        cursor = connection.cursor()
        return connection, cursor
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None, None


def create_tables(cursor):
    """Creates necessary tables for the hospital management system."""
    cursor.execute("CREATE DATABASE IF NOT EXISTS hospitals")
    cursor.execute("USE hospitals")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_details (
            name VARCHAR(30) PRIMARY KEY,
            age INT,
            address VARCHAR(50),
            doctor_recommended VARCHAR(30)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctor_details (
            name VARCHAR(30) PRIMARY KEY,
            specialization VARCHAR(40),
            age INT,
            address VARCHAR(50),
            contact VARCHAR(15),
            fees INT,
            monthly_salary INT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nurse_details (
            name VARCHAR(30) PRIMARY KEY,
            age INT,
            address VARCHAR(50),
            contact VARCHAR(15),
            monthly_salary INT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS other_workers_details (
            name VARCHAR(30) PRIMARY KEY,
            age INT,
            address VARCHAR(50),
            contact VARCHAR(15),
            monthly_salary INT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            username VARCHAR(30) PRIMARY KEY,
            password VARCHAR(30)
        )
    """)


def register_user(cursor, connection):
    """Handles user registration."""
    print("REGISTER YOURSELF")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        cursor.execute("INSERT INTO user_data VALUES (%s, %s)", (username, password))
        connection.commit()
        print("Registered Successfully!")
    except mysql.connector.Error as err:
        print(f"Error during registration: {err}")


def login_user(cursor):
    """Handles user login."""
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT password FROM user_data WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result and result[0] == password:
        print("Login Successful!")
        return True
    else:
        print("Invalid Username or Password.")
        return False


def administration_menu(cursor, connection):
    """Displays and handles administration tasks."""
    while True:
        print("""
1. SHOW DETAILS
2. ADD NEW MEMBER
3. DELETE EXISTING MEMBER
4. EXIT TO MAIN MENU
        """)
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            print("""
1. DOCTOR DETAILS
2. NURSE DETAILS
3. OTHER WORKER DETAILS
            """)
            sub_choice = int(input("Enter your choice: "))
            if sub_choice == 1:
                cursor.execute("SELECT * FROM doctor_details")
                for row in cursor.fetchall():
                    print(row)
            elif sub_choice == 2:
                cursor.execute("SELECT * FROM nurse_details")
                for row in cursor.fetchall():
                    print(row)
            elif sub_choice == 3:
                cursor.execute("SELECT * FROM other_workers_details")
                for row in cursor.fetchall():
                    print(row)
            else:
                print("Invalid choice.")
        
        elif choice == 2:
            print("""
1. ADD DOCTOR
2. ADD NURSE
3. ADD OTHER WORKER
            """)
            sub_choice = int(input("Enter your choice: "))
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            address = input("Enter address: ")
            contact = input("Enter contact: ")
            monthly_salary = int(input("Enter monthly salary: "))
            
            if sub_choice == 1:
                specialization = input("Enter specialization: ")
                fees = int(input("Enter fees: "))
                cursor.execute("""
                    INSERT INTO doctor_details VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (name, specialization, age, address, contact, fees, monthly_salary))
            elif sub_choice == 2:
                cursor.execute("""
                    INSERT INTO nurse_details VALUES (%s, %s, %s, %s, %s)
                """, (name, age, address, contact, monthly_salary))
            elif sub_choice == 3:
                cursor.execute("""
                    INSERT INTO other_workers_details VALUES (%s, %s, %s, %s, %s)
                """, (name, age, address, contact, monthly_salary))
            else:
                print("Invalid choice.")
                continue

            connection.commit()
            print("Member added successfully!")
        
        elif choice == 3:
            print("""
1. DELETE DOCTOR
2. DELETE NURSE
3. DELETE OTHER WORKER
            """)
            sub_choice = int(input("Enter your choice: "))
            name = input("Enter the name of the member to delete: ")
            
            if sub_choice == 1:
                cursor.execute("DELETE FROM doctor_details WHERE name = %s", (name,))
            elif sub_choice == 2:
                cursor.execute("DELETE FROM nurse_details WHERE name = %s", (name,))
            elif sub_choice == 3:
                cursor.execute("DELETE FROM other_workers_details WHERE name = %s", (name,))
            else:
                print("Invalid choice.")
                continue

            connection.commit()
            print("Member deleted successfully!")
        
        elif choice == 4:
            break
        else:
            print("Invalid Choice. Try Again.")


def patient_menu(cursor, connection):
    """Displays and handles patient-related tasks."""
    while True:
        print("""
1. SHOW PATIENT DETAILS
2. ADD NEW PATIENT
3. DISCHARGE PATIENT
4. EXIT TO MAIN MENU
        """)
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            cursor.execute("SELECT * FROM patient_details")
            for row in cursor.fetchall():
                print(row)
        
        elif choice == 2:
            name = input("Enter patient name: ")
            age = int(input("Enter patient age: "))
            address = input("Enter patient address: ")
            doctor_recommended = input("Enter doctor recommended: ")

            cursor.execute("""
                INSERT INTO patient_details VALUES (%s, %s, %s, %s)
            """, (name, age, address, doctor_recommended))
            connection.commit()
            print("Patient added successfully!")
        
        elif choice == 3:
            name = input("Enter patient name to discharge: ")
            cursor.execute("DELETE FROM patient_details WHERE name = %s", (name,))
            connection.commit()
            print("Patient discharged successfully!")
        
        elif choice == 4:
            break
        else:
            print("Invalid Choice. Try Again.")

def main():
    """Main function for the hospital management system."""
    print("""
====================================================
WELCOME TO SURAJ HOSPITALS PVT. LTD.
====================================================
    """)
    password = input("Enter the database password: ")

    connection, cursor = connect_to_database(password)
    if not connection:
        return

    create_tables(cursor)

    while True:
        print("""
1. SIGN IN (LOGIN)
2. SIGN UP (REGISTER)
3. EXIT
        """)
        choice = int(input("Enter your choice: "))

        if choice == 2:
            register_user(cursor, connection)
        elif choice == 1:
            if login_user(cursor):
                while True:
                    print("""
1. ADMINISTRATION
2. PATIENT MANAGEMENT
3. LOGOUT
                    """)
                    option = int(input("Enter your choice: "))

                    if option == 1:
                        administration_menu(cursor, connection)
                    elif option == 2:
                        patient_menu(cursor, connection)
                    elif option == 3:
                        print("Logged Out Successfully.")
                        break
                    else:
                        print("Invalid Option. Try Again.")
        elif choice == 3:
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid Choice. Try Again.")

    connection.close()


if __name__ == "__main__":
    main()
