from database import get_connection
from Models.position import Position

class Employee:
    def __init__(self, employee_id=None, last_name="", first_name="", hire_date=None,
                 phone="", position_id=None):
        self.employee_id = employee_id
        self.last_name = last_name
        self.first_name = first_name
        self.hire_date = hire_date
        self.phone = phone
        self.position_id = position_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.employee_id is None:
            cursor.execute("""
            INSERT INTO employees (last_name, first_name, hire_date, phone, position_id)
            VALUES (?, ?, ?, ?, ?)
            """, (self.last_name, self.first_name, self.hire_date, self.phone, self.position_id))
            self.employee_id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE employees SET last_name=?, first_name=?, hire_date=?, phone=?, position_id=?
            WHERE employee_id=?
            """, (self.last_name, self.first_name, self.hire_date, self.phone, 
                 self.position_id, self.employee_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT e.*, p.title 
        FROM employees e
        LEFT JOIN positions p ON e.position_id = p.position_id
        """)
        rows = cursor.fetchall()
        conn.close()
        employees = []
        for row in rows:
            employee = Employee(*row[:6])
            employee.position_title = row[6] if row[6] else "Без должности"
            employees.append(employee)
        return employees

    @staticmethod
    def get_by_id(employee_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT e.*, p.title 
        FROM employees e
        LEFT JOIN positions p ON e.position_id = p.position_id 
        WHERE e.employee_id = ?
        """, (employee_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            employee = Employee(*row[:6])
            employee.position_title = row[6]
            return employee
        return None