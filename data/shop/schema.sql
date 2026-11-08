CREATE TABLE customers(id TEXT PRIMARY KEY, name TEXT, phone TEXT);
CREATE TABLE products(id TEXT PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
CREATE TABLE inventory(product_id TEXT, variant TEXT, stock INTEGER, PRIMARY KEY(product_id, variant));
CREATE TABLE orders(id TEXT PRIMARY KEY, customer_id TEXT, status TEXT, delivered_at TEXT, city TEXT);
CREATE TABLE order_items(order_id TEXT, product_id TEXT, variant TEXT, qty INTEGER,
  activated INTEGER DEFAULT 0, opened INTEGER DEFAULT 0, PRIMARY KEY(order_id, product_id, variant));
CREATE TABLE returns(id INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT, product_id TEXT, reason TEXT, status TEXT);
CREATE TABLE escalations(id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, reason TEXT, summary TEXT);