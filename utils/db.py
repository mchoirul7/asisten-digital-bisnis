import sqlite3
from config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT,
            name TEXT,
            qty INTEGER,
            date TEXT,
            data_period TEXT,
            data_hash TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(sku, name, qty, date, data_period, data_hash):
    conn = get_connection()
    try:
        conn.execute('''
            INSERT INTO inventory (sku, name, qty, date, data_period, data_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sku, name, qty, str(date), data_period, data_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def is_duplicate_row(data_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM inventory WHERE data_hash = ?", (data_hash,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def delete_data_by_period(period):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE data_period = ?", (period,))
    conn.commit()
    conn.close()

def reset_inventory():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory")
    conn.commit()
    conn.close()
