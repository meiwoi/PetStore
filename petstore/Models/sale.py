from database import get_connection
from datetime import date
from Models.animal import Animal
from Models.product import Product

class Sale:
    def __init__(self, sale_id=None, sale_date=None, employee_id=None, 
                 customer_id=None, total_price=0):
        self.sale_id = sale_id
        self.sale_date = sale_date
        self.employee_id = employee_id
        self.customer_id = customer_id
        self.total_price = total_price

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.sale_id is None:
            cursor.execute("""
            INSERT INTO sales (sale_date, employee_id, customer_id, total_price)
            VALUES (?, ?, ?, ?)
            """, (self.sale_date, self.employee_id, self.customer_id, self.total_price))
            self.sale_id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE sales SET sale_date=?, employee_id=?, customer_id=?, total_price=?
            WHERE sale_id=?
            """, (self.sale_date, self.employee_id, self.customer_id, self.total_price, self.sale_id))
        conn.commit()
        conn.close()

    def add_animal(self, animal_id, quantity=1):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM animals WHERE animal_id=?", (animal_id,))
        price = cursor.fetchone()[0]
        
        cursor.execute("""
        INSERT INTO sale_details (sale_id, animal_id, quantity, price)
        VALUES (?, ?, ?, ?)
        """, (self.sale_id, animal_id, quantity, price))
        
        cursor.execute("UPDATE animals SET status='продано' WHERE animal_id=?", (animal_id,))
        self.total_price += price * quantity
        conn.commit()
        conn.close()
        self.finalize()

    def add_product(self, product_id, quantity=1):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT price, quantity_in_stock FROM products WHERE product_id=?", (product_id,))
        price, current_quantity = cursor.fetchone()
        
        if current_quantity < quantity:
            print("❌ Недостаточно товара в наличии!")
            return
        
        cursor.execute("""
        INSERT INTO sale_details (sale_id, product_id, quantity, price)
        VALUES (?, ?, ?, ?)
        """, (self.sale_id, product_id, quantity, price))
        
        cursor.execute("UPDATE products SET quantity_in_stock = quantity_in_stock - ? WHERE product_id=?", 
                      (quantity, product_id))
        self.total_price += price * quantity
        conn.commit()
        conn.close()
        self.finalize()

    def apply_discount(self):
        if self.customer_id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT discount FROM customers WHERE customer_id=?", (self.customer_id,))
            result = cursor.fetchone()
            if result:
                discount = result[0]
                self.total_price *= (1 - discount / 100)
            conn.close()

    def finalize(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE sales SET total_price=? WHERE sale_id=?", 
                      (self.total_price, self.sale_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT sale_id, sale_date, employee_id, customer_id, total_price FROM sales")
        rows = cursor.fetchall()
        conn.close()
        return [Sale(*row) for row in rows]