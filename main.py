#main.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
from db import get_songs, add_songs, check_password, add_new_user, add_exercise, get_feed_for_user, get_workout_by_timestamp, add_length_and_type

app = Flask(__name__)
CORS(app)

def current_timestamp(): 
    return(int(time.time()))

@app.route('/', methods=['POST', 'GET'])
def songs():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400  

        add_songs(request.get_json())
        return 'Song Added'

    return get_songs()    

@app.route('/login', methods=['POST'])
def login_user():
    params = request.json
    username = params.get("username")
    password = params.get("password")
    return(check_password(username, password))


@app.route('/addUser', methods=['POST'])
def add_user():
    params = request.json
    username = params.get("username")
    password = params.get("password")
    add_new_user(username, password)
    return jsonify({"operation": "success"})

@app.route('/logWorkout', methods=['POST'])
def log_workout(): 
    timestamp = current_timestamp()
    params = request.json
    exercise_details = params.get("exercise_details")
    account_id = params.get("account_id")
    exercise_type = params.get("exercise_type")
    length = params.get("length")
    add_length_and_type(account_id=account_id, timestamp=timestamp, exercise_type=exercise_type, length=length)
    for exercise in exercise_details: 
        add_exercise(account_id=exercise["account_id"], timestamp=timestamp, exercise_type=exercise["exercise_type"], weight=exercise["weight"], reps=exercise["reps"])
    return jsonify({"operation": "success"})

@app.route('/getFeed', methods=['GET'])
def get_feed():
    params = request.args
    account_id = params.get("account_id")
    return (get_feed_for_user(account_id))

@app.route('/getWorkout', methods=['GET'])
def get_workout_details():
    params = request.args
    timestamp = params.get("timestamp")
    account_id = params.get("account_id")
    return (get_workout_by_timestamp(timestamp, account_id))


if __name__ == '__main__':
    app.run()