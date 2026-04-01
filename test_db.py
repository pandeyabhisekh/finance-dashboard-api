import sys
import os
from sqlalchemy import inspect

# Add the current directory to sys.path so we can import 'app'
sys.path.append(os.getcwd())

from app.db.session import engine
from app.models.user import User
from app.models.transaction import Transaction

def test_connection():
    try:
        # Try to connect
        with engine.connect() as connection:
            print("Successfully connected to the database!")
            
            # Check if tables exist
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"Existing tables: {tables}")
            
            required_tables = ['users', 'transactions']
            for table in required_tables:
                if table in tables:
                    print(f"Table '{table}' exists.")
                else:
                    print(f"Table '{table}' is MISSING.")
                    
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    test_connection()
