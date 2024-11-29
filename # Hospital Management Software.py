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
    cursor.execute("CREATE DATABASE IF NOT EXISTS SP_hospitals")
    cursor.execute("USE SP_hospitals")
    
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
    username = input("Enter your preferred username: ")
    password = input("Enter your preferred password: ")

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


def administration_menu():
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
            print("Showing Details... (To Be Implemented)")
        elif choice == 2:
            print("Adding New Member... (To Be Implemented)")
        elif choice == 3:
            print("Deleting Member... (To Be Implemented)")
        elif choice == 4:
            break
        else:
            print("Invalid Choice. Try Again.")


def patient_menu():
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
            print("Showing Patient Details... (To Be Implemented)")
        elif choice == 2:
            print("Adding New Patient... (To Be Implemented)")
        elif choice == 3:
            print("Discharging Patient... (To Be Implemented)")
        elif choice == 4:
            break
        else:
            print("Invalid Choice. Try Again.")


def main():
    """Main function for the hospital management system."""
    print("""
====================================================
WELCOME TO SP HOSPITALS PVT. LTD.
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
                        administration_menu()
                    elif option == 2:
                        patient_menu()
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
