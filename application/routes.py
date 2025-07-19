from flask import current_app as app, jsonify,request
from flask_security import auth_required,roles_required,current_user,hash_password
from .database import db

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the Vehicle Parking App!</h1>"

@app.route('/api/admin')
@auth_required('token')
@roles_required('admin')
def admin_home():
    return jsonify({
        "message": "Welcome to the admin home page!"
    })

@app.route('/api/user')
@auth_required('token')
@roles_required('user')
def user_home():
    user = current_user
    return jsonify({
        "username": user.username,
        "email": user.email,
        "password": user.password
    })

@app.route('/api/register', methods=['POST'])
def create_user():
    credentials = request.get_json()
    if not app.security.datastore.find_user(email  = credentials['email']):
        app.security.datastore.create_user(email= credentials['email'],
                                           username= credentials['username'],
                                           password=hash_password(credentials['password']),
                                           roles=['user'])
        db.session.commit()
        return jsonify({
            "message": "User created successfully!"
        }), 201
    
    return jsonify({
            "message": "User already exists!"
        }), 409