import bcrypt
import os
import sqlite3

class AuthSystem: 
    def __init__(self, db_path):
        self.db_path = db_path

    def hash_password(self, password):
        # Generates a secure salt and hashes the password
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def authenticate_user(self, username, password):
        if not self.db_path or not os.path.exists(self.db_path):
            print(f"Error: Database file not found at {self.db_path}")
            return False
            
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            # Select the hashed password for the given username
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            
            if result:
                stored_hash = result[0]
                # If stored as string in SQLite, convert to bytes
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode('utf-8')
                
                # Compare entered password with stored hash
                return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
                
        except sqlite3.Error as error:
            print(f"Database error: {error}")
        finally:
            if 'con' in locals():
                con.close()
        
        return False