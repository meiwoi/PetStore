from database import get_connection

class Customer:
    def __init__(self, customer_id=None, first_name="", last_name="", phone="", email="", discount=0):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.discount = discount

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.customer_id is None:
            cursor.execute("""
            INSERT INTO customers (first_name, last_name, phone, email, discount)
            VALUES (?, ?, ?, ?, ?)
            """, (self.first_name, self.last_name, self.phone, self.email, self.discount))
            self.customer_id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE customers SET first_name=?, last_name=?, phone=?, email=?, discount=?
            WHERE customer_id=?
            """, (self.first_name, self.last_name, self.phone, self.email, self.discount, self.customer_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        conn.close()
        return [Customer(*row) for row in rows]

    @staticmethod
    def get_by_id(customer_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_id=?", (customer_id,))
        row = cursor.fetchone()
        conn.close()
        return Customer(*row) if row else None