from auth import AuthSystem

class ManagementSystem(AuthSystem):
    def __init__(self, db_path):
        AuthSystem.__init__(self, db_path)
        
    def proposals(self):
        conn, cursor = self.connect_database()
        if cursor:
            try:
                cursor.execute("SELECT * FROM Proposals")
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching proposals: {e}")
            finally:
                conn.close()
        return []
    
    def run_app(self):
        print("--- Encrypt Inc. OS ---")
        user = input("Username: ")
        pw = input("Password: ")
        
        
        user_type, first_name = self.authenticate_user(user, pw)
        
        if user_type:
            # Now you can use first_name here!
            print(f"{user_type.upper()}")
            print(f"\nLogin Successful! Welcome: {first_name} // ({user})") 
            
            if user_type == "Admins":
                self.display_interface() 
            else:
                print(f"Accessing Talent Dashboard for {first_name}...")
        else:
            print("\nAccess Denied.") 
            
    def display_interface(self):
        name = input("Enter the table name to display: ")
        self.display_table(name)