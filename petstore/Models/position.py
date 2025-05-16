from database import get_connection

class Position:
    def __init__(self, position_id=None, title="", salary=0, description=""):
        self.position_id = position_id
        self.title = title
        self.salary = salary
        self.description = description

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.position_id is None:
            cursor.execute("INSERT INTO positions (title, salary, description) VALUES (?, ?, ?)",
                          (self.title, self.salary, self.description))
            self.position_id = cursor.lastrowid
        else:
            cursor.execute("UPDATE positions SET title=?, salary=?, description=? WHERE position_id=?",
                          (self.title, self.salary, self.description, self.position_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM positions")
        rows = cursor.fetchall()
        conn.close()
        return [Position(*row) for row in rows]