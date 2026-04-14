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
    
    def sign_up(self, email, username, password, table, first_name):
        conn, cursor = self.connect_database()
        hashed = self.hash_password(password)

        try:
            cursor.execute(f"SELECT Username FROM {table} WHERE ContactEmail = ?", (email,))
            cursor.execute(f"SELECT FirstName FROM {table} WHERE ContactEmail = ?", (email,))
            record = cursor.fetchone()

            if record:
                current_user = record[0]
                if current_user is None or current_user == "":
                    # VALIDATION: Only attach if a username hasn't been set yet
                    query = f"UPDATE {table} SET Username = ?, HashedPassword = ? WHERE ContactEmail = ?"
                    cursor.execute(query, (first_name, username, hashed, email))
                    print(f"[*] Identity Verified. Credentials attached to {email}")
                else:
                    print("[!] Error: This account is already registered.")
                    return None, None
            else:
                print("[!] Access Denied: Email not recognized in Encrypt Inc Registry.")
                return None, None

            conn.commit()
        except sqlite3.Error as e:
            print(f"Auth Error: {e}")

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
        self.sign_up("daniel@encrypt.com", "do3005", "crashcrash7", "Admins") 
        self.sign_up("a.crimson@encrypt.com", "acronims", "cruzofdreams", "Creators")