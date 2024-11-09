import sqlite3


def initiate_product_db(db_path='Products_db.db'):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')
    connect.commit()
    connect.close()


def initiate_users_db(db_path='Users_db.db'):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
        )
    ''')
    connect.commit()
    connect.close()


# Доработал функцию add_product. Теперь она добавляет продукт в базу данных,
# только если запись с таким названием не существует.
def add_product(title, description, price, db_path='Products_db.db'):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Products WHERE title = ?", (title,))
    existing_product = cursor.fetchone()
    if existing_product:
        print(f'Продукт с названием {title} уже внесен в базу данных.')
    else:
        cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                       (title, description, price))
        connect.commit()
        print(f'Продукт {title} успешно внесен в базу данных.')
    connect.close()


# Также добавил функцию remove_product, которая позволяет удалять записи из таблицы Proucts по id,
# и дополнил её плейсхолдером, чтобы избежать многократного вызова функции, если возникнет необходимость удалить большое
# колличество записей
def remove_product(product_ids, db_path='Products_db.db'):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    placeholder = ','.join(['?'] * len(product_ids))
    cursor.execute(f"DELETE FROM Products WHERE id IN({placeholder})", product_ids)
    connect.commit()
    connect.close()


def get_all_products(db_path='Products_db.db'):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connect.close()
    return products


async def add_users(username, email, age, db_path='Users_db.db'):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (username, email, age, 1000))
    connect.commit()
    connect.close()

# Также добавил функцию для удаления записей из таблицы Users для удобства работы с тренировочной БД
def remove_users(users_ids, db_path='Users_db.db'):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    placeholder = ','.join(['?'] * len(users_ids))
    cursor.execute(f"DELETE FROM Users WHERE id IN({placeholder})", users_ids)
    connect.commit()
    connect.close()


def is_included(username, db_path='Users_db.db'):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    connect.close()
    return bool(existing_user)


initiate_product_db()
initiate_users_db()

#add_product(title='Аскорбиновая кислота', description='Классические аскорбинки, в формате желтых шариков', price=100)
#add_product(title='Компливит для детей', description='Мультивитаминный комплекс для детей в формате желейных конфет',
#            price=200)
#add_product(title='Herbal Vitamins',
#            description='Травяной витаминный комплекс в капсулах, на основе лекарственных растений', price=300)
#add_product(title='Рыбий жир', description='Очищеный рыбий жир в капсулах, источник омега-3', price=400)