from database import get_connection

class Supplier:
    def __init__(self, supplier_id=None, name="", contact_person="", phone="", email=""):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_person = contact_person
        self.phone = phone
        self.email = email

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.supplier_id is None:
            cursor.execute("""
            INSERT INTO suppliers (name, contact_person, phone, email)
            VALUES (?, ?, ?, ?)
            """, (self.name, self.contact_person, self.phone, self.email))
            self.supplier_id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE suppliers SET name=?, contact_person=?, phone=?, email=?
            WHERE supplier_id=?
            """, (self.name, self.contact_person, self.phone, self.email, self.supplier_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suppliers")
        rows = cursor.fetchall()
        conn.close()
        return [Supplier(*row) for row in rows]