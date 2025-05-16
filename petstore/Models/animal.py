from database import get_connection
from Models.species import Species

class Animal:
    def __init__(self, animal_id=None, date_of_birth=None, gender="", status="в наличии",
                 species_id=None, supplier_id=None, price=0):
        self.animal_id = animal_id
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.status = status
        self.species_id = species_id
        self.supplier_id = supplier_id
        self.price = price

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.animal_id is None:
            cursor.execute("""
            INSERT INTO animals (date_of_birth, gender, status, species_id, supplier_id, price)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (self.date_of_birth, self.gender, self.status, self.species_id, 
                 self.supplier_id, self.price))
            self.animal_id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE animals SET date_of_birth=?, gender=?, status=?, species_id=?, 
                            supplier_id=?, price=?
            WHERE animal_id=?
            """, (self.date_of_birth, self.gender, self.status, self.species_id,
                 self.supplier_id, self.price, self.animal_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT a.*, s.name 
        FROM animals a
        LEFT JOIN species s ON a.species_id = s.species_id
        """)
        rows = cursor.fetchall()
        conn.close()
        animals = []
        for row in rows:
            animal = Animal(*row[:6])
            animal.species_name = row[6] if row[6] else "Не указан"
            animals.append(animal)
        return animals