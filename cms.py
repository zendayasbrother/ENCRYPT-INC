import os
import pandas as pd 
import sqlite3 
from auth import AuthSystem
from database import DataManager
from dotenv import load_dotenv

# RBA Login system using the admin's and creator passwords
class ManagementSystem(AuthSystem, DataManager):
    def __init__(self, db_path):
        # Initialize both parent classes
        AuthSystem.__init__(self, db_path)
        DataManager.__init__(self, db_path)
    
    def run_app(self):
        print("--- Encrypt Inc. OS ---")
        user = input("Username: ")
        pw = input("Password: ")
        
        if self.authenticate_user(user, pw):
            print("\nLogin Successful!")
            self.display_table_interface()
        else:
            print("\nAccess Denied.")

    def display_table_interface(self):
        name = input("Enter the table name to display: ")
        self.display_table(name) 

if __name__ == "__main__":
    load_dotenv() 
    db_path = os.getenv('DB_PATH') 
    
    if db_path and os.path.exists(db_path):
        app = ManagementSystem(db_path)
        app.run_app()
    else:
        print(f"Error: Database path '{db_path}' is invalid or missing.")
        
    # Admins: Create and manage users, Read Tables and Figures, Update and Delete records (binary fail / success)
    # Creators and Freelancers: Read Respective Tables and Figures, Update personal metrics, Propose new projects and ideas for approval 
    # possibly main.py (?) to run the app and separate files for different user roles?