import os
from engine import ManagementSystem
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv() 
    db_path = os.getenv('DB_PATH') 
    
    app = ManagementSystem(db_path)
    app.plant_seeds() # This will only add them if they don't exist
    app.run_app()     # This starts your "Sign Up / Login > Credentials" flow