import sqlite3
import os
from flask import g, current_app

class Database:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_data BLOB NOT NULL
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def insert_file(self, file_name, file_data):
        query = "INSERT INTO files (file_name, file_data) VALUES (?, ?);"
        self.cursor.execute(query, (file_name, file_data))
        self.conn.commit()

    def get_all_files(self):
        query = "SELECT file_name, file_data FROM files;"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        self.cursor.close()
        self.conn.close()

# Function to get the database instance
def get_db():
    if 'db' not in g:
        g.db = Database()
    return g.db

# Function to close the database connection at the end of the request
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# Function to format file size
def format_file_size(size):
    # Your implementation for formatting file size goes here
    # For example, you can use a function to convert bytes to a human-readable format
    if size < 1024:
        return f"{size} B"
    elif 1024 <= size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    elif 1024 ** 2 <= size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"
    else:
        return f"{size / (1024 ** 3):.2f} GB"
