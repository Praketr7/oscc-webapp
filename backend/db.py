import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "oscc_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Barcelona@2025")
DB_PORT = os.getenv("DB_PORT", 5432)

def get_connection():
    """Returns a psycopg2 connection suitable for pandas"""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
        # Do NOT set cursor_factory=RealDictCursor for pandas
    )

# Usage
conn = get_connection()

conn.close()
