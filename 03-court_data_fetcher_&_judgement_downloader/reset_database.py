import sqlite3
import os

def reset_database():
    """Reset the database with correct schema"""
    if os.path.exists('court_cases.db'):
        os.remove('court_cases.db')
        print("✅ Old database removed")
    
    conn = sqlite3.connect('court_cases.db')
    c = conn.cursor()
    
    # Create case_queries table with correct columns
    c.execute('''
        CREATE TABLE IF NOT EXISTS case_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_number TEXT,
            year INTEGER,
            court_code TEXT,
            state_code TEXT,
            dist_code TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            raw_response TEXT,
            parsed_data TEXT
        )
    ''')
    
    # Create cause_lists table
    c.execute('''
        CREATE TABLE IF NOT EXISTS cause_lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            court_name TEXT,
            court_code TEXT,
            list_date DATE,
            raw_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ New database created with correct schema")

if __name__ == "__main__":
    reset_database()