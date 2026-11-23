# database.py
# This file creates the SQLite database, tables, and inserts demo data.
# It uses only Python's built-in sqlite3 module - no extra install needed.

import sqlite3
from pathlib import Path

# The database file will be created in the project folder.
DB_PATH = Path(__file__).parent / "shop.db"


def get_connection():
    """
    Open a new connection to the SQLite database.
    row_factory = sqlite3.Row lets us access columns by name,
    for example: row["status"] instead of row[3].
    """
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    """Create the three tables if they do not already exist."""
    with get_connection() as connection:
        cursor = connection.cursor()

        # --- orders table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id        TEXT PRIMARY KEY,
                customer_name   TEXT NOT NULL,
                customer_email  TEXT NOT NULL,
                status          TEXT NOT NULL,
                estimated_delivery TEXT,
                items_summary   TEXT,
                created_at      TEXT NOT NULL
            )
        """)

        # --- products table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                name           TEXT NOT NULL,
                category       TEXT NOT NULL,
                price          REAL NOT NULL,
                specifications TEXT
            )
        """)

        # --- tickets table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id      TEXT PRIMARY KEY,
                customer_name  TEXT,
                message        TEXT NOT NULL,
                issue_type     TEXT NOT NULL,
                status         TEXT NOT NULL,
                created_at     TEXT NOT NULL
            )
        """)

        connection.commit()


def insert_demo_data():
    """
    Insert demo orders and products.
    INSERT OR IGNORE means: if the row already exists, skip it.
    This makes the function safe to run multiple times.
    """
    with get_connection() as connection:
        cursor = connection.cursor()

        # --- Demo orders (6 sample orders) ---
        demo_orders = [
            ("ORD-1001", "Rahim Ahmed",  "rahim@example.com",  "Shipped",    "2026-10-20", "2 x Wireless Earbuds", "2026-10-14"),
            ("ORD-1002", "Fatema Khan",  "fatema@example.com", "Delivered",  "2026-10-12", "1 x Smart Watch",      "2026-10-10"),
            ("ORD-1003", "Karim Hossain","karim@example.com",  "Processing", "2026-10-22", "3 x Cotton T-Shirt",   "2026-10-16"),
            ("ORD-1004", "Nusrat Jahan", "nusrat@example.com", "Pending",    "2026-10-25", "1 x Bluetooth Speaker","2026-10-17"),
            ("ORD-1005", "Sabbir Rahman","sabbir@example.com", "Cancelled",  None,         "1 x Phone Case",       "2026-10-13"),
            ("ORD-1006", "Ayesha Siddika","ayesha@example.com","Confirmed",  "2026-10-23", "1 x Laptop Backpack",  "2026-10-16"),
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO orders
            (order_id, customer_name, customer_email, status, estimated_delivery, items_summary, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, demo_orders)

        # --- Demo products (10 sample products) ---
        demo_products = [
            ("Wireless Earbuds",     "Electronics",  1500.00, "Bluetooth 5.2, 6h battery, IPX4 water resistant"),
            ("Smart Watch",          "Electronics",  3500.00, "1.8 inch display, heart rate monitor, 7 days battery"),
            ("Bluetooth Speaker",    "Electronics",  2200.00, "10W output, 12h playtime, waterproof"),
            ("Cotton T-Shirt",       "Clothing",      450.00, "100% cotton, sizes S/M/L/XL, 6 colors"),
            ("Laptop Backpack",      "Accessories",  1200.00, "Water resistant, 15.6 inch laptop compartment, USB port"),
            ("Phone Case",           "Accessories",   250.00, "Shockproof, fits iPhone 13/14/15"),
            ("Running Shoes",        "Footwear",     2800.00, "Lightweight, sizes 39-45, breathable mesh"),
            ("Office Chair",         "Home",         8500.00, "Ergonomic design, adjustable height, lumbar support"),
            ("LED Desk Lamp",        "Home",          850.00, "3 brightness levels, USB charging port, touch control"),
            ("Smartphone Charger",   "Electronics",   650.00, "65W fast charging, USB-C, 1.5m cable"),
        ]

        cursor.executemany("""
            INSERT INTO products (name, category, price, specifications)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM products WHERE name = ?
            )
        """, [(p[0], p[1], p[2], p[3], p[0]) for p in demo_products])

        connection.commit()


def initialize_database():
    """
    Main entry point.
    Call this once at app startup - creates tables and demo data safely.
    """
    create_tables()
    insert_demo_data()


# -------------------------------------------------------------------
# Allow running this file directly to initialize the DB manually:
#     python database.py
# -------------------------------------------------------------------
if __name__ == "__main__":
    initialize_database()
    print("Database initialized at:", DB_PATH)

    # Show summary so you can verify
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tickets")
        ticket_count = cursor.fetchone()[0]

    print(f"Orders: {order_count}")
    print(f"Products: {product_count}")
    print(f"Tickets: {ticket_count}")