import sqlite3, os

os.makedirs('data/shop', exist_ok=True)
path = 'data/shop/seed.db'
if os.path.exists(path):
    os.remove(path)
con = sqlite3.connect(path)
con.executescript(open('data/shop/schema.sql', encoding='utf-8').read())

con.executemany('INSERT INTO customers VALUES(?,?,?)', [
    ('C01', 'Lan', '0900000001'), ('C02', 'Minh', '0900000002'),
    ('C03', 'Hà', '0900000003'), ('C04', 'Tuấn', '0900000004'),
    ('C05', 'Mai', '0900000005')])
con.executemany('INSERT INTO products VALUES(?,?,?,?)', [
    ('P01', 'Aurora X5', 'phone', 6990000), ('P02', 'Nova Buds 2', 'earbuds', 890000),
    ('P03', 'Nova Buds Pro', 'earbuds', 1690000), ('P04', 'Pulse Watch S2', 'watch', 2490000),
    ('P05', 'Ion Charger 65W', 'charger', 490000), ('P06', 'Aurora X5 Case', 'case', 190000)])
con.executemany('INSERT INTO inventory VALUES(?,?,?)', [
    ('P01', 'xanh', 5), ('P01', 'đen', 0), ('P02', 'trắng', 12), ('P03', 'đen', 3),
    ('P04', 'đen', 0), ('P05', '-', 40), ('P06', '-', 25)])
con.executemany('INSERT INTO orders VALUES(?,?,?,?,?)', [
    ('TN-1001', 'C01', 'delivered', '2026-11-07', 'Hà Nội'),
    ('TN-1002', 'C01', 'delivered', '2026-10-29', 'Hà Nội'),
    ('TN-1003', 'C02', 'delivered', '2026-11-05', 'TP.HCM'),
    ('TN-1004', 'C02', 'shipping', None, 'TP.HCM'),
    ('TN-1005', 'C03', 'delivered', '2026-10-21', 'Đà Nẵng'),
    ('TN-1006', 'C03', 'cancelled', None, 'Đà Nẵng'),
    ('TN-1007', 'C04', 'delivered', '2026-11-08', 'Cần Thơ'),
    ('TN-1008', 'C05', 'processing', None, 'Hà Nội')])
con.executemany('INSERT INTO order_items VALUES(?,?,?,?,?,?)', [
    ('TN-1001', 'P02', 'trắng', 1, 0, 0), ('TN-1002', 'P01', 'xanh', 1, 0, 0),
    ('TN-1003', 'P01', 'đen', 1, 1, 1), ('TN-1004', 'P03', 'đen', 1, 0, 0),
    ('TN-1005', 'P04', 'đen', 1, 1, 1), ('TN-1006', 'P05', '-', 1, 0, 0),
    ('TN-1007', 'P02', 'trắng', 1, 0, 1), ('TN-1008', 'P05', '-', 1, 0, 0),
    ('TN-1008', 'P06', '-', 1, 0, 0)])
con.commit()
con.close()