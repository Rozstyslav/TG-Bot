from re import S, match, split
import telebot
from telebot.types import Message
from telebot import types
from collections import defaultdict
import time
import datetime
import requests
import sqlite3
import os



token = ''

bot = telebot.TeleBot(token)

Monday = ''
Tuesday = ''
Wednesday = ''
Thursday = ''
Friday = ''
Saturday = ''
Sunday = ''

gender = ''
clicked_option = ''
gender_chosen = False
gain_mass_clicked = False
lose_weight_clicked = False

user_button_presses = defaultdict(set)

import sqlite3

def table_Product():
    conn = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
                        Product_ID INTEGER PRIMARY KEY,
                        Product_Name TEXT,
                        Calories INTEGER,
                        Product_Type TEXT,
                        Time TEXT
                    )''')

    conn.commit()
    conn.close()


def addUser(nick, age, weight, height, gender):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (Nickname NVARCHAR(255) PRIMARY KEY AUTOINCREMENT NOT NULL, Age INTEGER, Weight INTEGER, Height INTEGER, Gender NVARCHAR(255) NOT NULL)")

        cursor.execute("INSERT INTO users (Nickname, Age, Weight, Height, Gender) VALUES (?, ?, ?, ?, ?)",
                       (nick, age, weight, height, gender))
        connection.commit()

        cursor.execute("SELECT last_insert_rowid()")
        return cursor.fetchone()[0]

    except sqlite3.Error as error:
        print("Error:", error)
        return None

    finally:
        connection.close()


def getTableExercisesName(id):
    connection = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Exercises_Name FROM Exercises WHERE Exercises_ID=?", (id,))
    rows = cursor.fetchall()

    exercise_names = [row[0] for row in rows]

    connection.close()

    return exercise_names[0] if exercise_names else None


def create_training_day_table():

    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TrainingDay (
            Id INTEGER PRIMARY KEY, 
            UserId NVARCHAR(255) , 
            Monday NVARCHAR(1024) ,
            Tuesday NVARCHAR(1024),
            Wednesday NVARCHAR(1024) ,
            Thursday NVARCHAR(1024) ,
            Friday NVARCHAR(1024) ,
            Saturday NVARCHAR(1024) ,
            Sunday NVARCHAR(1024)
        )
    ''')

    conn.commit()
    print("Training table is exist or created successfully.")
    conn.close()

def drop_training_day_table():
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS TrainingDay")
    conn.commit()
    print("Training table dropped successfully.")
    conn.close()


def view_training_day_table():
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TrainingDay")
    rows = cursor.fetchall()

    if rows:
        print("TrainingDay:")
        for row in rows:
            print(row)
    else:
        print("Тable is empyty.")

    conn.close()


def add_training_day(user_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO TrainingDay (UserId, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (user_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday))

    conn.commit()
    conn.close()


def add_training_day_monday(user_id, tasks):
    conn = sqlite3.connect('DataBase/User.db')


    cursor = conn.cursor()
    cursor.execute("INSERT INTO TrainingDay (Monday) VALUES (?) where UserId = ?",
                   (tasks,user_id,))

    conn.commit()
    conn.close()


def view_training_day_table_by_id(id):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TrainingDay where UserId = ?",(id,))
    rows = cursor.fetchall()

    if rows:
        print("TrainingDay:")
        for row in rows:
            print(row)
    else:
        print("Тable is empyty.")

    conn.close()


def add_training_day_F(message, day, tasks):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()

    user_id = message.from_user.id

    cursor.execute("SELECT UserId FROM TrainingDay WHERE UserId=?", (user_id,))
    existing_day = cursor.fetchone()

    if existing_day:
        cursor.execute("UPDATE TrainingDay SET {}=? WHERE UserId=?".format(day), (','.join(tasks), user_id,))
    else:
        cursor.execute("INSERT INTO TrainingDay (UserId, {}) VALUES (?, ?)".format(day), (user_id, ','.join(tasks),))

    conn.commit()
    conn.close()


def add_products_day_F(user_id, day, tasks):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()

    cursor.execute("SELECT UserId FROM ProductsInDay WHERE UserId=?", (user_id,))
    existing_day = cursor.fetchone()

    if existing_day:
        cursor.execute("UPDATE ProductsInDay SET {}=? WHERE UserId=?".format(day), (','.join(tasks), user_id,))
    else:
        cursor.execute("INSERT INTO ProductsInDay (UserId, {}) VALUES (?, ?)".format(day), (user_id, ','.join(tasks),))

    conn.commit()
    conn.close()

def getTableProductsName(id):
    connection = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Product_Name, Time FROM Product WHERE Product_ID=?", (id,))

    row = cursor.fetchone()

    product_info = f"{row[0]}, Тип: {row[1]}" if row else None

    connection.close()

    return product_info

def create_products_table():

    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProductsInDay (
            Id INTEGER PRIMARY KEY, 
            UserId NVARCHAR(255) , 
            MondayMorning NVARCHAR(1024) ,
            MondayDinner NVARCHAR(1024) ,
            MondayEvening NVARCHAR(1024) ,
            TuesdayMorning NVARCHAR(1024),
            TuesdayDinner NVARCHAR(1024),
            TuesdayEvening NVARCHAR(1024),
            WednesdayMorning NVARCHAR(1024) ,
            WednesdayDinner NVARCHAR(1024) ,
            Wednesdayvening NVARCHAR(1024) ,
            ThursdayMorning NVARCHAR(1024) ,
            ThursdayDinner NVARCHAR(1024) ,
            Thursdayvening NVARCHAR(1024) ,                     
            FridayMorning NVARCHAR(1024) ,
            FridayDinner NVARCHAR(1024) ,
            Fridayvening NVARCHAR(1024) ,
            SaturdayMorning NVARCHAR(1024) ,
            SaturdayDinner NVARCHAR(1024) ,
            Saturdayvening NVARCHAR(1024) ,
            SundayMorning NVARCHAR(1024),
            SundayDinner NVARCHAR(1024),
            Sundayvening NVARCHAR(1024)
        )
    ''')

    conn.commit()
    print("Training table is exist or created successfully.")
    conn.close()

def drop_products_table():
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS ProductsInDay")
    conn.commit()
    print("Training table dropped successfully.")
    conn.close()

def FindUserDataBase(name):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Nickname FROM users WHERE Nickname = ?", (name,))
    result = cursor.fetchall()
    print(result)

    connection.close()
    connection.commit()
    print("Training table is exist or created successfully.")
    connection.close()

def deleteUsersTable():
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    connection.commit()
    connection.close()
    print("Table 'users' deleted successfully.")


def deleteUserDatabase():
    db_path = 'DataBase/User.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Database deleted successfully.")
    else:
        print("Database does not exist.")


def is_user_registered(username):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users (Nickname NVARCHAR(255) PRIMARY KEY NOT NULL, Age INTEGER, Weight INTEGER, Height INTEGER, Gender NVARCHAR(255) NOT NULL)''')
    connection.commit()
    cursor.execute("SELECT * FROM users WHERE Nickname = ?", (username,))
    result = cursor.fetchone()
    connection.close()
    return result is not None


