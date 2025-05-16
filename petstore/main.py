from Models.customer import Customer
from Models.animal import Animal
from Models.product import Product
from Models.supplier import Supplier
from Models.employee import Employee
from Models.position import Position
from Models.species import Species
from Models.category import Category
from Models.sale import Sale
from datetime import date
from database import initialize_db

def validate_input(prompt, input_type=str, allow_empty=False):
    while True:
        try:
            value = input(prompt).strip()
            if not value and not allow_empty:
                print("❌ Это поле не может быть пустым!")
                continue
            if input_type == int:
                return int(value)
            elif input_type == float:
                return float(value)
            return value
        except ValueError:
            print(f"❌ Неверный формат! Ожидается {input_type.__name__}")

def show_main_menu():
    while True:
        print("\n🐾 === Зоомагазин ===")
        print("1. 🛒 Продажи")
        print("2. 📦 Товары")
        print("3. 🐾 Животные")
        print("4. 👥 Клиенты")
        print("5. 📦 Поставщики")
        print("6. 👷 Сотрудники")
        print("7. 📊 Должности")
        print("8. 🐶 Виды животных")
        print("9. 📁 Категории товаров")
        print("0. 🛑 Выход")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            sale_menu()
        elif choice == "2":
            product_menu()
        elif choice == "3":
            animal_menu()
        elif choice == "4":
            customer_menu()
        elif choice == "5":
            supplier_menu()
        elif choice == "6":
            employee_menu()
        elif choice == "7":
            position_menu()
        elif choice == "8":
            species_menu()
        elif choice == "9":
            category_menu()
        elif choice == "0":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор")

def customer_menu():
    while True:
        print("\n👥 === Работа с клиентами ===")
        print("1. ➕ Добавить клиента")
        print("2. 📋 Просмотреть клиентов")
        print("0. ◀️ Назад")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            first_name = validate_input("Имя: ")
            last_name = validate_input("Фамилия: ")
            phone = validate_input("Телефон: ")
            email = validate_input("Email: ", allow_empty=True)
            discount = float(validate_input("Скидка (%): ", float, True) or 0)
            
            customer = Customer(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                discount=discount
            )
            customer.save()
            print("✅ Клиент добавлен!")
            
        elif choice == "2":
            customers = Customer.get_all()
            print("\nСписок клиентов:")
            for c in customers:
                print(f"{c.customer_id}. {c.first_name} {c.last_name} | Тел: {c.phone} | Скидка: {c.discount}%")
        elif choice == "0":
            break

def product_menu():
    while True:
        print("\n📦 === Работа с товарами ===")
        print("1. ➕ Добавить товар")
        print("2. 📋 Просмотреть товары")
        print("0. ◀️ Назад")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            name = validate_input("Название: ")
            category_id = validate_input("ID категории: ", int)
            price = validate_input("Цена: ", float)
            quantity = validate_input("Количество: ", int)
            exp_date = validate_input("Срок годности (ГГГГ-ММ-ДД): ")
            supplier_id = validate_input("ID поставщика: ", int)
            
            product = Product(
                name=name,
                price=price,
                quantity_in_stock=quantity,
                expiration_date=exp_date,
                supplier_id=supplier_id,
                category_id=category_id
            )
            product.save()
            print("✅ Товар сохранен!")
            
        elif choice == "2":
            products = Product.get_all()
            print("\nСписок товаров:")
            for p in products:
                print(f"{p.product_id}. {p.name} | {p.category_name} | {p.price} руб. | В наличии: {p.quantity_in_stock}")
        elif choice == "0":
            break

def animal_menu():
    while True:
        print("\n🐾 === Работа с животными ===")
        print("1. ➕ Добавить животное")
        print("2. 📋 Просмотреть животных")
        print("0. ◀️ Назад")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            date_of_birth = validate_input("Дата рождения (ГГГГ-ММ-ДД): ")
            gender = validate_input("Пол (м/ж): ")
            species_id = validate_input("ID вида: ", int)
            supplier_id = validate_input("ID поставщика: ", int)
            price = validate_input("Цена: ", float)
            
            animal = Animal(
                date_of_birth=date_of_birth,
                gender=gender,
                species_id=species_id,
                supplier_id=supplier_id,
                price=price
            )
            animal.save()
            print("✅ Животное добавлено!")
            
        elif choice == "2":
            animals = Animal.get_all()
            print("\nСписок животных:")
            for a in animals:
                print(f"{a.animal_id}. {a.species_name} | Дата рождения: {a.date_of_birth} | Пол: {a.gender} | Цена: {a.price} руб. | Статус: {a.status}")
        elif choice == "0":
            break

def supplier_menu():
    while True:
        print("\n📦 === Работа с поставщиками ===")
        print("1. ➕ Добавить поставщика")
        print("2. 📋 Просмотреть поставщиков")
        print("0. ◀️ Назад")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            name = validate_input("Название компании: ")
            contact = validate_input("Контактное лицо: ")
            phone = validate_input("Телефон: ")
            email = validate_input("Email: ", allow_empty=True)
            
            supplier = Supplier(
                name=name,
                contact_person=contact,
                phone=phone,
                email=email
            )
            supplier.save()
            print("✅ Поставщик добавлен!")
            
        elif choice == "2":
            suppliers = Supplier.get_all()
            print("\nСписок поставщиков:")
            for s in suppliers:
                print(f"{s.supplier_id}. {s.name} | {s.contact_person} | Тел: {s.phone}")
        elif choice == "0":
            break

