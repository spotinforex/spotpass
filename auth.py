# auth.py
from flask import Blueprint, request, jsonify
from backend import Backend

auth_routes = Blueprint('auth', __name__)  # Create Blueprint for authentication
backend = Backend()

@auth_routes.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    
    # Ensure required fields are provided
    if not all(key in data for key in ('first_name', 'last_name', 'email', 'username', 'password')):
        return jsonify({"error": "Missing required fields", "success": False}), 400
    
    return backend.create_account(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        username=data.get('username'),
        password=data.get('password')
    )

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    
    # Ensure required fields are provided
    if not all(key in data for key in ('username', 'password')):
        return jsonify({"error": "Missing username or password", "success": False}), 400
    
    return backend.login(
        username=data.get('username'),
        password=data.get('password')
    )
