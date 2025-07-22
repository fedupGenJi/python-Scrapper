import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import re
from sqlalchemy import create_engine, text

from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Get the variable
DATABASE = os.getenv("DATABASE_URL")

# Database connection
engine = create_engine(DATABASE)

# Read CSV
df = pd.read_csv("databaselaptop.csv", encoding='latin1')

# Clean RAM and Storage GB -> int
def clean_gb(value):
    try:
        return int(re.findall(r'\d+', str(value))[0])
    except:
        return random.randint(4, 64)  # fallback default

# Scrape images from Flipkart
def scrape_flipkart_images(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        imgs = soup.find_all('img')
        return [img['src'] for img in imgs if 'rukminim2.flixcart.com' in img.get('src', '')]
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

# Memory of previous values for fallback
previous_values = {}

# Use value if present, else pick a previous one or random fallback
def get_value(col_name, current_val, fallback=None):
    if pd.notna(current_val) and str(current_val).strip():
        val = str(current_val).strip()
        previous_values.setdefault(col_name, []).append(val)
        return val
    elif col_name in previous_values and previous_values[col_name]:
        return random.choice(previous_values[col_name])
    else:
        return fallback if fallback is not None else f"Unknown-{random.randint(1000,9999)}"

total_inserted = 0

# Process each row
for index, row in df.iterrows():
    try:
        display_name = get_value('display_name', row.get('name'), "Laptop Model")
        brand_name = display_name.split()[0] if display_name else "BrandX"
        model_name = get_value('model_name', row.get('Series'), "SeriesX")
        model_year_match = re.search(r'\((\d{4})\)', display_name)
        model_year = int(model_year_match.group(1)) if model_year_match else random.randint(2020, 2025)
        product_type = get_value('product_type', row.get('Type'), "Notebook")
        product_auth = random.choice(['authentic', 'grey', 'refurbished'])
        suitable_for = get_value('suitable_for', row.get('Suitable For'), "General Use")
        color = get_value('color', row.get('Color'), "Black")
        processor_generation = get_value('processor_generation', row.get('Processor Generation'), "10th Gen")
        processor = get_value('processor', row.get('Processor Brand'), "Intel")
        processor_series = get_value('processor_series', row.get('Processor Name'), "i5")
        ram = clean_gb(row.get('RAM'))
        ram_type = get_value('ram_type', row.get('RAM Type'), "DDR4")
        storage = clean_gb(row.get('SSD Capacity'))
        storage_type = 'ssd' if str(row.get('SSD')).strip().lower() == 'yes' else 'hdd'
        graphic = get_value('graphic', row.get('Graphic Processor'), "Intel UHD")
        graphic_ram = clean_gb(row.get('Dedicated Graphic Memory Capacity'))
        display = get_value('display', row.get('Screen Size'), "15.6 inch")
        display_type = get_value('display_type', row.get('Screen Type'), "IPS")
        touchscreen = str(row.get('Touchscreen')).strip().lower() == 'yes'
        power_supply = get_value('power_supply', row.get('Power Supply'), "65W")
        battery = get_value('battery', row.get('Battery'), "3 Cell Li-ion")
        warranty = get_value('warranty', row.get('Warranty'), "1 Year")
        
        # Price
        raw_price = str(row.get('Price'))
        price_match = re.search(r'\d[\d,]*\.?\d*', raw_price)
        cost_price = float(price_match.group(0).replace(',', '')) if price_match else round(random.uniform(30000, 80000), 2)
        
        # Quantity
        quantity = random.randint(5, 70)

        # Images
        image_urls = scrape_flipkart_images(row.get('link'))
        placeholder_image = "https://http.cat/404.jpg"

        if image_urls:
            face_image_url = image_urls[0]
            side_images = image_urls[1:7]
        else:
            face_image_url = placeholder_image
            side_images = [placeholder_image] * 3

        insert_query = text("""
            INSERT INTO laptop_details (
                brand_name, model_name, model_year, display_name, product_type,
                product_authentication, suitable_for, color, processor_generation, processor,
                processor_series, ram, ram_type, storage, storage_type, graphic,
                graphic_ram, display, display_type, touchscreen, power_supply, battery,
                warranty, cost_price, face_image_url, quantity
            )
            VALUES (
                :brand_name, :model_name, :model_year, :display_name, :product_type,
                :product_auth, :suitable_for, :color, :processor_generation, :processor,
                :processor_series, :ram, :ram_type, :storage, :storage_type, :graphic,
                :graphic_ram, :display, :display_type, :touchscreen, :power_supply, :battery,
                :warranty, :cost_price, :face_image_url, :quantity
            )
            RETURNING id;
        """)

        laptop_data = {
            'brand_name': brand_name,
            'model_name': model_name,
            'model_year': model_year,
            'display_name': display_name,
            'product_type': product_type,
            'product_auth': product_auth,
            'suitable_for': suitable_for,
            'color': color,
            'processor_generation': processor_generation,
            'processor': processor,
            'processor_series': processor_series,
            'ram': ram,
            'ram_type': ram_type,
            'storage': storage,
            'storage_type': storage_type,
            'graphic': graphic,
            'graphic_ram': graphic_ram,
            'display': display,
            'display_type': display_type,
            'touchscreen': touchscreen,
            'power_supply': power_supply,
            'battery': battery,
            'warranty': warranty,
            'cost_price': cost_price,
            'face_image_url': face_image_url,
            'quantity': quantity
        }

        print(f"\nInserting data for row {index}:")
        for key, value in laptop_data.items():
            print(f"  {key}: {value}")

        with engine.begin() as conn:
            result = conn.execute(insert_query, laptop_data)
            laptop_id = result.fetchone()[0]

            for url in side_images:
                conn.execute(text("""
                    INSERT INTO laptop_side_images (laptop_id, image_url)
                    VALUES (:laptop_id, :image_url)
                """), {'laptop_id': laptop_id, 'image_url': url})

        total_inserted += 1
        print(f"[✓] Inserted laptop: {display_name} (ID {laptop_id})")

    except Exception as e:
        print(f"[✗] Error processing row {index}: {e}")

print(f"\nTotal laptops inserted: {total_inserted}")