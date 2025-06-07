from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime, timezone

# === Initialize the Flask app ===
app = Flask(__name__)
CORS(app, supports_credentials=True)

# === App Configurations ===
app.secret_key = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pythonlogin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# === Initialize database and migration ===
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# === User Model ===
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

# === Helper Function ===
def get_current_time():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

# === Routes ===

@app.route('/')
def hello_world():
    return jsonify({
        'message': 'Hello, World!',
        'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'time': datetime.now(timezone.utc).strftime('%H:%M:%S'),
        'timestamp': get_current_time()
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    account = Account.query.filter_by(username=username).first()
    if account and check_password_hash(account.password, password):
        session['loggedin'] = True
        session['id'] = account.id
        session['username'] = account.username
        return jsonify({
            'message': 'Login successful',
            'username': account.username,
            'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
            'time': datetime.now(timezone.utc).strftime('%H:%M:%S'),
            'timestamp': get_current_time()
        }), 200

    return jsonify({'error': 'Incorrect username or password'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'error': 'All fields are required'}), 400
    if Account.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return jsonify({'error': 'Invalid email format'}), 400
    if not re.match(r'[A-Za-z0-9]+', username):
        return jsonify({'error': 'Username must contain only letters and numbers'}), 400

    hashed_password = generate_password_hash(password)
    new_account = Account(username=username, password=hashed_password, email=email)
    db.session.add(new_account)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201

@app.route('/home', methods=['GET'])
def home():
    if 'loggedin' in session:
        return jsonify({
            'message': f"Welcome {session['username']}!",
            'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
            'time': datetime.now(timezone.utc).strftime('%H:%M:%S'),
            'timestamp': get_current_time()
        }), 200
    return jsonify({'error': 'Unauthorized'}), 401

@app.route('/profile', methods=['GET'])
def profile():
    if 'loggedin' in session:
        account = Account.query.filter_by(id=session['id']).first()
        if account:
            return jsonify({
                'id': account.id,
                'username': account.username,
                'email': account.email,
                'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
                'time': datetime.now(timezone.utc).strftime('%H:%M:%S'),
                'timestamp': get_current_time()
            }), 200
    return jsonify({'error': 'Unauthorized'}), 401

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({
        'message': 'Logged out successfully',
        'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'time': datetime.now(timezone.utc).strftime('%H:%M:%S'),
        'timestamp': get_current_time()
    }), 200

# === Run the App ===
if __name__ == '__main__':
    app.run(debug=False)



