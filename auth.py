import os
import bcrypt
import sqlite3  
from database import DataManager

class AuthSystem: 
    def __init__(self, db_path):
        self.db_path = db_path

    def hash_password(self, password):
        # Generates a secure salt and hashes the password
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, password, hashed):
        # Compares the provided password with the stored hashed password
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def sign_up(self, username, password, role):
        if not self.db_path or not os.path.exists(self.db_path):
            print(f"Error: Database file not found at {self.db_path}")
            return False # replace with extended function
        
        hashed = self.hash_password(password)
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO Users (Username, Password, Role)
                    VALUES (?, ?, ?)
                ''', (username, hashed, role))
                conn.commit()
                print(f"User {username} registered successfully.")
        except sqlite3.IntegrityError:
            print("Error: Username already exists.")
        

    
    def authenticate_user(self, username, password):
        if not self.db_path or not os.path.exists(self.db_path):
            print(f"Error: Database file not found at {self.db_path}")
            return False # replace with extended function
        
        # Authentication logic here, checking against the database
        # sign up: hash the password and store it in the database, doesn't use plant_seeds() function, just a one time setup for the admin user
        # log in: retrieve the hashed password from the database and compare it with the provided password using bcrypt.checkpw() in plant_seeds()
        pass
        
def plant_seeds(db_path):
    try:
        con = sqlite3.connect(db_path)
        cursor = con.cursor()
        
        agent_heads = [ 
            ('Daniel', 'Founder & CEO'),
            ('Griffin', 'COO'),
            ('Teni', 'CFO'),
            ('Sven', 'CCO'),
            ('Angela', 'Head of Product'), 
            ('Jade', 'Head of Legal'),
            ('Willow', 'Senior Data Scientist')]
        
        
        creators = [('Ethan', 'Head of Sales'),
            ('Olivia', 'Head of HR'),
            ('Noah', 'Head of Security')]
        
        # Seed with an admin user
        admin_username = ''
        admin_password = ''  
        # Hash the admin password
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert into either admin or freelancer user tables into the database
        cursor.execute(''' 
            INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)
        ''', (admin_username, hashed_password)) # should be an if statement to check if user already exists or RBA
        
        con.commit()
        print("Database seeded successfully.")
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        if 'con' in locals():
            con.close()