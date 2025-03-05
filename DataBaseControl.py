import sqlite3
from datetime import datetime
from datetime import date
import os





def addUser(nick, age, weight, height, gender):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (Id INTEGER PRIMARY KEY AUTOINCREMENT, Nickname NVARCHAR(255) NOT NULL, Age INTEGER, Weight INTEGER, Height INTEGER, Gender NVARCHAR(255) NOT NULL)''')
    cursor.execute("INSERT INTO users (Nickname, Age , Weight  , Height , Gender) VALUES (?, ?, ?, ?, ?)", (nick, age, weight, height, gender))
    connection.commit()
    connection.close()

def viewUserDataBase():

    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()
    connection.commit()

    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())
    print('\n')

    connection.close()


def FindUserDataBase(name):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Nickname FROM users WHERE Nickname = ?", (name))
    result = cursor.fetchall()
    print(result)

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
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (Id INTEGER PRIMARY KEY AUTOINCREMENT, Nickname NVARCHAR(255) NOT NULL, Age INTEGER, Weight INTEGER, Height INTEGER, Gender NVARCHAR(255) NOT NULL)''')
    connection.commit()
    cursor.execute("SELECT * FROM users WHERE Nickname = ?", (username,))
    result = cursor.fetchone()
    connection.close()
    return result is not None


def create_tables_Exercises():
    # Connect to SQLite database (creates a new database if not exists)
    conn = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = conn.cursor()

    # Create Exercises table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Exercises (
                        Exercises_ID INTEGER PRIMARY KEY,
                        Exercises_Name TEXT,
                        Exercises_Type TEXT
                    )''')

    # Create Product table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
                        Product_ID INTEGER PRIMARY KEY,
                        Product_Name TEXT,
                        Calories INTEGER,
                        Product_Type TEXT,
                    )''')


    conn.commit()
    conn.close()

