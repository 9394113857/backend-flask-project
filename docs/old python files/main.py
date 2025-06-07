# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/')
def index():
    return jsonify(message="Welcome to the Flask API!")

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Dummy check (replace with real DB logic)
    if username == 'admin' and password == 'admin':
        return jsonify(success=True, message='Login successful', token='fake-jwt-token')
    else:
        return jsonify(success=False, message='Invalid credentials'), 401

@app.route('/profile', methods=['GET'])
def profile():
    return jsonify(user={"username": "admin", "email": "admin@example.com"})

if __name__ == '__main__':
    app.run(debug=True)
