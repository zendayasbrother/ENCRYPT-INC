import os
from engine import ManagementSystem
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv() 
    db_path = os.getenv('DB_PATH') 
    
    if db_path and os.path.exists(db_path):
        app = ManagementSystem(db_path)
        
        # This handles the "Sign Up / Update" logic in the background
        app.plant_seeds() 
        
        # This launches the Username/Password prompt and Login Greeting
        app.run_app()
    else:
        print(f"Error: Database path is invalid or missing.")