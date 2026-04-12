import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect_database(self):
        if not self.db_path or not os.path.exists(self.db_path):
            print(f"Error: Database file not found at {self.db_path}")
            return None, None
            
        try:
            con = sqlite3.connect(self.db_path, uri =True)
            cursor = con.cursor()
            
            # Security & Health Check
            cursor.execute("PRAGMA integrity_check;")
            if cursor.fetchone()[0] == "ok":
                return con, cursor
        except sqlite3.Error as error:
            print(f"Database error: {error}")
            return None, None
        
    def proposals(self):
        conn, cursor = self.connect_database()
        if cursor:
            try:
                cursor.execute("SELECT * FROM proposals")
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching proposals: {e}")
            finally:
                conn.close()
        return [] # first, admin window, then talent inputs and requests
    

    def display_table(self, table_name):
        conn, _ = self.connect_database()
        if conn:
            try:
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                print(f"\n--- {table_name} Table ---")
                print(df)
            except Exception as e:
                print(f"Error reading table: {e}")
            finally:
                conn.close()