import requests
import key_name
from pprint import pprint
import sqlite3
from django.utils import timezone
import os

data_kp = key_name.KINOPOISK_URL + key_name.KINOPOISK_URL_MAIN
data_kp += '/filters'
response_kp = requests.get(data_kp, headers=key_name.DATA_KP)
if response_kp.status_code == 200:
    results = response_kp.json()['genres']
    # pprint(scrinshot)

# con = sqlite3.connect('../db.sqlite3')
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'db.sqlite3')
con = sqlite3.connect(db_path)
cur = con.cursor()
for i in results:
    print(i['genre'])

    sql_select = '''
        SELECT MAX(id)
        FROM films_genres;
    '''
    id_add = cur.execute(sql_select)
    id_add = id_add.fetchone()
    id_add = id_add[0] + 1 if id_add[0] is not None else 1
    # print(id_add[0])
    sql_inzert = '''
        INSERT INTO films_genres
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    sql_request = (
        id_add, timezone.now(), i['genre']
    )
    cur.execute(sql_inzert, sql_request)
    print('ok')
con.commit()
con.close()