def table_Product():
    conn = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
                        Product_ID INTEGER PRIMARY KEY,
                        Product_Name TEXT,
                        Calories INTEGER,
                        Product_Type TEXT,
                        Time Text
                    )''')


    conn.commit()
    conn.close()
    
def drop_table_Product():
    conn = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Product")

    conn.commit()
    conn.close()






def insert_exercises_data():
    conn = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = conn.cursor()

    exercises_data = [
        (0, '', ''),
        (1, 'Жим гантель на лавці', 'Грудні м\'язи'),
        (2, 'Жим штанги на лавці', 'Грудні м\'язи'),
        (3, 'Розведення гантелей на лавці', 'Грудні м\'язи'),
        (4, 'Жим гантелей на нахилених лавці', 'Грудні м\'язи'),
        (5, 'Зведення рук в тренажері метелик', 'батерфляй, Грудні м\'язи'),
        (6, 'Зведення рук на блокових тренажерах', 'Грудні м\'язи'),
        (7, 'Жим штанги на похилій лаві', 'Грудні м\'язи'),
        (8, 'Віджимання на брусах', 'Грудні м\'язи'),
        (9, 'Жим лежачи на похилій лаві', 'Грудні м\'язи'),
        (10, 'Пулловер', 'Грудні м\'язи'),
        (11, 'Віджимання від підлоги', 'Грудні м\'язи'),
        (12, 'Тяга блока до грудей', 'Спина'),
        (13, 'Тяга блока до живота', 'Спина'),
        (14, 'Станова тяга', 'Спина'),
        (15, 'Тяга гантелей в нахилі на лавці', 'Спина'),
        (16, 'Тяга гантелей в наклоні', 'Спина'),
        (17, 'Тяга штанги в наклоні', 'Спина'),
        (18, 'Гіперекстензія', 'Спина'),
        (19, 'Підтягування', 'Спина'),
        (20, 'Шраги', 'Спина'),
        (21, 'Тяга на тренажері сидячи з упором грудей', 'Спина'),
        (22, 'Тяга штанги до підборіддя', 'Спина'),
        (23, 'Жим гантелей сидячи або стоячи', 'Плечі'),
        (24, 'Підйом гантелей на бічні дельтовидні м\'язи', 'Плечі'),
        (25, 'Підйом штанги в обертанні', 'Плечі'),
        (26, 'Махи', 'Плечі'),
        (27, 'Присідання з штангою', 'Ноги'),
        (28, 'Підйом на носки', 'Ноги'),
        (29, 'Присідання зі штангою на грудях', 'Ноги'),
        (30, 'Гак-присідання в тренажері', 'Ноги'),
        (31, 'Присідання з штангою перед собою', 'Ноги'),
        (32, 'Присідання на одній нозі з гантелями', 'Ноги'),
        (33, 'Жим ногами в станку', 'Ноги'),
        (34, 'Розгинання ніг в тренажері', 'Ноги'),
        (35, 'Згинання ніг в тренажері', 'Ноги'),
        (36, 'Зведення ніг сидячи в тренажері', 'Ноги'),
        (37, 'Відведення ноги назад в блочному тренажері', 'Ноги'),
        (38, 'Підйом тулуба', 'Прес'),
        (39, 'V-Ups підйоми', 'Прес'),
        (40, 'Планка', 'Прес'),
        (41, 'Спринтові скручення', 'Прес'),
        (42, 'Зворотні скручування', 'Прес'),
        (43, 'Альпініст', 'Прес'),
        (44, 'Планка з обважнювачем', 'Прес'),
        (45, 'Бокова планка', 'Прес'),
        (46, 'Скручування на лавці', 'Прес'),
        (47, 'Підйом колін на перекладині', 'Прес'),
        (48, 'Планка на перекладині', 'Прес'),
        (49, 'Бігова доріжка як розминка', 'Кардіо'),
        (50, 'Бігова доріжка з рівнем навантаження', 'Кардіо'),
        (51, 'Степер', 'Кардіо'),
        (52, 'Велотренажер', 'Кардіо'),
        (53, 'Скакалка', 'Кардіо'),
        (54, 'Гребний тренажер', 'Кардіо'),
        (55, 'Еліптичний тренажер', 'Кардіо'),
        (56, 'Згинання однієї руки з рукояткою нижнього блоку', 'Біцепс'),
        (57, 'Згинання рук з рукоятками верхніх блоків', 'Біцепс'),
        (58, 'Підйом штанги на біцепс', 'Біцепс'),
        (59, 'Підйом штанги на біцепс хват зверху', 'Біцепс'),
        (60, 'Підйом гантелей на біцепс сидячи', 'Біцепс'),
        (61, 'Згинання рук на лавці Скотта', 'Біцепс'),
        (62, 'Згинання рук з гантелями на похилій лавці', 'Біцепс')
    ]


    cursor.executemany('INSERT INTO Exercises (Exercises_ID, Exercises_Name, Exercises_Type) VALUES (?, ?, ?)', exercises_data)

  
    conn.commit()
    conn.close()


def insert_products_data():
    conn = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = conn.cursor()
    products = [
    (1, 'Овочевий салат з авокадо', 150, 'Салати', 'сніданок'),
    (2, 'Грильована курка з овочами', 300, 'Гарніри та основні страви', 'обід'),
    (3, 'Тунець з броколі та кунжутом', 250, 'Рибні страви', 'обід'),
    (4, 'Фруктовий салат з м''ятою', 120, 'Салати', 'вечеря'),
    (5, 'Печена картопля з розмарином', 200, 'Гарніри та основні страви', 'сніданок'),
    (6, 'Цезар з куркою', 350, 'Салати', 'обід'),
    (7, 'Омлет з шпинатом та сиром', 200, 'Сніданки', 'сніданок'),
    (8, 'Грецький салат з оливками', 180, 'Салати', 'вечеря'),
    (9, 'Рибний суп з креветками', 280, 'Супи', 'обід'),
    (10, 'Смузі з ягодами та бананом', 150, 'Напої та коктейлі', 'сніданок'),
    (11, 'Чіа пудинг з медом та фруктами', 220, 'Десерти', 'сніданок'),
    (12, 'Гречана каша з овочами', 230, 'Гарніри та основні страви', 'сніданок'),
    (13, 'Піца з томатами та базиліком', 350, 'Піци', 'вечеря'),
    (14, 'Курячий бульйон з вермишеллю', 150, 'Супи', 'сніданок'),
    (15, 'Печена лосось з цитрусовим соусом', 320, 'Рибні страви', 'вечеря'),
    (16, 'Салат з манго та куркою', 270, 'Салати', 'обід'),
    (17, 'Вівсянка з медом та горіхами', 180, 'Сніданки', 'сніданок'),
    (18, 'Свіжі овочі з гірчичним соусом', 120, 'Салати', 'вечеря'),
    (19, 'Стейк з яловичини з овочами', 400, 'Гарніри та основні страви', 'обід'),
    (20, 'Фруктовий льодяник', 100, 'Десерти', 'вечеря'),
    (21, 'Суп з квасолею та овочами', 200, 'Супи', 'сніданок'),
    (22, 'Смузі з манго та апельсином', 170, 'Напої та коктейлі', 'сніданок'),
    (23, 'Чіа пудинг з кокосовим молоком', 250, 'Десерти', 'сніданок'),
    (24, 'Гарбузовий крем-суп', 180, 'Супи', 'вечеря'),
    (25, 'Паста з томатним соусом та овочами', 320, 'Паста', 'обід'),
    (26, 'Салат з руколою та карамелізованими горіхами', 160, 'Салати', 'сніданок'),
    (27, 'Фреш з моркви та апельсина', 140, 'Напої та коктейлі', 'сніданок'),
    (28, 'Овочевий суп з куркою', 250, 'Супи', 'вечеря'),
    (29, 'Стейк з лосося на грилі', 350, 'Рибні страви', 'обід'),
    (30, 'Млинці з ягодами', 280, 'Десерти', 'вечеря'),
    (31, 'Салат з тунцем та маслинами', 290, 'Салати', 'обід'),
    (32, 'Мюслі з йогуртом та фруктами', 200, 'Сніданки', 'сніданок'),
    (33, 'Грецький омлет', 230, 'Сніданки', 'сніданок'),
    (34, 'Суп-пюре з гарбуза та коренеплодів', 210, 'Супи', 'обід'),
    (35, 'Курячі крильця в медово-гірчичному соусі', 380, 'Закуски', 'вечеря'),
    (36, 'Стейк з курки з овочами на грилі', 320, 'Гарніри та основні страви', 'обід'),
    (37, 'Печена цільнокомбікормова картопля', 220, 'Гарніри та основні страви', 'вечеря'),
    (38, 'Рибний гуляш з картоплею', 300, 'Рибні страви', 'сніданок'),
    (39, 'Вегетаріанський бургер', 350, 'Сніданки', 'вечеря'),
    (40, 'Фруктовий салат з гранолою', 180, 'Сніданки', 'вечеря'),
    (41, 'Крем-суп з броколі', 190, 'Супи', 'вечеря'),
    (42, 'Паста з грибами та соусом альфредо', 380, 'Паста', 'обід'),
    (43, 'Салат зі свіжими овочами та горіхами', 170, 'Салати', 'вечеря'),
    (44, 'Чіабатта з авокадо та помідорами', 250, 'Закуски', 'сніданок'),
    (45, 'Лосось під кисло-солодким соусом', 310, 'Рибні страви', 'обід'),
    (46, 'Салат з водяних горіхів та ягодами', 200, 'Салати', 'сніданок'),
    (47, 'Горяча каша з кокосовим молоком', 240, 'Сніданки', 'обід'),
    (48, 'Суп зі шпинатом та кокосовим молоком', 180, 'Супи', 'вечеря'),
    (49, 'Печений картофель з овочами', 270, 'Гарніри та основні страви', 'сніданок'),
    (50, 'Томатний суп з мідіями', 250, 'Супи', 'обід'),
    (51, 'Смажений рис з овочами', 320, 'Гарніри та основні страви', 'сніданок'),
    (52, 'Фруктовий морозиво', 150, 'Десерти', 'обід'),
    (53, 'Салат з капусти з морквою та яблуками', 160, 'Салати', 'сніданок'),
    (54, 'Стейк з телятини з карамелізованою цибулею', 400, 'Гарніри та основні страви', 'вечеря'),
    (55, 'Омлет з шпинатом та помідорами', 220, 'Сніданки', 'сніданок'),
    (56, 'Чіабатта з кавуном та м''ятним соусом', 260, 'Закуски', 'обід'),
    (57, 'Грецький салат з куркою', 290, 'Салати', 'вечеря'),
    (58, 'Піца з тунцем та каперсами', 330, 'Піци', 'сніданок'),
    (59, 'Суп з курячим бульйоном та локшиною', 230, 'Супи', 'вечеря'),
    (60, 'Рибна запіканка з картоплею', 320, 'Рибні страви', 'обід'),
    (61, 'Шоколадний мус', 200, 'Десерти', 'сніданок'),
    (62, 'Салат з куркою та кокосовим молоком', 280, 'Салати', 'вечеря'),
    (63, 'Фруктова нарізка з м''ятним медом', 170, 'Сніданки', 'сніданок'),
    (64, 'Суп з курячим бульйоном та локшиною', 250, 'Супи', 'обід'),
    (65, 'Паста з куркою та грибами', 350, 'Паста', 'сніданок'),
    (66, 'Салат з міксом зелених листових овочів', 120, 'Салати', 'вечеря'),
    (67, 'Омлет з томатами та сиром', 240, 'Сніданки', 'обід'),
    (68, 'Смажена курка з броколі', 290, 'Гарніри та основні страви', 'вечеря'),
    (69, 'Салат з огірків та помідорів', 150, 'Салати', 'сніданок'),
    (70, 'Рибні котлети з кабачками', 280, 'Рибні страви', 'обід'),
    (71, 'Фруктове пюре', 130, 'Десерти', 'сніданок'),
    (72, 'Суп-крем з гарбуза та імбирними прянощами', 210, 'Супи', 'вечеря'),
    (73, 'Кукурудзяний гарнір з овочами', 230, 'Гарніри та основні страви', 'сніданок'),
    (74, 'Салат з айви та горішками з сиром', 180, 'Салати', 'обід'),
    (75, 'Омлет з лососем та шпинатом', 260, 'Сніданки', 'вечеря'),
    (76, 'Квіткова каша з кунжутом', 200, 'Сніданки', 'обід'),
    (77, 'Цвітна капуста на грилі', 180, 'Закуски', 'вечеря'),
    (78, 'Піца з грибами та шпинатом', 320, 'Піци', 'сніданок'),
    (79, 'Червона риба зі спаржею', 300, 'Рибні страви', 'обід'),
    (80, 'Салат з ягід та оріхів', 170, 'Салати', 'вечеря')
    ]
    cursor.executemany('INSERT INTO Product (Product_ID, Product_Name, Calories, Product_Type, Time) VALUES (?, ?, ?, ?, ?);', products)
   
    conn.commit()
    conn.close()




def viewFullTableExercises(id):
    connection = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = connection.cursor()

    cursor.execute("SELECT  FROM Exercises where Exercises_ID=?", (id,))
    print(cursor.fetchall())
    print('\n')

    connection.close()

def viewTableExercises(id):
    connection = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Exercises_ID,Exercises_Name FROM Exercises where Exercises_ID=?", (id,))
    print(cursor.fetchall())
    print('\n')

    connection.close()


def getTableExercisesName(id):
    connection = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Exercises_Name FROM Exercises WHERE Exercises_ID=?", (id,))
    rows = cursor.fetchall()
    
    exercise_names = [row[0] for row in rows]

    connection.close()

    return exercise_names


def viewTableProducts():

    connection = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = connection.cursor()
    connection.commit()

    cursor.execute("SELECT * FROM Product")
    print(cursor.fetchall())
    print('\n')

    connection.close()



def editUserHeigh(userId,height):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET Height = ? WHERE  Nickname = ?",(height,userId))
    connection.commit()

    connection.close()


def editUserWeigh(userId,weight):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET Weight = ? WHERE  Nickname = ?",(weight,userId))
    connection.commit()

    connection.close()



def editUserAge(userId,age):
    connection = sqlite3.connect('DataBase/User.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET Age = ? WHERE  Nickname = ?",(weight,userId))
    connection.commit()

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
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        cursor.execute("INSERT INTO Training (TrainingName, TrainingDate, UserId) VALUES (?, ?, ?)", (training_name, training_date, user_id))
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





async def schedualMessage(user_id):
    today = date.today()
    isSendedMessage = 0
    #today  = "2024-04-21"
    curTime  = datetime.now().strftime('%H')
    print(today)
    print(curTime)
    while(True):
        try:
            conn = sqlite3.connect('DataBase/User.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Training WHERE UserId=? AND TrainingDate=?", (user_id, today,))
            training_data = cursor.fetchall()
            if not training_data:  
                print("error")
            else:
                if(curTime == "08" and   isSendedMessage == 0):
                    print(training_data)
                    isSendedMessage = 1
                elif(curTime != "08" and   isSendedMessage == 1):
                    isSendedMessage = 0

        except sqlite3.Error as e:
            print("Error getting training data:", e)
        finally:
            if conn:
                conn.close()


#------------------------TREINING-----------------------------
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

import sqlite3

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

def add_training_day_F(user_id, day, tasks):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute("SELECT UserId FROM TrainingDay WHERE UserId=?", (user_id,))
    existing_day = cursor.fetchone()

    if existing_day:
        cursor.execute("UPDATE TrainingDay SET {}=? WHERE UserId=?".format(day), (tasks, user_id,))
    else:
        cursor.execute("INSERT INTO TrainingDay (UserId, {}) VALUES (?, ?)".format(day), (user_id, tasks,))

    conn.commit()
    conn.close()


#----------Products-----------
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
    print("Training table is exist or created successfully.")
    conn.close()


def drop_products_table():
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS ProductsInDay")
    conn.commit()
    print("Training table dropped successfully.")
    conn.close()


def add_products_day_F(user_id, day, tasks):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute("SELECT UserId FROM ProductsInDay WHERE UserId=?", (user_id,))
    existing_day = cursor.fetchone()

    if existing_day:
        cursor.execute("UPDATE ProductsInDay SET {}=? WHERE UserId=?".format(day), (tasks, user_id,))
    else:
        cursor.execute("INSERT INTO ProductsInDay (UserId, {}) VALUES (?, ?)".format(day), (user_id, tasks,))

    conn.commit()
    conn.close()

def add_products_day_F(user_id, day, tasks):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute("SELECT UserId FROM ProductsInDay WHERE UserId=?", (user_id,))
    existing_day = cursor.fetchone()

    if existing_day:
        cursor.execute("UPDATE ProductsInDay SET {}=? WHERE UserId=?".format(day), (tasks, user_id,))
    else:
        cursor.execute("INSERT INTO ProductsInDay (UserId, {}) VALUES (?, ?)".format(day), (user_id, tasks,))

    conn.commit()
    conn.close()




def getTableProductsName(id):
    connection = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Product_Name FROM ProductsInDay WHERE Product_ID=?", (id,))
    rows = cursor.fetchall()

    products_names = [row[0] for row in rows]

    connection.close()

    return products_names[0] if products_names else None




# def getTableProductsName(id):
#     connection = sqlite3.connect('DataBase/Exercises_Products.db')
#     cursor = connection.cursor()

#     cursor.execute("SELECT Product_Name, 'Рекомендовано: ' || Time FROM Product WHERE Product_ID=?", (id,))
#     # Тут вміст запиту було виправлено, а саме додано 'Рекомендовано: ' || Time

#     rows = cursor.fetchall()

#     product_info = [(row[0], row[1]) for row in rows]

#     connection.close()

#     return product_info[0] if product_info else None




def getTableProductsName(id):
    connection = sqlite3.connect('DataBase/Exercises_Products.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Product_Name || '. Рекомендовано: ' || Time FROM Product WHERE Product_ID=?", (id,))

    row = cursor.fetchone()

    product_info = row[0] if row else None

    connection.close()

    return product_info
#add_training_day_F("2345666", "Friday", "SPINA")

def add_training_day_F_1(user_id, day, tasks):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    cursor.execute("SELECT UserId FROM ProductsInDay WHERE UserId=?", (user_id,))
    existing_day = cursor.fetchone()

    if existing_day:
        cursor.execute("UPDATE ProductsInDay SET {}=? WHERE UserId=?".format(day), (tasks, user_id,))
    else:
        cursor.execute("INSERT INTO ProductsInDay (UserId, {}) VALUES (?, ?)".format(day), (user_id, tasks,))

    conn.commit()
    conn.close()

# def get_exercise_for_day(user_id, day):
#     conn = sqlite3.connect('DataBase/User.db')
#     cursor = conn.cursor()
    
#     # Використовуємо параметризований запит
#     cursor.execute('''
#         SELECT {} FROM TrainingDay 
#         WHERE UserId = ?
#     '''.format(day), (user_id,))  
    
