import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv()

def obtain_motor():
    return os.getenv("DB_ENGINE", "sqlite").lower()

def open_connection():
    motor = obtain_motor()

    if motor == "sqlite":
        return sqlite3.connect(os.getenv("DB_NAME", "adventure_travel.db"))

    if motor == "mysql":
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            )
    raise ValueError(f"Motor no soportado: {motor}")

def marker_sql():
    if obtain_motor() == "sqlite":
        return "?"
    return "%s"

connection = None
try:
    connection = open_connection()
    cursor = connection.cursor()

    connection.commit()

except Exception:
    if connection:
        connection.rollback()
    raise

finally:
    if connection:
        connection.close()
        
def get_connection():
    """Alias compatibility wrapper for open_connection."""
    conn = open_connection()
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn        

def get_engine() -> str:
    """Returns the database engine identifier ('sqlite' by default)."""
    return "sqlite"