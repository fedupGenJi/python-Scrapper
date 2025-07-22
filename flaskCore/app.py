from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Get the variable
DATABASE = os.getenv("DATABASE_URL")

app = Flask(__name__)

engine = create_engine(DATABASE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/laptops')
def get_laptops():
    query = text("SELECT * FROM laptop_details ORDER BY id DESC LIMIT 1100;")
    with engine.begin() as conn:
        result = conn.execute(query).mappings()
        laptops = [dict(row) for row in result]
    return jsonify(laptops)

if __name__ == '__main__':
    app.run(debug=True)
