from database import get_connection
from Models.category import Category

class Product:
    def __init__(self, product_id=None, name="", price=0, quantity_in_stock=0,
                 expiration_date=None, supplier_id=None, category_id=None):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity_in_stock = quantity_in_stock
        self.expiration_date = expiration_date
        self.supplier_id = supplier_id
        self.category_id = category_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.product_id is None:
            cursor.execute("""
            INSERT INTO products (name, price, quantity_in_stock, expiration_date, 
                                supplier_id, category_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (self.name, self.price, self.quantity_in_stock, self.expiration_date,
                 self.supplier_id, self.category_id))
            self.product_id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE products SET name=?, price=?, quantity_in_stock=?, expiration_date=?, 
                            supplier_id=?, category_id=?
            WHERE product_id=?
            """, (self.name, self.price, self.quantity_in_stock, self.expiration_date,
                 self.supplier_id, self.category_id, self.product_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT p.*, c.name 
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        """)
        rows = cursor.fetchall()
        conn.close()
        products = []
        for row in rows:
            product = Product(*row[:6])
            product.category_name = row[6] if row[6] else "Без категории"
            products.append(product)
        return products