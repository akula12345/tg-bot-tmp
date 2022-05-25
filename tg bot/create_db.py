import sqlite3

db = sqlite3.connect('shop.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INT
)
""")

sql.execute("""CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name INT,
    category TEXT,
    size TEXT,
    price INt
)
""")

sql.execute("""CREATE TABLE IF NOT EXISTS shoppingCart  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INT,
    name INT,
    category TEXT,
    size TEXT,
    price INt
)
""")