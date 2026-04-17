from auth import AuthSystem

class ManagementSystem(AuthSystem):
    def __init__(self, db_path):
        AuthSystem.__init__(self, db_path)
        
    def run_app(self):
        print("--- Encrypt Inc. OS ---")
        user = input("Username: ")
        pw = input("Password: ")
        
        # This calls the standard auth check
        user_type, first_name = self.authenticate_user(user, pw)
        
        if user_type:
            print(f"\nLogin Successful! Welcome: {first_name} // ({user_type.upper()})")
            if user_type == "Admin":
                # Admins can also view and accept / decline proposals sent by talent before deciding to search up and manipulate tables and records
                self.display_interface() 
            else:
                # Talent can only view their own records and can create proposals via algorithmic form; Pairings, Genre, Budget, etc.
                print(f"Accessing {user_type} Dashboard...")
                print()
        else:
            print("\nAccess Denied.")

    def display_interface(self):
        name = input("Enter the table name to display: ")
        self.display_table(name)
        
        
        
        