def editUserHeight(userId, height):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET Height = ? WHERE  Nickname = ?", (height, userId))
    connection.commit()

    connection.close()


def editUserWeight(userId, weight):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET Weight = ? WHERE  Nickname = ?", (weight, userId))
    connection.commit()

    connection.close()


def editUserAge(userId, age):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET Age = ? WHERE  Nickname = ?", (age, userId))
    connection.commit()

    connection.close()


def getGender(userId):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()
    cursor.execute("SELECT Gender FROM users WHERE Nickname = ?", (userId,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

    connection.close()

def getHeight(userId):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Height FROM users where Nickname = ?", (userId,))
    result = cursor.fetchone()
    if result:
        height = result[0]
        return height

    connection.close()


def getWeight(userId):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Weight FROM users where Nickname = ?", (userId,))
    result = cursor.fetchone()
    if result:
        weight = result[0]
        return weight

    connection.close()


def getAge(userId):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Age FROM users where Nickname = ?", (userId,))
    result = cursor.fetchone()
    if result:
        age = result[0]
        return age

    connection.close()


def CreateTrainingTable():
    try:
        connection = sqlite3.connect('DataBase/User.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Training (
                Id INTEGER PRIMARY KEY,
                UserId TEXT NOT NULL,
                TrainingName TEXT NOT NULL,
                TrainingDate TEXT NOT NULL
            )
        ''')
        connection.commit()
        print("Training table is exist or created successfully.")
    except sqlite3.Error as e:
        print("Error creating table:", e)
    finally:
        if connection:
            connection.close()


def getTrainingData(user_id):
    try:
        conn = sqlite3.connect('DataBase/User.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Training WHERE UserId=?", (user_id,))
        training_data = cursor.fetchall()
        return training_data
    except sqlite3.Error as e:
        print("Error getting training data:", e)
    finally:
        if conn:
            conn.close()


def insertTrainingData(training_name, training_date, user_id):
    try:
        conn = sqlite3.connect('DataBase/User.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Training (TrainingName, TrainingDate, UserId) VALUES (?, ?, ?)",
                       (training_name, training_date, user_id))
        conn.commit()
        print("Training data inserted successfully.")
    except sqlite3.Error as e:
        print("Error inserting training data:", e)
    finally:
        if conn:
            conn.close()

def deleteTrainingData(training_date, user_id):
    try:
        conn = sqlite3.connect('DataBase/User.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Training WHERE TrainingDate = ? AND UserId = ?", (training_date, user_id))
        conn.commit()
        print("Training data deleted successfully.")
    except sqlite3.Error as e:
        print("Error deleting training data:", e)
    finally:
        if conn:
            conn.close()


def updateTrainingData(training_name, new_training_date, user_id):
    try:
        connection = sqlite3.connect('DataBase/User.db')
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE Training
            SET TrainingDate = ?
            WHERE UserId = ? AND TrainingName = ?
        ''', (new_training_date, user_id, training_name))
        connection.commit()
        print("Training data updated successfully.")
    except sqlite3.Error as e:
        print("Error updating training data:", e)
    finally:
        if connection:
            connection.close()

def insertTrainingData(training_name, training_date, user_id):
    try:
        connection = sqlite3.connect('DataBase/User.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO Training (UserId, TrainingName, TrainingDate)
            VALUES (?, ?, ?)
        ''', (user_id, training_name, training_date))
        connection.commit()
        print("Training data inserted successfully.")
    except sqlite3.Error as e:
        print("Error inserting training data:", e)
    finally:
        if connection:
            connection.close()


def create_training_day_table():
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TrainingDay (
            Id INTEGER PRIMARY KEY, 
            UserId NVARCHAR(255) NOT NULL, 
            Monday NVARCHAR(1024) NOT NULL,
            Tuesday NVARCHAR(1024) NOT NULL,
            Wednesday NVARCHAR(1024) NOT NULL,
            Thursday NVARCHAR(1024) NOT NULL,
            Friday NVARCHAR(1024) NOT NULL,
            Saturday NVARCHAR(1024) NOT NULL,
            Sunday NVARCHAR(1024) NOT NULL
        )
    ''')

    conn.commit()
    print("Training table is exist or created successfully.")
    conn.close()


def get_exercise_for_day(user_id, day):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT {} FROM TrainingDay WHERE UserId = ?'''.format(day), (user_id,))

    exercise = cursor.fetchone()

    conn.close()

    if exercise is None:
        return "Відсутня інформація"
    else:
        return exercise[0]

def get_product_for_day(user_id, day):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT {} FROM ProductsInDay WHERE UserId = ?'''.format(day), (user_id,))

    exercise = cursor.fetchone()

    conn.close()

    if exercise is None:
        return "Відсутня інформація"
    else:
        return exercise[0]