#     # Отримуємо результат та повертаємо його
#     exercise = cursor.fetchone()[0]
    
#     conn.close()
    
#     return exercise


def get_exercise_for_day(user_id, day):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    
    # Використовуємо параметризований запит
    cursor.execute('''
        SELECT {} FROM TrainingDay 
        WHERE UserId = ?
    '''.format(day), (user_id,))  
    
    # Отримуємо результат
    exercise = cursor.fetchone()
    
    conn.close()
    
    # Перевіряємо, чи є результат
    if exercise is None:
        return "Відсутня інформація про вправи на цей день"
    else:
        return exercise[0]
    
def get_product_for_day(user_id, day):
    conn = sqlite3.connect('DataBase/User.db')
    cursor = conn.cursor()
    
    # Використовуємо параметризований запит
    cursor.execute('''
        SELECT {} FROM ProductsInDay 
        WHERE UserId = ?
    '''.format(day), (user_id,))  
    
    # Отримуємо результат
    exercise = cursor.fetchone()
    
    conn.close()
    
    # Перевіряємо, чи є результат
    if exercise is None:
        return "Відсутня інформація про вправи на цей день"
    else:
        return exercise[0]



 
#create_training_day_table()

# add_training_day_F('367165560','Monday','SPINA')
# add_training_day_F('367165560','Tuesday','SPINA')
#add_training_day_F('367165560','Sunday','SPINA')

view_training_day_table()
print(get_exercise_for_day('367165560','Tuesday'))

#create_products_table()
#insert_products_data()
 

#print(getTableProductsName(3))

#view_training_day_table_by_id(367165560)

#create_training_day_table()
#add_training_day(2345665, "Leg", "Heir", "DS", "SD", "SD", "WE", "SD")
#view_training_day_table()

#drop_training_day_table()

#viewTableExercises(2)
    #while(True):

        
#editUserHeigh(120,'367165560')
#print(getHeight('367165560'))
#print(getWeight('367165560'))
#print(getAge('367165560'))


#viewTableProducts()
#insert_products_data()
#viewUserDataBaseProducts()

#addUser('Андрій', 13,60,170,'Чоловік')
#viewUserDataBase()
#print(is_user_registered('Андрій'))


#FindUserDataBase("Улех")


#create_tables_Exercises()

#insert_products_data()
#deleteUserDatabase()
#insertTrainingData("Leg", "2024-04-22", 367165560)
#DeleteTrainingData("2024-04-9",367165560)
#print(getTrainingData(367165560))

#schedualMessage(367165560)




