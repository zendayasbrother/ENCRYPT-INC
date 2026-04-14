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
    
    def access_portal(self, first_name, last_name, username, password, role, table):
        """Unified function: Checks database, Updates if exists, Inserts if new."""
        conn, cursor = self.connect_database()
        if not conn: return None, None

        try:
            hashed = self.hash_password(password)
            
            # Check if user exists
            cursor.execute(f"SELECT Username FROM {table} WHERE Username = ?", (username,))
            exists = cursor.fetchone()

            if exists:
                # Update query (Existing Record)
                query = f"UPDATE {table} SET HashedPassword = ? WHERE Username = ?"
                cursor.execute(query, (hashed, username))
                print(f"[*] Credentials synced for: {username}")
            else:
                # Sign Up query (New Record)
                if table == "Admins":
                    query = f"INSERT INTO Admins (FirstName, LastName, Role, Username, HashedPassword) VALUES (?, ?, ?, ?, ?)"
                    params = (first_name, last_name, role, username, hashed)
                elif table == "Creators":
                    query = f'INSERT INTO Creators (FirstName, LastName, "Primary Niche", "Secondary Niche", Country, Username, HashedPassword) VALUES (?, ?, ?, ?, ?, ?, ?)'
                    params = (first_name, last_name, role, "General", "Unknown", username, hashed)
                
                cursor.execute(query, params)
                print(f"[+] New account created for: {username}")
            
            conn.commit()
            # After updating/inserting, return the data for the Greeting
            return table, first_name

        except sqlite3.Error as e:
            print(f"Portal Error: {e}")
            return None, None
        finally:
            conn.close()

    def authenticate_user(self, username, password):
        conn, cursor = self.connect_database()
        if not conn: return None, None
        tables = ["Admins", "Creators", "Freelancers"]
        for table in tables:
            try:
                cursor.execute(f"SELECT HashedPassword, FirstName FROM {table} WHERE Username = ?", (username,))
                result = cursor.fetchone()
                if result and self.check_password(password, result[0]):
                    fn = result[1]
                    conn.close()
                    return table, fn
            except sqlite3.Error:
                continue 
        if conn: conn.close()
        return None, None
        
    def plant_seeds(self):
        # One fell swoop: Syncs/Creates and could theoretically log them in
        self.access_portal("Daniel", "Founder", "do3005", "crashcrash7", "Founder & CEO", "Admins")
        self.access_portal("Alex", "Crimson", "a.crimson", "cruzofdreams", "Tech", "Creators")