def create_products_table():
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProductsInDay (
            Id INTEGER PRIMARY KEY, 
            UserId NVARCHAR(255) , 
            MondayMorning NVARCHAR(1024) ,
            MondayDinner NVARCHAR(1024) ,
            MondayEvening NVARCHAR(1024) ,
            TuesdayMorning NVARCHAR(1024),
            TuesdayDinner NVARCHAR(1024),
            TuesdayEvening NVARCHAR(1024),
            WednesdayMorning NVARCHAR(1024) ,
            WednesdayDinner NVARCHAR(1024) ,
            WednesdayEvening NVARCHAR(1024) ,
            ThursdayMorning NVARCHAR(1024) ,
            ThursdayDinner NVARCHAR(1024) ,
            ThursdayEvening NVARCHAR(1024) ,                     
            FridayMorning NVARCHAR(1024) ,
            FridayDinner NVARCHAR(1024) ,
            FridayEvening NVARCHAR(1024) ,
            SaturdayMorning NVARCHAR(1024) ,
            SaturdayDinner NVARCHAR(1024) ,
            SaturdayEvening NVARCHAR(1024) ,
            SundayMorning NVARCHAR(1024),
            SundayDinner NVARCHAR(1024),
            SundayEvening NVARCHAR(1024)
        )
    ''')
    conn.commit()
    conn.close()

# deleteUsersTable()

@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.from_user.username, ": ", message.from_user.id)

    if is_user_registered(message.from_user.id) == False:
        first_name = message.from_user.first_name
        user_id = message.from_user.id

        markup = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton("Зареєструватися", callback_data="reg")
        markup.add(but1)

        bot.send_message(message.chat.id,
                         rf"Вітаю, {message.from_user.first_name}! Спробуймо правильно харчуватись і дивитись за калоріями!",
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Ви вже зареєстровані")
        menu_message(message)


@bot.callback_query_handler(func=lambda call: call.data == 'reg' and not gender_chosen)
def choose_gender(call):
    global gender_chosen
    gender_chosen = True
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    items_1 = telebot.types.InlineKeyboardButton(text='Чоловік', callback_data='choose_gender:Чоловік')
    items_2 = telebot.types.InlineKeyboardButton(text='Жінка', callback_data='choose_gender:Жінка')
    markup.add(items_1, items_2)

    bot.send_message(call.message.chat.id, "Оберіть свою стать", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('choose_gender:') and not gender)
def handle_gender_choice(call):
    global gender, gender_chosen
    gender_chosen = True
    gender = call.data.split(':')[1]
    bot.answer_callback_query(call.id, text="Стать вибрано!")
    enter_age(call.message, gender)


def enter_age(message, gender):
    bot.send_message(message.chat.id, "Введіть свій вік:")
    bot.register_next_step_handler(message, enter_weight, gender)


def enter_weight(message, gender):
    try:
        age = int(message.text)
        if 14 <= age <= 60:
            bot.send_message(message.chat.id, "Введіть свою вагу:")
            bot.register_next_step_handler(message, enter_height, age, gender)
        else:
            bot.send_message(message.chat.id, "Введіть коректний вік!")
            bot.register_next_step_handler(message, enter_weight, gender)
    except ValueError:
        bot.send_message(message.chat.id, "Введіть коректне число для віку!")
        enter_weight(message, gender)


def enter_height(message, age, gender):
    try:
        weight = float(message.text)
        if 30 <= weight <= 150:
            bot.send_message(message.chat.id, "Введіть свій зріст:")
            bot.register_next_step_handler(message, show_result, age, weight, gender)
        else:
            bot.send_message(message.chat.id, "Введіть коректну вагу!")
            bot.register_next_step_handler(message, enter_height, age, gender)
    except ValueError:
        bot.send_message(message.chat.id, "Введіть коректне число для ваги!")
        bot.register_next_step_handler(message, enter_height, age, gender)


def show_result(message, age, weight, gender):
    global current_message
    current_message = message
    try:
        nick = message.from_user.id
        height = float(message.text)
        first_name = message.from_user.first_name

        if not (130 <= height <= 220):
            raise ValueError("Введіть коректний зріст!")

        bmi = weight / ((height / 100) * (height / 100))

        bot.send_message(message.chat.id,
                         f"Інформація про вас: \nІм'я: {first_name}\nВік: {age}\nВага: {weight}\nЗріст: {height}\nCтать: {gender}")
        bot.send_message(message.chat.id, f"Ваш індекс маси тіла (ІМТ): {bmi:.1f}")
        get_imt(height, weight, message, bmi)

        addUser(nick, age, weight, height, gender)

    except ValueError as e:
        bot.send_message(message.chat.id, str(e))
        bot.register_next_step_handler(message, show_result, age, weight, gender)


def get_imt(height, weight, message, imt):
    try:
        chat_id = message.chat.id

        if imt < 18.5:
            photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%9D%D0%B5%D0%B4%D0%BE%D1%81%D1%82%D0%B0%D1%82%D0%BD%D1%8F%20%D0%B2%D0%B0%D0%B3%D0%B0.jpg?raw=true"
        elif 18.5 <= imt <= 24.9:
            photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%9D%D0%BE%D1%80%D0%BC%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%20%D0%B2%D0%B0%D0%B3%D0%B0.jpg?raw=true"
        elif 25 <= imt <= 29.9:
            photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%9D%D0%B0%D0%B4%D0%BC%D1%96%D1%80%D0%BD%D0%B0%20%D0%B2%D0%B0%D0%B3%D0%B0.jpg?raw=true"
        elif 30 <= imt <= 39.9:
            photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%9E%D0%B6%D0%B8%D1%80%D1%96%D0%BD%D0%BD%D1%8F.jpg?raw=true"
        elif imt >= 40:
            photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%92%D0%B5%D0%BB%D0%B8%D0%BA%D0%B5%20%D0%BE%D0%B6%D0%B8%D1%80%D1%96%D0%BD%D0%BD%D1%8F.jpg?raw=true"

        response = requests.get(photo_url)
        if response.status_code == 200:
            bot.send_photo(chat_id, photo=response.content)
        else:
            bot.send_message(chat_id, "Failed to fetch image from GitHub")

    except ZeroDivisionError as e:
        bot.send_message(message.chat.id, str(e))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")
    get_recomendations(imt, message)


def get_recomendations(imt, message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    items_1 = telebot.types.InlineKeyboardButton(text='Набір маси', callback_data='Набір маси')
    items_2 = telebot.types.InlineKeyboardButton(text='Схуднення', callback_data='Схуднення')
    markup.add(items_1, items_2)

    bot.send_message(message.chat.id, "Оберіть свою мету:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'Набір маси' and not lose_weight_clicked)
def handle_gain_mass(call):
    global gender, clicked_option, gain_mass_clicked
    gain_mass_clicked = True
    chat_id = call.message.chat.id
    clicked_option = 'Набір маси'
    send_photos(chat_id, gender)
    menu_message(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'Схуднення' and not gain_mass_clicked)
def handle_lose_weight(call):
    global gender, clicked_option, lose_weight_clicked
    lose_weight_clicked = True
    chat_id = call.message.chat.id
    clicked_option = 'Схуднення'
    send_photos(chat_id, gender)
    menu_message(call.message)

def send_photos(chat_id, gender):
    if gender == 'Чоловік':
        if clicked_option == 'Набір маси':
            photo_url_1 = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%9D%D0%B0%D0%B1%D1%96%D1%80%20%D0%BC%D0%B0%D1%81%D0%B8%20(%D1%87%D0%BE%D0%BB).jpg?raw=true"
            photo_url_2 = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%A0%D0%B0%D1%86%D1%96%D0%BE%D0%BD%20%D0%B4%D0%BB%D1%8F%20%D0%BD%D0%B0%D0%B1%D0%BE%D1%80%D1%83%20%D0%BC%D0%B0%D1%81%D0%B8.jpg?raw=true"
        elif clicked_option == 'Схуднення':
            photo_url_1 = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%94%D0%BB%D1%8F%20%D1%81%D1%85%D1%83%D0%B4%D0%BD%D0%B5%D0%BD%D0%BD%D1%8F%20(%D1%87%D0%BE%D0%BB).jpg?raw=true"
            photo_url_2 = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%A0%D0%B0%D1%86%D1%96%D0%BE%D0%BD%20%D0%B4%D0%BB%D1%8F%20%D1%81%D1%85%D1%83%D0%B4%D0%BD%D0%B5%D0%BD%D0%BD%D1%8F.jpg?raw=true"
    elif gender == 'Жінка':
        if clicked_option == 'Набір маси':
            photo_url_1 = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%9D%D0%B0%D0%B1%D1%96%D1%80%20%D0%BC%D0%B0%D1%81%D0%B8%20(%D0%B6%D1%96%D0%BD).jpg?raw=true"
            photo_url_2 = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%A0%D0%B0%D1%86%D1%96%D0%BE%D0%BD%20%D0%B4%D0%BB%D1%8F%20%D0%BD%D0%B0%D0%B1%D0%BE%D1%80%D1%83%20%D0%BC%D0%B0%D1%81%D0%B8.jpg?raw=true"
        elif clicked_option == 'Схуднення':
            photo_url_1 = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%94%D0%BB%D1%8F%20%D1%81%D1%85%D1%83%D0%B4%D0%BD%D0%B5%D0%BD%D0%BD%D1%8F%20(%D0%B6%D1%96%D0%BD).jpg?raw=true"
            photo_url_2 = "https://github.com/MaxymSmal37/OBD_Telegram_bot/blob/main/img/%D0%A0%D0%B0%D1%86%D1%96%D0%BE%D0%BD%20%D0%B4%D0%BB%D1%8F%20%D1%81%D1%85%D1%83%D0%B4%D0%BD%D0%B5%D0%BD%D0%BD%D1%8F.jpg?raw=true"

    response_1 = requests.get(photo_url_1)
    response_2 = requests.get(photo_url_2)

    if response_1.status_code == 200 and response_2.status_code == 200:
        photo1_data = response_1.content
        photo2_data = response_2.content

        bot.send_media_group(chat_id, [
            telebot.types.InputMediaPhoto(photo1_data),
            telebot.types.InputMediaPhoto(photo2_data)
        ])
    else:
        print("Failed to fetch one or both photos from GitHub.")

@bot.message_handler(commands=['menu'])
def menu_message(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    but_1 = telebot.types.InlineKeyboardButton(text='Iндекс маси тіла', callback_data='індексМасиТіла')
    but_2 = telebot.types.InlineKeyboardButton(text='Редагувати список вправ', callback_data='РедагуватиСписокВправ')
    but_3 = telebot.types.InlineKeyboardButton(text='Редагувати список харчування', callback_data='РедагуватиСписокХарчування')
    but_4 = telebot.types.InlineKeyboardButton(text='Переглянути свої вправи', callback_data='ПереглянутиВправи')
    but_5 = telebot.types.InlineKeyboardButton(text='Переглянути свій раціон', callback_data='ПереглянутиРаціон')
    but_6 = telebot.types.InlineKeyboardButton(text='✏️ Редагувати параметри тіла', callback_data='РедагуватиПараметриТіла')

    markup.add(but_1, but_2, but_3, but_4, but_5,but_6)

    bot.send_message(message.chat.id, "Меню", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'ПереглянутиВправи')
def process_view_training(call):
    translate_days = {
        'Monday': 'Понеділок',
        'Tuesday': 'Вівторок',
        'Wednesday': 'Середа',
        'Thursday': 'Четвер',
        'Friday': 'П\'ятниця',
        'Saturday': 'Субота',
        'Sunday': 'Неділя'
    }

    chat_id = call.message.chat.id

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days_of_week:
        exercise_info = get_exercise_for_day(chat_id, day)

        translated_day = translate_days.get(day, day)

        res = f"{translated_day}: {'Відсутня інформація про вправи на цей день' if exercise_info is None else exercise_info}"
        bot.send_message(chat_id, res)

    menu_message(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'ПереглянутиРаціон')
def process_view_product(call):
    translate_days = {
        'MondayMorning': 'Понеділок - ранок',
        'MondayDinner': 'Понеділок - обід',
        'MondayEvening': 'Понеділок - вечір',
        'TuesdayMorning': 'Вівторок - ранок',
        'TuesdayDinner': 'Вівторок - обід',
        'TuesdayEvening': 'Вівторок - вечір',
        'WednesdayMorning': 'Середа - ранок',
        'WednesdayDinner': 'Середа - обід',
        'WednesdayEvening': 'Середа - вечір',
        'ThursdayMorning': 'Четвер - ранок',
        'ThursdayDinner': 'Четвер - обід',
        'ThursdayEvening': 'Четвер - вечір',
        'FridayMorning': 'П\'ятниця - ранок',
        'FridayDinner': 'П\'ятниця - обід',
        'FridayEvening': 'П\'ятниця - вечір',
        'SaturdayMorning': 'Субота - ранок',
        'SaturdayDinner': 'Субота - обід',
        'SaturdayEvening': 'Субота - вечір',
        'SundayMorning': 'Неділя - ранок',
        'SundayDinner': 'Неділя - обід',
        'SundayEvening': 'Неділя - вечір'
    }

    chat_id = call.message.chat.id

    days_of_week = ['MondayMorning', 'MondayDinner', 'MondayEvening', 'TuesdayMorning', 'TuesdayDinner',
                    'TuesdayEvening', 'WednesdayMorning', 'WednesdayDinner', 'WednesdayEvening', 'ThursdayMorning',
                    'ThursdayDinner', 'ThursdayEvening', 'FridayMorning', 'FridayDinner', 'FridayEvening',
                    'SaturdayMorning', 'SaturdayDinner', 'SaturdayEvening', 'SundayMorning', 'SundayDinner',
                    'SundayEvening']
    for day in days_of_week:
        exercise_info = get_product_for_day(chat_id, day)

        translated_day = translate_days.get(day, day)

        res = f"{translated_day}: {'Відсутня інформація' if exercise_info is None else exercise_info}"
        bot.send_message(chat_id, res)

    menu_message(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'індексМасиТіла')
def index_mas_tila(call):
    chat_id = call.message.chat.id

    weight = getWeight(call.from_user.id)
    height = getHeight(call.from_user.id)

    imt = weight / ((height / 100) * (height / 100))
    if imt < 18.5:
        photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Недостатня%20вага.jpg"
    elif 18.5 <= imt <= 24.9:
        photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Нормальна%20вага.jpg"
    elif 25 <= imt <= 29.9:
        photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Надмірна%20вага.jpg"
    elif 30 <= imt <= 39.9:
        photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Ожиріння.jpg"
    elif imt >= 40:
        photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Велике%20ожиріння.jpg"

    response = requests.get(photo_url)
    if response.status_code == 200:
        bot.send_photo(chat_id, photo=response.content)
        menu_message(call.message)
    else:
        bot.send_message(chat_id, "Не вдалося завантажити зображення з GitHub")


@bot.callback_query_handler(func=lambda call: call.data == 'РедагуватиПараметриТіла')
def edit(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    but_1 = telebot.types.InlineKeyboardButton(text='Зріст', callback_data='Зріст')
    but_2 = telebot.types.InlineKeyboardButton(text='Вага', callback_data='Вага')
    but_3 = telebot.types.InlineKeyboardButton(text='Вік', callback_data='Вік')

    markup.add(but_1, but_2, but_3)

    bot.send_message(call.message.chat.id, "Редагування", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'РедагуватиСписокВправ')
def recomendations(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    but_1 = telebot.types.InlineKeyboardButton(text='Понеділок', callback_data='Monday')
    but_2 = telebot.types.InlineKeyboardButton(text='Вівторок', callback_data='Tuesday')
    but_3 = telebot.types.InlineKeyboardButton(text='Середа', callback_data='Wednesday')
    but_4 = telebot.types.InlineKeyboardButton(text='Четвер', callback_data='Thursday')
    but_5 = telebot.types.InlineKeyboardButton(text='Пятниця', callback_data='Friday')
    but_6 = telebot.types.InlineKeyboardButton(text='Субота', callback_data='Saturday')
    but_7 = telebot.types.InlineKeyboardButton(text='Неділя', callback_data='Sunday')
    but_8 = telebot.types.InlineKeyboardButton(text='Повернутись до меню', callback_data='Меню')
    markup.add(but_1, but_2, but_3, but_4, but_5, but_6, but_7, but_8)

    bot.send_message(call.message.chat.id, "Оберіть день для редагування вправ:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
def select_day(call):
    day = call.data
    chat_id = call.message.chat.id
    exercise_info = ""
    for i in range(1, 63):
        exercise_name = getTableExercisesName(i)

        if exercise_name:
            exercise_info += f'{i}: {exercise_name}\n'
        else:
            exercise_info += f'No exercise found for ID {i}\n'

    bot.send_message(chat_id, exercise_info)
    bot.send_message(chat_id, f"Оберіть вправи які вам довподоби для {day}\nНаприклад: 1,54,43 ...")
    bot.register_next_step_handler(call.message, handle_exercise_selection, day)

def handle_exercise_selection(message, day, exercises=[]):
    if message.text == 'end':
        add_training_day_F(message, day, exercises)
        exercises.clear()
        menu_message(message)
        return
    if 1 <= message.text.isdigit() <= 63 :
        exercise_number = int(message.text)
        exercise_name = getTableExercisesName(exercise_number)
        if exercise_name:
            exercises.append(exercise_name)
            bot.send_message(message.chat.id, f"Added exercise '{exercise_name}'. \tEnter another exercise number, or type 'end' to finish.")
        else:
            bot.send_message(message.chat.id, "Exercise not found. Please enter a valid exercise number.")
    else:
        bot.send_message(message.chat.id, "Please enter a valid exercise number.")
    bot.register_next_step_handler(message, handle_exercise_selection, day, exercises)


@bot.callback_query_handler(func=lambda call: call.data == 'РедагуватиСписокХарчування')
def products(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    but_1 = telebot.types.InlineKeyboardButton(text='Понеділок', callback_data='Mondays')
    but_2 = telebot.types.InlineKeyboardButton(text='Вівторок', callback_data='Tuesdays')
    but_3 = telebot.types.InlineKeyboardButton(text='Середа', callback_data='Wednesdays')
    but_4 = telebot.types.InlineKeyboardButton(text='Четвер', callback_data='Thursdays')
    but_5 = telebot.types.InlineKeyboardButton(text='Пятниця', callback_data='Fridays')
    but_6 = telebot.types.InlineKeyboardButton(text='Субота', callback_data='Saturdays')
    but_7 = telebot.types.InlineKeyboardButton(text='Неділя', callback_data='Sundays')
    but_8 = telebot.types.InlineKeyboardButton(text='Повернутись до меню', callback_data='Меню')
    markup.add(but_1, but_2, but_3, but_4, but_5, but_6, but_7, but_8)

    bot.send_message(call.message.chat.id, "Оберіть день для редагування страв:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'Mondays')
def mon_time(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    but_1 = telebot.types.InlineKeyboardButton(text='Сніданок', callback_data='MondayMorning')
    but_2 = telebot.types.InlineKeyboardButton(text='Обід', callback_data='MondayDinner')
    but_3 = telebot.types.InlineKeyboardButton(text='Вечеря', callback_data='MondayEvening')
    markup.add(but_1, but_2, but_3)

    bot.send_message(call.message.chat.id, "Оберіть частину раціону для редагування страв:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['MondayMorning', 'MondayDinner', 'MondayEvening'])
def mon_sov(call):
    days = call.data
    select_product(call)
    handle_product_selection(call.message, days, products=[])

@bot.callback_query_handler(func=lambda call: call.data == 'Tuesdays')
def tue_time(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    but_1 = telebot.types.InlineKeyboardButton(text='Сніданок', callback_data='TuesdayMorning')
    but_2 = telebot.types.InlineKeyboardButton(text='Обід', callback_data='TuesdayDinner')
    but_3 = telebot.types.InlineKeyboardButton(text='Вечеря', callback_data='TuesdayEvening')
    markup.add(but_1, but_2, but_3)

    bot.send_message(call.message.chat.id, "Оберіть частину раціону для редагування страв:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['TuesdayMorning', 'TuesdayDinner', 'TuesdayEvening'])
def tue_sov(call):
    days = call.data
    select_product(call)
    handle_product_selection(call.message, days, products=[])


@bot.callback_query_handler(func=lambda call: call.data == 'Wednesdays')
def wed_time(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    but_1 = telebot.types.InlineKeyboardButton(text='Сніданок', callback_data='WednesdayMorning')
    but_2 = telebot.types.InlineKeyboardButton(text='Обід', callback_data='WednesdayDinner')
    but_3 = telebot.types.InlineKeyboardButton(text='Вечеря', callback_data='Wednesdayvening')
    markup.add(but_1, but_2, but_3)

    bot.send_message(call.message.chat.id, "Оберіть частину раціону для редагування страв:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['WednesdayMorning', 'WednesdayDinner', 'Wednesdayvening'])
def wed_sov(call):
    days = call.data
    select_product(call)
    handle_product_selection(call.message, days, products=[])


@bot.callback_query_handler(func=lambda call: call.data == 'Thursdays')
def thu_time(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    but_1 = telebot.types.InlineKeyboardButton(text='Сніданок', callback_data='ThursdayMorning')
    but_2 = telebot.types.InlineKeyboardButton(text='Обід', callback_data='ThursdayDinner')
    but_3 = telebot.types.InlineKeyboardButton(text='Вечеря', callback_data='Thursdayvening')
    markup.add(but_1, but_2, but_3)

    bot.send_message(call.message.chat.id, "Оберіть частину раціону для редагування страв:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['ThursdayMorning', 'ThursdayDinner', 'Thursdayvening'])
def thu_sov(call):
    days = call.data
    select_product(call)
    handle_product_selection(call.message, days, products=[])


@bot.callback_query_handler(func=lambda call: call.data == 'Fridays')
def fri_time(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    but_1 = telebot.types.InlineKeyboardButton(text='Сніданок', callback_data='FridayMorning')
    but_2 = telebot.types.InlineKeyboardButton(text='Обід', callback_data='FridayDinner')
    but_3 = telebot.types.InlineKeyboardButton(text='Вечеря', callback_data='Fridayvening')
    markup.add(but_1, but_2, but_3)

    bot.send_message(call.message.chat.id, "Оберіть частину раціону для редагування страв:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['FridayMorning', 'FridayDinner', 'Fridayvening'])
def fri_sov(call):
    days = call.data
    select_product(call)
    handle_product_selection(call.message, days, products=[])


@bot.callback_query_handler(func=lambda call: call.data == 'Saturdays')
def sat_time(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    but_1 = telebot.types.InlineKeyboardButton(text='Сніданок', callback_data='SaturdayMorning')
    but_2 = telebot.types.InlineKeyboardButton(text='Обід', callback_data='SaturdayDinner')
    but_3 = telebot.types.InlineKeyboardButton(text='Вечеря', callback_data='Saturdayvening')
    markup.add(but_1, but_2, but_3)

    bot.send_message(call.message.chat.id, "Оберіть частину раціону для редагування страв:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['SaturdayMorning', 'SaturdayDinner', 'Saturdayvening'])
def sat_sov(call):
    days = call.data
    select_product(call)
    handle_product_selection(call.message, days, products=[])


@bot.callback_query_handler(func=lambda call: call.data == 'Sundays')
def sun_time(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    but_1 = telebot.types.InlineKeyboardButton(text='Сніданок', callback_data='SundayMorning')
    but_2 = telebot.types.InlineKeyboardButton(text='Обід', callback_data='SundayDinner')
    but_3 = telebot.types.InlineKeyboardButton(text='Вечеря', callback_data='Sundayvening')
    markup.add(but_1, but_2, but_3)

    bot.send_message(call.message.chat.id, "Оберіть частину раціону для редагування страв:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['SundayMorning', 'SundayDinner', 'Sundayvening'])
def sun_sov(call):
    days = call.data
    select_product(call)
    handle_product_selection(call.message, days, products=[])


def select_product(call):
    days = call.data
    chat_id = call.message.chat.id
    product_info = ""
    for i in range(1, 81):
        product_name = getTableProductsName(i)

        if product_name:
            product_info += f'{i}: {product_name}\n'
        else:
            product_info += f'No food found for ID {i}\n'

    bot.send_message(chat_id, product_info)
    bot.send_message(chat_id, f"Оберіть страви які вам довподоби для {days}\nНаприклад: 1,54,43 ...")


def handle_product_selection(message, days, products=[]):
    if message.text == 'end':
        user_id = message.from_user.id
        add_products_day_F(user_id, days, products)
        products.clear()
        menu_message(message)
        return
    if 1 <= message.text.isdigit() <= 80:
        product_number = int(message.text)
        product_name = getTableProductsName(product_number)
        if product_name:
            products.append(product_name)
            bot.send_message(message.chat.id, f"Added product '{product_name}'. \tEnter another product number, or type 'end' to finish.")
        else:
            bot.send_message(message.chat.id, "Product not found. Please enter a valid product number.")
    else:
        bot.send_message(message.chat.id, "Please enter a valid product number.")
    bot.register_next_step_handler(message, handle_product_selection, days, products)


# @bot.callback_query_handler(func=lambda call: call.data == 'Меню')
# def go_back_ti_menu(call):
#     send_main_menu(call.message)

# !!!!!!!!!
@bot.callback_query_handler(func=lambda call: call.data == 'Зріст')
def editHeight(call):
    bot.send_message(call.message.chat.id, "Введіть свій новий зріст")
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    bot.register_next_step_handler(call.message, process_new_height)


def process_new_height(message):
    try:
        new_height = int(message.text)
        if 130 <= new_height <= 220:
            editUserHeight(message.from_user.id, new_height)
            bot.send_message(message.chat.id, f"Зріст успішно змінено на: {new_height}см.")

            weight = getWeight(message.from_user.id)
            height = getHeight(message.from_user.id)
            imt = weight / ((height / 100) * (height / 100))

            if imt < 18.5:
                photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Недостатня%20вага.jpg"
            elif 18.5 <= imt <= 24.9:
                photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Нормальна%20вага.jpg"
            elif 25 <= imt <= 29.9:
                photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Надмірна%20вага.jpg"
            elif 30 <= imt <= 39.9:
                photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Ожиріння.jpg"
            elif imt >= 40:
                photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Велике%20ожиріння.jpg"

            bot.send_message(message.chat.id, f"Ваш індекс маси тіла (ІМТ): {imt:.1f}")

            response = requests.get(photo_url)
            if response.status_code == 200:
                bot.send_photo(message.chat.id, photo=response.content)
            else:
                bot.send_message(message.chat.id, "Failed to load image from GitHub")

            menu_message(message)

        else:
            bot.send_message(message.chat.id, "Введіть зріст від 130 до 220")
            bot.register_next_step_handler(message, process_new_height)


    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть числове значення для зросту.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Виникла помилка: {str(e)}")


@bot.callback_query_handler(func=lambda call: call.data == 'Вага')
def editWeight(call):
    bot.send_message(call.message.chat.id, "Введіть свій нову вагу")
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    bot.register_next_step_handler(call.message, process_new_weight)


def process_new_weight(message):
    try:
        new_weight = int(message.text)
        if 30 <= new_weight <= 150:
            editUserWeight(message.from_user.id, new_weight)
            bot.send_message(message.chat.id, f"Вагу успішно змінено на: {new_weight} кг.")

            weight = getWeight(message.from_user.id)
            height = getHeight(message.from_user.id)
            imt = weight / ((height / 100) * (height / 100))

            if imt < 18.5:
                photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Недостатня%20вага.jpg"
            elif 18.5 <= imt <= 24.9:
                photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Нормальна%20вага.jpg"
            elif 25 <= imt <= 29.9:
                photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Надмірна%20вага.jpg"
            elif 30 <= imt <= 39.9:
                photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Ожиріння.jpg"
            elif imt >= 40:
                photo_url = "https://github.com/MaxymSmal37/OBD_Telegram_bot/raw/main/img/Велике%20ожиріння.jpg"

            bot.send_message(message.chat.id, f"Ваш індекс маси тіла (ІМТ): {imt:.1f}")

            response = requests.get(photo_url)
            if response.status_code == 200:
                bot.send_photo(message.chat.id, photo=response.content)
            else:
                bot.send_message(message.chat.id, "Failed to load image from GitHub")

            menu_message(message)

        else:
            bot.send_message(message.chat.id, "Введіть вагу від 30 до 150")
            bot.register_next_step_handler(message, process_new_weight)

        menu_message(message)

    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть числове значення для ваги.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Виникла помилка: {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data == 'Вік')
def editAge(call):
    bot.send_message(call.message.chat.id, "Введіть свій новий вік")
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    bot.register_next_step_handler(call.message, process_new_age)

def process_new_age(message):
    try:
        new_age = int(message.text)
        if 14 <= new_age <= 60:
            editUserAge(message.from_user.id, new_age)
            bot.send_message(message.chat.id, f"Вік успішно змінено на: {new_age}")
            menu_message(message)
        else:
            bot.send_message(message.chat.id, "Введіть вік від 14 до 60")
            bot.register_next_step_handler(message, process_new_age)


    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть числове значення для віку.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Виникла помилка: {str(e)}")


@bot.message_handler(commands=['end'])
def start_message(message):
    bot.send_message(message.chat.id, rf"bye bye")
    img = open('./img/gif1.mp4', 'rb')
    bot.send_video(message.chat.id, img, None, 'Text')
    img.close()
    bot.send_message(message.chat.id, "")


@bot.message_handler(commands=['info'])
def info_message(message):
    bot.send_message(message.chat.id, "Це інформація про нашого бота!")
    time.sleep(1)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Допомога: ")


bot.polling(non_stop=True)