def employee_menu():
    while True:
        print("\n👷 === Работа с сотрудниками ===")
        print("1. ➕ Добавить сотрудника")
        print("2. 📋 Просмотреть сотрудников")
        print("0. ◀️ Назад")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            last_name = validate_input("Фамилия: ")
            first_name = validate_input("Имя: ")
            hire_date = validate_input("Дата приема на работу (ГГГГ-ММ-ДД): ")
            phone = validate_input("Телефон: ")
            position_id = validate_input("ID должности: ", int)
            
            employee = Employee(
                last_name=last_name,
                first_name=first_name,
                hire_date=hire_date,
                phone=phone,
                position_id=position_id
            )
            employee.save()
            print("✅ Сотрудник добавлен!")
            
        elif choice == "2":
            employees = Employee.get_all()
            print("\nСписок сотрудников:")
            for e in employees:
                print(f"{e.employee_id}. {e.last_name} {e.first_name} | {e.position_title} | Тел: {e.phone}")
        elif choice == "0":
            break

def position_menu():
    while True:
        print("\n📊 === Работа с должностями ===")
        print("1. ➕ Добавить должность")
        print("2. 📋 Просмотреть должности")
        print("0. ◀️ Назад")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            title = validate_input("Название должности: ")
            salary = validate_input("Зарплата: ", float)
            description = validate_input("Описание: ", allow_empty=True)
            
            position = Position(
                title=title,
                salary=salary,
                description=description
            )
            position.save()
            print("✅ Должность добавлена!")
            
        elif choice == "2":
            positions = Position.get_all()
            print("\nСписок должностей:")
            for p in positions:
                print(f"{p.position_id}. {p.title} | Зарплата: {p.salary} руб. | {p.description}")
        elif choice == "0":
            break

def species_menu():
    while True:
        print("\n🐶 === Работа с видами животных ===")
        print("1. ➕ Добавить вид")
        print("2. 📋 Просмотреть виды")
        print("0. ◀️ Назад")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            name = validate_input("Название вида: ")
            description = validate_input("Описание: ", allow_empty=True)
            
            species = Species(
                name=name,
                description=description
            )
            species.save()
            print("✅ Вид животного добавлен!")
            
        elif choice == "2":
            species_list = Species.get_all()
            print("\nСписок видов:")
            for s in species_list:
                print(f"{s.species_id}. {s.name} | {s.description}")
        elif choice == "0":
            break

def category_menu():
    while True:
        print("\n📁 === Работа с категориями товаров ===")
        print("1. ➕ Добавить категорию")
        print("2. 📋 Просмотреть категории")
        print("0. ◀️ Назад")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            name = validate_input("Название категории: ")
            description = validate_input("Описание: ", allow_empty=True)
            
            category = Category(
                name=name,
                description=description
            )
            category.save()
            print("✅ Категория добавлена!")
            
        elif choice == "2":
            categories = Category.get_all()
            print("\nСписок категорий:")
            for c in categories:
                print(f"{c.category_id}. {c.name} | {c.description}")
        elif choice == "0":
            break

def sale_menu():
    while True:
        print("\n💳 === Продажи ===")
        print("1. 📦 Оформить продажу")
        print("2. 📋 Просмотреть продажи")
        print("0. ◀️ Назад")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            customers = Customer.get_all()
            print("\nВыберите клиента:")
            for c in customers:
                print(f"{c.customer_id}. {c.first_name} {c.last_name}")
            customer_id = validate_input("ID клиента: ", int)
            
            employees = Employee.get_all()
            print("\nВыберите сотрудника:")
            for e in employees:
                print(f"{e.employee_id}. {e.last_name} {e.first_name}")
            employee_id = validate_input("ID сотрудника: ", int)
            
            sale = Sale(
                sale_date=date.today().isoformat(),
                employee_id=employee_id,
                customer_id=customer_id,
                total_price=0
            )
            sale.save()
            
            while True:
                print("\n1. 🐾 Животное")
                print("2. 🍪 Товар")
                print("0. Завершить")
                item_choice = input("Выберите тип: ")
                
                if item_choice == "1":
                    animals = Animal.get_all()
                    print("\nДоступные животные:")
                    available_animals = [a for a in animals if a.status == 'в наличии']
                    for a in available_animals:
                        print(f"{a.animal_id}. {a.species_name} | Цена: {a.price} руб.")
                    animal_id = validate_input("ID животного: ", int)
                    sale.add_animal(animal_id)
                    
                elif item_choice == "2":
                    products = Product.get_all()
                    print("\nДоступные товары:")
                    available_products = [p for p in products if p.quantity_in_stock > 0]
                    for p in available_products:
                        print(f"{p.product_id}. {p.name} | Цена: {p.price} руб. | В наличии: {p.quantity_in_stock}")
                    product_id = validate_input("ID товара: ", int)
                    quantity = validate_input("Количество: ", int)
                    sale.add_product(product_id, quantity)
                    
                elif item_choice == "0":
                    break
            
            sale.apply_discount()
            sale.finalize()
            print(f"\n✅ Продажа оформлена! Итоговая цена: {sale.total_price:.2f} руб.")
            
        elif choice == "2":
            sales = Sale.get_all()
            print("\nИстория продаж:")
            for s in sales:
                customer = Customer.get_by_id(s.customer_id)
                employee = Employee.get_by_id(s.employee_id)
                print(f"{s.sale_id}. {s.sale_date} | "
                    f"Клиент: {customer.first_name} {customer.last_name if customer else 'Неизвестен'} | "
                    f"Сотрудник: {employee.last_name} {employee.first_name if employee else 'Неизвестен'} | "
                    f"Сумма: {s.total_price:.2f} руб.")      
        elif choice == "0":
            break

if __name__ == "__main__":
    initialize_db()
    show_main_menu()