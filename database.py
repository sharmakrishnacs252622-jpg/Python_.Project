import sqlite3
import json

DB_NAME = "restaurant.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            table_number INTEGER NOT NULL,
            items TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def add_order(user_id, table_number, items_dict, total):
    items_json = json.dumps(items_dict)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO orders (user_id, table_number, items, total)
        VALUES (?, ?, ?, ?)
    """, (user_id, table_number, items_json, total))
    conn.commit()
    conn.close()


def get_orders_by_status(status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT o.id, u.username, o.table_number, o.items,
               o.total, o.status, o.created_at
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.status=?
        ORDER BY o.created_at
    """, (status,))

    rows = c.fetchall()
    conn.close()

    orders = []
    for row in rows:
        orders.append({
            "id": row[0],
            "username": row[1],
            "table_number": row[2],
            "items": json.loads(row[3]),
            "total": row[4],
            "status": row[5],
            "created_at": row[6]
        })
    return orders


def update_status(order_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
    conn.commit()
    conn.close()

def delete_order(order_id):
    import sqlite3
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()


def delete_completed_orders():
    import sqlite3
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM orders WHERE status='completed'")
    conn.commit()
    conn.close()    