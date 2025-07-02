# seed.py
import mysql.connector
import uuid
import csv
import os
from mysql.connector import Error

def connect_db():
    return mysql.connector.connect(host="localhost", user="root", password="")

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()

def connect_to_prodev():
    return mysql.connector.connect(host="localhost", user="root", password="", database="ALX_prodev")

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
    ''')
    connection.commit()
    print("Table user_data created successfully")

def insert_data(connection, file_path):
    cursor = connection.cursor()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("SELECT COUNT(*) FROM user_data WHERE user_id=%s", (row['user_id'],))
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (row['user_id'], row['name'], row['email'], row['age'])
                )
    connection.commit()
