import os
import pandas as pd 
import sqlite3 
from auth import AuthSystem
from database import DataManager
from engine import ManagementSystem
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv() 
    db_path = os.getenv('DB_PATH') 
    
    if db_path and os.path.exists(db_path):
        app = ManagementSystem(db_path)
        app.run_app()
    else:
        print(f"Error: Database path '{db_path}' is invalid or missing.")