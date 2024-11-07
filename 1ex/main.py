from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Підключення до MongoDB 
client = MongoClient(
    "mongodb+srv://denis23:2323@test23.4vwna.mongodb.net/?retryWrites=true&w=majority&appName=Test23",
    server_api=ServerApi('1')
)

# Вибір бази даних
db = client.DB_1ex


# Додаємо тестові дані
def test_data(args):
    db.Coll_1ex.insert_many(
        [
            {
                "name": "Кіт_1",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Кіт_2",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
            {
                "name": "Кіт_3",
                "age": 8,
                "features": ["ходить на голові", "сірий"],
            },
        ]
    )

# Функція для розбору вводу користувача
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# Пошук кота в базі даних за іменем
def find_in_db(args):
    try:
        name = args[0]
        result = db.Coll_1ex.find_one({"name": name})
        if result:
            return result
        else:
            return f"Немає кота на ім'я '{name}'."
    except Exception as e:
        return f"Виникла помилка: {e}"

# Відображення усіх записів
def show_all():
    try:
        result = db.Coll_1ex.find({})
        for el in result:
            print(el)
    except Exception as e:
        print(f"Виникла помилка: {e}")

# Оновлення віку кота за ім'ям
def update_age(args):
    try:
        name = args[0]
        new_age = int(args[1])
        db.Coll_1ex.update_one({"name": name}, {"$set": {"age": new_age}})
        result = db.Coll_1ex.find_one({"name": name})
        if result is None:
            return "Такого кота не знайдено"
        else:
            return result
    except ValueError:
        return "Вік має бути числом."
    except Exception as e:
        return f"Виникла помилка: {e}"

# Додавання нової характеристики коту
def add_featur(args):
    try:
        name = args[0]
        new_featur = ' '.join(args[1:])
        db.Coll_1ex.update_one({"name": name}, {"$push": {"features": new_featur}})
        result = db.Coll_1ex.find_one({"name": name})
        if result is None:
            return "Такого кота не знайдено"
        else:
            return result
    except Exception as e:
        return f"Виникла помилка: {e}"

# Видалення усіх записів
def delete_all():
    try:
        db.Coll_1ex.delete_many({})
        return "Усі коти видалені"
    except Exception as e:
        return f"Виникла помилка: {e}"

# Видалення одного запису за ім'ям
def delete_one(args):
    try:
        name = args[0]
        db.Coll_1ex.delete_one({"name": name})
        return f"Кота на ім'я '{name}' видалено."
    except Exception as e:
        return f"Виникла помилка: {e}"

# Головна функція 
def main():
    print("Welcome to DB")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        # Обробка команд
        if command in ["e", "close", "exit"]:
            print("Good bye!")
            break
        elif command == "test":
            test_data(args)
            print("Test data added")
        elif command == "all":
            show_all() 
        elif command == "find":
            print(find_in_db(args))
        elif command == "age":
            print(update_age(args))        
        elif command == "featur":
            print(add_featur(args))
        elif command == "delete":
            print(delete_one(args))    
        elif command == "clear":
            print(delete_all()) 
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
