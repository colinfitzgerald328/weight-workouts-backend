#db.py
import os
import pymysql
from flask import jsonify

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        print(e)

    return conn


def get_songs():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM accounts;')
        songs = cursor.fetchall()
        if result > 0:
            got_songs = jsonify(songs)
        else:
            got_songs = 'No Songs in DB'
    conn.close()
    return got_songs

def add_songs(song):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO songs (title, artist, genre) VALUES(%s, %s, %s)', (song["title"], song["artist"], song["genre"]))
    conn.commit()
    conn.close()

def check_password(username, password):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM accounts where username=%s and password=%s', (username, password))
        account = cursor.fetchall()
        if result > 0: 
            got_account = {"operation": "success"}
        else: 
            got_account = {"operation": "error"}
    conn.close()
    return jsonify(got_account)


def add_new_user(username, password):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO accounts (username, password) VALUES(%s, %s)', (username, password))
    conn.commit()
    conn.close()