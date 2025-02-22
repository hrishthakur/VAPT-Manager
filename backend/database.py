import psycopg2
from psycopg2 import Error
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "vapt_manager"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "port": os.getenv("DB_PORT", "5432"),
}


def init_db():
    """Initializes the database for tracking vulnerabilities and SLAs"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id SERIAL PRIMARY KEY,
                name TEXT,
                description TEXT,
                impact TEXT,
                status TEXT DEFAULT 'Open',
                reported_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()
