# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create the Flask app and configure the database URI
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.name}>'

# Create the database and tables
# @app.before_first_request
# def create_tables():
#     db.create_all()
# # Create the database and tables
# db.create_all()
# Create the database and tables
with app.app_context():
    db.create_all()


# Homepage route
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the user management and authentication system!'}), 200

# List users
@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    result = [{'id': user.id, 'name': user.name, 'email': user.email, 'last_login': user.last_login} for user in users]
    return jsonify(result), 200

# Create user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Get user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'last_login': user.last_login}), 200

# Update user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200

# Delete user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or user.password != password:
        return jsonify({'message': 'Invalid credentials'}), 401

    # Update the last login timestamp
    user.last_login = datetime.now()
    db.session.commit()

    return jsonify({'message': 'Login successful'}), 200

if __name__ == '__main__':
    app.run(debug=True)
