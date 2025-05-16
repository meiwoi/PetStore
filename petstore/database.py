import sqlite3
from config import DB_NAME

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Клиенты
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        discount REAL DEFAULT 0
    )
    ''')

    # Виды животных
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS species (
        species_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    ''')

    # Животные
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS animals (
        animal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_of_birth DATE NOT NULL,
        gender TEXT,
        status TEXT DEFAULT 'в наличии',
        species_id INTEGER,
        supplier_id INTEGER,
        price REAL,
        FOREIGN KEY (species_id) REFERENCES species(species_id),
        FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    )
    ''')

    # Категории товаров
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    ''')

    # Товары
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity_in_stock INTEGER DEFAULT 0,
        expiration_date DATE,
        supplier_id INTEGER,
        category_id INTEGER,
        FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    )
    ''')
    
    # Должности
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS positions (
        position_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        salary REAL NOT NULL,
        description TEXT
    )
    ''')

    # Сотрудники
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        hire_date DATE NOT NULL,
        phone TEXT,
        position_id INTEGER,
        FOREIGN KEY (position_id) REFERENCES positions(position_id)
    )
    ''')

    # Поставщики
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_person TEXT,
        phone TEXT,
        email TEXT
    )
    ''')

    # Продажи
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_date DATE NOT NULL,
        employee_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        total_price REAL NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    ''')
    
    # Детали продаж
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sale_details (
        sale_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER,
        product_id INTEGER,
        animal_id INTEGER,
        quantity INTEGER DEFAULT 1,
        price REAL NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (animal_id) REFERENCES animals(animal_id)
    )
    ''')

    conn.commit()
    conn.close()