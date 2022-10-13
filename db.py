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
            got_account = {"operation": "success", "account_info": account}
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


def add_exercise(account_id, timestamp, exercise_type, weight, reps): 
    conn = open_connection()
    with conn.cursor() as cursor: 
        cursor.execute('INSERT INTO workouts (account_id, TIMESTAMP, exercise_type, weight, reps) VALUES (%s, %s, %s, %s, %s)', (account_id, timestamp, exercise_type, weight, reps))
    conn.commit()
    conn.close()


def get_feed_for_user(account_id): 
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT TIMESTAMP, COUNT(*) as sets, SUM(reps) as total_reps from workouts where account_id=%s group by TIMESTAMP order by TIMESTAMP DESC', (account_id))
        feed = cursor.fetchall()
        if result > 0:
            got_feed = {"operation": "success", "feed": feed}
        else:
            got_feed = {"operation": "error"}
    conn.close()
    return jsonify(got_feed)


def get_workout_by_timestamp(timestamp, account_id): 
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * from workouts where TIMESTAMP=%s and account_id=%s', (timestamp, account_id))
        workout = cursor.fetchall()
        if result > 0:
            got_workout = {"workout_details": workout}
        else:
            got_workout = {"operation": "error"}
    conn.close()
    return jsonify(got_workout)

def add_length_and_type(account_id, timestamp, exercise_type, length): 
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO workout_details (account_id, TIMESTAMP, exercise_type, length) VALUES (%s, %s, %s, %s)', (account_id, timestamp, exercise_type, length))
        conn.commit()
        conn.close()

def get_workout_details_by_timestamp(timestamp, account_id): 
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * from workout_details where TIMESTAMP=%s and account_id=%s', (timestamp, account_id))
        workout_details = cursor.fetchall()
        if result > 0:
            got_workout_stats = {"workout_stats": workout_details}
        else:
            got_workout_stats = {"operation": "error"}
    conn.close()
    return jsonify(got_workout_stats)

def add_user_profile_by_account(account_id, name, city, image_url): 
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO profiles (account_id, name, city, image_url) VALUES (%s, %s, %s, %s)', (account_id, name, city, image_url))
    conn.commit()
    conn.close()


def get_profile_by_account(account_id): 
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * from profiles where account_id=%s', (account_id))
        profile = cursor.fetchall()
        if result > 0:
            got_profile = {"user_profile": profile}
        else:
            got_profile = {"operation": "error"}
    conn.close()
    return jsonify(got_profile)

def delete_profile_by_account(account_id): 
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM profiles WHERE account_id=%s', (account_id))
    conn.commit()
    conn.close()
