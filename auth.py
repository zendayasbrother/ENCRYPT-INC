import bcrypt
import sqlite3  
from database import DataManager

class AuthSystem(DataManager): 
    def __init__(self, db_path):
        super().__init__(db_path)

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def sign_up(self, first_name, last_name, username, password, role, table):
        conn, cursor = self.connect_database()
        if not conn: return

        try:
            # BASE COVERED: Check if username already exists
            cursor.execute(f"SELECT Username FROM {table} WHERE Username = ?", (username,))
            if cursor.fetchone():
                print(f"[-] Record for '{username}' already exists. No new row added.")
                return

            hashed = self.hash_password(password)
            
            if table == "Admins":
                query = '''INSERT INTO Admins (FirstName, LastName, Role, Username, HashedPassword) 
                           VALUES (?, ?, ?, ?, ?)'''
                params = (first_name, last_name, role, username, hashed)
            
            elif table == "Creators":
                query = '''INSERT INTO Creators (FirstName, LastName, "Primary Niche", "Secondary Niche", 
                           Country, Username, HashedPassword) VALUES (?, ?, ?, ?, ?, ?, ?)'''
                params = (first_name, last_name, role, "General", "Unknown", username, hashed)
            
            cursor.execute(query, params)
            conn.commit()
            print(f"[+] User '{username}' registered successfully.")
        except sqlite3.Error as e:
            print(f"Signup error: {e}")
        finally:
            conn.close()

    def authenticate_user(self, username, password):
        conn, cursor = self.connect_database()
        if not conn: return None, None

        tables = ["Admins", "Creators", "Freelancers"]
        for table in tables:
            try:
                # Fetches password for check and FirstName for the greeting
                cursor.execute(f"SELECT HashedPassword, FirstName FROM {table} WHERE Username = ?", (username,))
                result = cursor.fetchone()
                
                if result and self.check_password(password, result[0]):
                    first_name = result[1]
                    conn.close()
                    return table, first_name 
            except sqlite3.Error:
                continue 
        
        if conn: conn.close()
        return None, None
        
    def plant_seeds(self):
        # Now uses sign_up correctly with the right amount of arguments
        self.sign_up("Daniel", "Founder", "do3005", "crashcrash7", "Founder & CEO", "Admins")
        self.sign_up("Alex", "Crimson", "a.crimson", "cruzofdreams", "Tech", "Creators")