from database import get_connection

class Species:
    def __init__(self, species_id=None, name="", description=""):
        self.species_id = species_id
        self.name = name
        self.description = description

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.species_id is None:
            cursor.execute("INSERT INTO species (name, description) VALUES (?, ?)", 
                          (self.name, self.description))
            self.species_id = cursor.lastrowid
        else:
            cursor.execute("UPDATE species SET name=?, description=? WHERE species_id=?",
                          (self.name, self.description, self.species_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM species")
        rows = cursor.fetchall()
        conn.close()
        return [Species(*row) for row in rows]