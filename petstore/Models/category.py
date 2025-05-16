from database import get_connection

class Category:
    def __init__(self, category_id=None, name="", description=""):
        self.category_id = category_id
        self.name = name
        self.description = description

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.category_id is None:
            cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)",
                          (self.name, self.description))
            self.category_id = cursor.lastrowid
        else:
            cursor.execute("UPDATE categories SET name=?, description=? WHERE category_id=?",
                          (self.name, self.description, self.category_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        rows = cursor.fetchall()
        conn.close()
        return [Category(*row) for row in rows]