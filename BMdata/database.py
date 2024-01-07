import mysql.connector
from mysql.connector import Error
from user_manager import UserManager
import random

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='budgetmaster',
            user='root',
            password='Dusan2002!'
        )
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except Error as e:
        print(f'Error connecting to MySQL database: {e}')

    return connection

def create_expenses_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user VARCHAR(255) NOT NULL,
        date DATE NOT NULL,
        category VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        amount FLOAT NOT NULL
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print('Expenses table created')
    except Error as e:
        print(f'Error creating expenses table: {e}')

def insert_expense(connection,user,date,category,description,amount):
    query = """
    INSERT INTO expenses (user, date, category, description, amount)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, (user,date,category,description,amount,))
        connection.commit()
        print('Expense inserted successfully')
    except Error as e:
        print(f'Error inserting expense: {e}')

def get_expenses_of_user(connection, user):
    query = "SELECT category, amount FROM expenses WHERE user = %s"
    try:
        cursor = connection.cursor()
        cursor.execute(query, (user,))
        expenses = cursor.fetchall()
        expenses_list = []
        for expense in expenses:
            expense_dict = {'category': expense[0], 'amount': expense[1]}
            expenses_list.append(expense_dict)
        return expenses_list
    except mysql.connector.Error as e:
        print(f'Error retrieving expenses: {e}')
        return []  # Return an empty list in case of an error

def get_income(connection,username):
    query = "SELECT income FROM users WHERE username = %s"
    try:
        cursor = connection.cursor()
        cursor.execute(query,(username,))
        income = cursor.fetchone()
        return income[0]
        
    except Error as e:
        print(f'Error retrieving income: {e}')

def update_income(connection, income):
    user = UserManager.get_current_user()
    if user:
        username = user.username
        sql = "UPDATE users SET income = %s WHERE username = %s"
        try:
            cursor = connection.cursor()
            cursor.execute(sql, (income, username))
            connection.commit()
            print('Income updated successfully')
        except mysql.connector.Error as e:
            print(f'Error updating income: {e}')
        finally:
            cursor.close()
    else:
        print("No user is currently logged in.")

def get_tip(connection):
    cursor = connection.cursor()

    # Query for all tips in the database
    cursor.execute('SELECT tip FROM tips_table')
    tips = cursor.fetchall()

    # Check if there are any tips in the database
    if not tips:
        return "No tips available."

    # Select a random tip from the list of tips
    random_tip = random.choice(tips)

    return random_tip[0]

def create_users_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        income FLOAT NOT NULL,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print('Users table created')
    except Error as e:
        print(f'Error creating users table: {e}')
    finally:
        cursor.close()

def insert_user(connection,name,income, username,email, password):
    query = """
    INSERT INTO users (name,income,username,email, password)
    VALUES (%s,%s,%s,%s, %s)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, (name,income,username, email,password))
        connection.commit()
        print('User inserted successfully')
    except Error as e:
        print(f'Error inserting user: {e}')
        


def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print('Connection to MySQL database closed')
