# database.py
# This file connects Python to MySQL and contains database operations.

import mysql.connector
from mysql.connector import Error


# Change these values according to your MySQL setup.
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "admin123",
    "use_pure": True
}


def get_connection():
    """Create the database if needed, then connect to it."""
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS employee_management")
    cursor.execute("USE employee_management")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INT AUTO_INCREMENT PRIMARY KEY,
            employee_name VARCHAR(100) NOT NULL,
            salary DECIMAL(10, 2) NOT NULL,
            department VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            gender VARCHAR(20) NOT NULL
        )
    """)

    cursor.close()
    return connection


def get_all_employees():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees ORDER BY employee_id")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def insert_employee(name, salary, department, age, gender):
    connection = get_connection()
    cursor = connection.cursor()
    sql = """
        INSERT INTO employees
        (employee_name, salary, department, age, gender)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (name, salary, department, age, gender))
    connection.commit()
    cursor.close()
    connection.close()


def update_employee(employee_id, name, salary, department, age, gender):
    connection = get_connection()
    cursor = connection.cursor()
    sql = """
        UPDATE employees
        SET employee_name = %s, salary = %s, department = %s,
            age = %s, gender = %s
        WHERE employee_id = %s
    """
    cursor.execute(sql, (name, salary, department, age, gender, employee_id))
    connection.commit()
    changed = cursor.rowcount
    cursor.close()
    connection.close()
    return changed


def delete_employee(employee_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    connection.commit()
    deleted = cursor.rowcount
    cursor.close()
    connection.close()
    return deleted

# py -m pip install mysql-connector-python
# py -m pip show mysql-connector-python
