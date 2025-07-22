from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Get the variable
DATABASE = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE)

drop_tables_sql = """
DROP TABLE IF EXISTS laptop_side_images CASCADE;
DROP TABLE IF EXISTS laptop_details CASCADE;
"""

create_laptop_details_sql = """
CREATE TABLE IF NOT EXISTS laptop_details (
    id SERIAL PRIMARY KEY,
    brand_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_year INTEGER,
    display_name TEXT,
    product_type TEXT,
    product_authentication TEXT,
    suitable_for TEXT,
    color TEXT,
    processor_generation TEXT,
    processor TEXT,
    processor_series TEXT,
    ram INTEGER,
    ram_type TEXT,
    storage INTEGER,
    storage_type TEXT,
    graphic TEXT,
    graphic_ram INTEGER,
    display TEXT,
    display_type TEXT,
    touchscreen BOOLEAN,
    power_supply TEXT,
    battery TEXT,
    warranty TEXT,
    cost_price NUMERIC(10, 2) NOT NULL,
    show_price NUMERIC(10, 2) GENERATED ALWAYS AS (cost_price + cost_price * 0.18) STORED,
    face_image_url TEXT, 
    quantity INTEGER DEFAULT 0
);
"""

create_laptop_side_images_sql = """
CREATE TABLE IF NOT EXISTS laptop_side_images (
    id SERIAL PRIMARY KEY,
    laptop_id INTEGER REFERENCES laptop_details(id) ON DELETE CASCADE,
    image_url TEXT  
);
"""

def recreate_tables():
    with engine.begin() as conn:
        print("Dropping existing tables if any...")
        conn.execute(text(drop_tables_sql))
        print("Creating table laptop_details...")
        conn.execute(text(create_laptop_details_sql))
        print("Creating table laptop_side_images...")
        conn.execute(text(create_laptop_side_images_sql))
    print("Tables recreated successfully.")

if __name__ == "__main__":
    recreate_tables()
