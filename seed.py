import sqlite3
import bcrypt

def plant_seeds(db_path):
    try:
        con = sqlite3.connect(db_path)
        cursor = con.cursor()
        
        agent_heads = [ 
            ('Daniel', 'Founder & CEO'),
            ('Griffin', 'COO'),
            ('Teni', 'CFO'),
            ('Sven', 'CCO'),
            ('Angela', 'Head of Product'), 
            ('Jade', 'Head of Legal'),
            ('Willow', 'Senior Data Scientist')]
        
        
        creators = [('Ethan', 'Head of Sales'),
            ('Olivia', 'Head of HR'),
            ('Noah', 'Head of Security')]
        
        # Seed with an admin user
        admin_username = ''
        admin_password = ''  
        # Hash the admin password
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert into either admin or freelancer user tables into the database
        cursor.execute(''' 
            INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)
        ''', (admin_username, hashed_password)) # should be an if statement to check if user already exists or RBA
        
        con.commit()
        print("Database seeded successfully.")
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        if 'con' in locals():
            con.close()