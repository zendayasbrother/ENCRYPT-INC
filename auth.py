import bcrypt
import sqlite3  
from database import DataManager

class AuthSystem(DataManager): 
    def __init__(self, db_path):
        super().__init__(db_path)

    def hash_password(self, password):
        # bcrypt handles salt generation automatically
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, password, hashed):
        # hashed contains the salt, the algorithm version, and the hash itself
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def sign_up(self, first_name, last_name, username, password, role, table):
        hashed = self.hash_password(password)
        conn, cursor = self.connect_database()
        if conn:
            try:
                # Username is added penultimately (right before the HashedPassword)
                if table == "Admins":
                    query = '''INSERT INTO Admins (FirstName, LastName, Role, Username, HashedPassword) 
                               VALUES (?, ?, ?, ?, ?)'''
                    params = (first_name, last_name, role, username, hashed)
                
                elif table == "Creators":
                    query = '''INSERT INTO Creators (FirstName, LastName, "Primary Niche", "Secondary Niche", 
                               Country, Username, HashedPassword) VALUES (?, ?, ?, ?, ?, ?, ?)'''
                    params = (first_name, last_name, "General", "General", "Unknown", username, hashed)
                
                elif table == "Freelancers":
                    query = '''INSERT INTO Freelancers (FirstName, LastName, Role, Username, HashedPassword) 
                               VALUES (?, ?, ?, ?, ?)'''
                    params = (first_name, last_name, role, username, hashed)

                cursor.execute(query, params)
                conn.commit()
                print(f"User '{username}' registered successfully in {table}.")
            except sqlite3.Error as e:
                print(f"Signup error: {e}")
            finally:
                conn.close()

    def authenticate_user(self, username, password):
        conn, cursor = self.connect_database()
        if not conn: 
            return None

        # Searching across tables specifically by the new 'Username' column
        tables = ["Admins", "Creators", "Freelancers"]
        for table in tables:
            try:
                # We select the HashedPassword where the Username matches
                cursor.execute(f"SELECT HashedPassword FROM {table} WHERE Username = ?", (username,))
                result = cursor.fetchone()
                
                if result and self.check_password(password, result[0]):
                    conn.close()
                    return table # Successful login returns the table (Role)
            except sqlite3.Error:
                continue 
        
        if conn:
            conn.close()
        return None
        
    def plant_seeds(self):
        # Admin seed
        self.sign_up("Daniel", "Founder", "do3005", "crashcrash7", "Founder & CEO", "Admins")
        
        # Updated Creator seed to match a record from your database (Alex Crimson)
        self.sign_up("Alex", "Crimson", "a.crimson", "cruzofdream", "Tech", "Creators")
        