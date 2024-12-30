import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to MySQL database
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="BIS_698_Group2"
    )
except mysql.connector.Error as e:
    messagebox.showerror("Database Connection Error", f"Failed to connect to the database: {e}")
    exit()

# Function to create tables 'goals' and 'progress' if they don't exist
def create_tables_if_not_exist():
    try:
        cursor = db.cursor()

        # Create the 'goals' table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                `id` int NOT NULL AUTO_INCREMENT,
                `username` varchar(255) NOT NULL,
                `password` varchar(255) NOT NULL,
                `email` varchar(255),
                `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                UNIQUE KEY `username` (`username`)
            )
        """)

        # Create the 'goals' table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                goal_id INT AUTO_INCREMENT PRIMARY KEY,
                goal_name VARCHAR(255) NOT NULL,
                deadline DATE,
                completion_percentage INT
            )
        """)

        # Create the 'progress' table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                progress_id INT AUTO_INCREMENT PRIMARY KEY,
                goal_id INT,
                progress_date DATE,
                completion_percentage INT,
                FOREIGN KEY (goal_id) REFERENCES goals(goal_id)
            )
        """)

        cursor.close()
        db.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Connection Error", f"Failed to create tables: {e}")
        exit()

# Call the function to create tables
create_tables_if_not_exist()