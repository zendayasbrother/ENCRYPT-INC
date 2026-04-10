import os
import sqlite3
import bcrypt
from dotenv import load_dotenv

# Assuming DataManager is a base class that handles basic connection logic
# from database import DataManager 

load_dotenv()

class SeedData: 
    def __init__(self): 
        # Encapsulation: Pulling the path from .env and making it a private attribute
        self.__db_path = os.getenv('DB_PATH')
        if not self.__db_path:
            raise ValueError("DB_PATH not found in environment variables.")

    def __hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def plant_seeds(self):
        agent_heads = [ 
            ('Daniel', 'Onyeakazi', 'M', 'Founder', 'crashcrash7'),
            ('Griffin', 'Lawson', 'M', 'Chief Operations Officer - Legal', 'legakeg'),
            ('Teni', 'Olayinka', 'F', 'Chief Financial Officer', 'breakabread'),
            ('Sven', 'Talefson', 'M', 'Chief Brand & Communications Officer', 'olafchat'),
            ('Angela', 'Keith', 'F', 'Head of Product', 'justatumble'), 
            ('Jade', 'Zhang', 'F', 'Head of Legal Operations', 'valleychrono'),
            ('Willow', 'Youn', 'F', 'Senior Data Scientist', 'wrangelieth')
        ]

        try:
            with sqlite3.connect(self.__db_path) as con:
                cursor = con.cursor()
                
                query = """
                    INSERT INTO Admins (FirstName, LastName, Sex, Role, HashedPassword) 
                    VALUES (?, ?, ?, ?, ?)
                """
                
                for first, last, sex, role, plain_password in agent_heads:
                    hashed = self.__hash_password(plain_password)
                    cursor.execute(query, (first, last, sex, role, hashed))
                
                con.commit()
                print(f"Successfully seeded {len(agent_heads)} admins.")

        except sqlite3.Error as error:
            print(f"Database error: {error}")

if __name__ == "__main__":
    seeder = SeedData()
    seeder.plant_seeds()