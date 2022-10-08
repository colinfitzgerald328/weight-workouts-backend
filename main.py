#main.py
from flask import Flask, jsonify, request
from db import get_songs, add_songs, check_password, add_new_user

app = Flask(__name__)

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
    return "User successfully added to database"
      


if __name__ == '__main__':
    app.run()