import sqlite3
from services import get_data


db = sqlite3.connect('sqlite3.db')
cursor = db.cursor()


def initizlize():
    cursor.execute("""CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        city_link TEXT,
        city_part TEXT,
        city_part_link TEXT,
        count TEXT
    )""")

    data = get_data()
    data_tuples = [(i['city_link'], i['city_part'], i['city_part_link'], i['count'], i['city']) for i in data]
    for data_tuple in data_tuples:
        cursor.execute('SELECT * FROM cities WHERE city=?', (data_tuple[4],))
        entry = cursor.fetchone()
        if entry is None:
            cursor.executemany("INSERT INTO cities (city_link, city_part, city_part_link, count, city) VALUES (?, ?, ?, ?, ?)", (data_tuple,))
        else:
            cursor.executemany("UPDATE cities SET city_link=?, city_part=?, city_part_link=?, count=? WHERE city=?", (data_tuple,))
    db.commit()



def find_cities(city: str):
    cities = cursor.execute("SELECT * FROM cities")
    cities_list = []
    for _city in cities:
        if city.lower() in str(_city[1]).lower() or city.lower() in str(_city[3]).lower():
            cities_list.append(_city)
    
    return cities_list


def get_city(city_id: int):
    cursor.execute("SELECT * FROM cities WHERE id=?", (city_id,))
    city = cursor.fetchone()
    return city