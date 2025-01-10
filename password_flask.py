from flask import Blueprint, request
from backend import Backend

password_routes = Blueprint('password', __name__)  # Create Blueprint for password management
backend = Backend()

@password_routes.route('/add_password', methods=['POST'])
def add_password():
    data = request.json
    return backend.add_password(
        website=data.get('website'),
        password=data.get('password')
    )

@password_routes.route('/find_password', methods=['POST'])
def find_password():
    data = request.json
    return backend.find_password(password_website=data.get('website'))

@password_routes.route('/update_password', methods=['POST'])
def update_password():
    data = request.json
    return backend.update_password(
        website=data.get('website'),
        updated_password=data.get('updated_password'),
        confirm_password=data.get('confirm_password')
    )

@password_routes.route('/delete_password', methods=['POST'])
def delete_password():
    data = request.json
    return backend.delete_password(website=data.get('website'))

@password_routes.route('/view_passwords', methods=['GET'])
def view_passwords():
    return backend.view_password()
