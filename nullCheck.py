from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Get the variable
DATABASE = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE)

def check_nulls():
    inspector = inspect(engine)
    found_null = False  # Flag to track if any NULL is found
    
    try:
        with engine.connect() as conn:
            tables = inspector.get_table_names()
            for table in tables:
                print(f"\nChecking table: {table}")
                columns = [col['name'] for col in inspector.get_columns(table)]
                
                result = conn.execute(text(f"SELECT * FROM {table}"))
                rows = result.mappings().all()
                
                if not rows:
                    print("  No rows found.")
                    continue
                
                for idx, row in enumerate(rows, start=1):
                    null_columns = [col for col in columns if row[col] is None]
                    if null_columns:
                        found_null = True
                        print(f"  Row {idx} has NULL in columns: {null_columns}")
            
            if not found_null:
                print("\nNo NULL values found in any table!")
            else:
                print("\nNULL values exist in the database.")
    
    except SQLAlchemyError as e:
        print("Database error:", e)


if __name__ == "__main__":
    check_nulls()
