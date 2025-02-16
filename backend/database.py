import sqlite3

DB_PATH = "security_fixes.db"

def init_db():
    """Initializes the database for tracking vulnerabilities and SLAs"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            impact TEXT,
            status TEXT DEFAULT 'Open',
            reported_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
