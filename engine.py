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
        
    def proposals(self):
        conn, cursor = self.connect_database()
        if cursor:
            try:
                cursor.execute("SELECT * FROM proposals")
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching proposals: {e}")
            finally:
                conn.close()
        return [] # first, admin window, then talent inputs and requests
    
    def run_app(self):
        print("--- Encrypt Inc. OS ---")
        user = input("Username: ")
        pw = input("Password: ")
        
        
        if self.authenticate_user(user, pw):
            print("\nLogin Successful!")
            self.proposals() 
            self.display_table_interface()
        else:
            print("\nAccess Denied.")
            # replace with extended function

    def display_table_interface(self):
        name = input("Enter the table name to display: ")
        self.display_table(name) 


        
    # Admins: Create and manage users, Read Tables and Figures, Update and Delete records (binary fail / success)
    # Creators and Freelancers: Read Respective Tables and Figures, Update personal metrics, Propose new projects and ideas for approval, Delete own proposals and requests