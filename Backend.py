from flask import jsonify
import sqlite3
import re
from database import Password
from inputvalidator import Format 

manager = Password('password_storage.db')  # Instantiating the Password manager class
validator = Format()

class Backend:
    def __init__(self):
        self.user_id = None  # To store logged-in user ID

    def create_account(self, first_name, last_name, email, username, password=None):
        try:
            manager.ensure_connection()
            
            # Validate inputs
            checker, error = validator.get_valid_string(first_name)
            if not checker:
                return jsonify({"success": False, "error": error})
            
            checker, error = validator.get_valid_string(last_name)
            if not checker:
                return jsonify({"success": False, "error": error})
            
            checker, error = validator.is_valid_email(email)
            if not checker:
                return jsonify({"success": False, "error": error})
            
            checker, error = validator.get_valid_string(username)
            if not checker:
                return jsonify({"success": False, "error": error})
            
            if not password:
                password = self.generate_password()
            
            checker, error = validator.is_strong_password(password)
            if not checker:
                return jsonify({"success": False, "error": error})
            
            encrypted_password = manager.encrypt_password(password)
            
            # Insert into the database
            query = '''INSERT INTO users (first_name, last_name, email, username, password)
                       VALUES (?, ?, ?, ?, ?)'''
            manager.cursor.execute(query, (first_name, last_name, email, username, encrypted_password))
            manager.connect.commit()
            
            return jsonify({"success": True, "message": "Account created successfully.", "generated_password": password})
        
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                return jsonify({"success": False, "error": "Username already exists."})
            elif "email" in str(e):
                return jsonify({"success": False, "error": "Email already exists."})
            else:
                return jsonify({"success": False, "error": "Database integrity error."})
        
        except Exception as e:
            return jsonify({"success": False, "error": f"Unexpected error: {e}"})
    
    def login(self, username, password):
        try:
            manager.ensure_connection()
            
            # Validate inputs
            if not username:
                return jsonify({"success": False, "error": "Username cannot be empty."})
            if not password:
                 return jsonify({"success": False, "error": "Password cannot be empty."})
            # Query database
            query = '''SELECT user_id, password FROM users WHERE username = ?'''
            manager.cursor.execute(query, (username,))
            user = manager.cursor.fetchone()
            
            if user:
                user_id, encrypted_password = user
                decrypted_password = manager.decrypt_password(encrypted_password)
                if decrypted_password == password:
                    self.user_id = user_id
                    return jsonify({"success": True, "message": "Login successful."})
                else:
                    return jsonify({"success": False, "error": "Invalid password."})
            else:
                return jsonify({"success": False, "error": "Invalid username."})
        
        except Exception as e:
            return jsonify({"success": False, "error": f"Unexpected error: {e}"})
    
    def add_password(self, website, password=None):
        try:
            manager.ensure_connection()
            if not self.user_id:
                return jsonify({"success": False, "error": "You must log in before adding a password."})
            
            if not re.match(r'^(https?://)?(www\.)?[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$', website):
                return jsonify({"success": False, "error": "Invalid website format."})
            
            if not password:
                password = self.generate_password()
            
            checker, error = validator.is_strong_password(password)
            if not checker:
                return jsonify({"success": False, "error": error})
            
            encrypted_password = manager.encrypt_password(password)
            
            query = '''INSERT INTO passwords (user_id, website, password) VALUES (?, ?, ?)'''
            manager.cursor.execute(query, (self.user_id, website, encrypted_password))
            manager.connect.commit()
            
            return jsonify({"success": True, "message": f"Password for {website} added successfully."})
        
        except sqlite3.IntegrityError as ie:
            return jsonify({"success": False, "error": f"Database integrity error: {ie}"})
        except Exception as e:
            return jsonify({"success": False, "error": f"Unexpected error: {e}"})

    def find_password(self,password_website):
        try:
            manager.ensure_connection()
            if not self.user_id:
                return jsonify({"success": False, "error": "Please log in to find a password."})
                
            
            if find_password_website:
                query = '''SELECT website, password FROM passwords WHERE website = ? AND user_id = ?'''
                manager.cursor.execute(query, (password_website, self.user_id))
            else:
                return jsonify({"success": False, "error": "No input provided. Please enter a Website."})
                return

            records = manager.cursor.fetchall()

            if records: # statements checks if passwords are found 
                for website, encrypted_password in records:
                    decrypted_password = manager.decrypt_password(encrypted_password)
                    return jsonify({"success": True, "message": f"Website: {website}\nPassword: {decrypted_password}"})
            else:
                return jsonify({"success": False, "error": "No records found"})
        except Exception as e:
            return jsonify({"success": False, "error": f"Unexpected error: {e}"})
    def update_password(self, website,updated_password,confirm_password):
     try:
        # Ensure the database connection is active
         manager.ensure_connection()

        # Check login state
         if not self.user_id:
            return jsonify({"success": False, "error": "Please log in to update a password."})

        # Validate website input
         if not website:
            return jsonify({"success": False, "error": "Please input a website to update."})

        # Check if the website exists for the logged-in user
         query = '''SELECT password FROM passwords WHERE website = ? AND user_id = ?'''
         manager.cursor.execute(query, (website, self.user_id))
         existing_password = manager.cursor.fetchone()

         if not existing_password:
             return jsonify({"success": False, "error": "No record found for this website under your account."})

        # Auto-generate password if left blank
         if not updated_password:
             updated_password = self.generate_password()
             if not updated_password:
                 return jsonify({"success": False, "error": "Failed to generate a password. Please try again."})

        # Validate password strength
         is_valid, error = validator.is_strong_password(updated_password)
         if not is_valid:
             return jsonify({"success": False, "error": f"Password strength issue: {error}"})

        # Confirm password
         if updated_password != confirm_password:
             return {"success": False, "error": "Passwords do not match. Please try again."}

        # Encrypt the new password
         encrypted_password = manager.encrypt_password(updated_password)

        # Execute the update query
         update_query = '''UPDATE passwords SET password = ? WHERE website = ? AND user_id = ?'''
         manager.cursor.execute(update_query, (encrypted_password, website, self.user_id))
         manager.connect.commit()

        # Confirm success
         if manager.cursor.rowcount > 0:
             return jsonify({"success": True, "message": "Password updated successfully."})
         else:
             return jsonify({"success": False, "error": "Could not update the password. Please try again."})

     except sqlite3.DatabaseError as db_error:
         return jsonify({"success": False, "error": f"Database error: {db_error}"})
     except Exception as e:
         return jsonify({"success": False, "error": f"Unexpected error: {e}"})
    def view_password(self):
     try:
        # Ensure a logged-in user
         if not hasattr(self, 'user_id') or not self.user_id:
             return jsonify({"success": False, "error": "Please log in to view your saved passwords."}), 400

        # Fetch passwords for the logged-in user
         query = '''SELECT website, password FROM passwords WHERE user_id = ?'''
         manager.cursor.execute(query, (self.user_id,))
         rows = manager.cursor.fetchall()

        # Display results if any are found
         if rows:
             passwords = [{"website": website, "password": manager.decrypt_password(encrypted_password)} for website, encrypted_password in rows]
             return jsonify({"success": True, "passwords": passwords}), 200
         else:
             return jsonify({"success": False, "message": "No saved passwords found for your account."}), 404
     except Exception as e:
         return jsonify({"success": False, "error": f"Error viewing password: {e}"}), 500
    def delete_password(self,website):
     try:
        # Ensure a logged-in user
         if not hasattr(self, 'user_id') or not self.user_id:
             return jsonify({"success": False, "error": "Please log in to delete a password."}), 400

        
        # Validate input
         if not website:
             return jsonify({"success": False, "error": "Website cannot be empty. Please provide a valid website."}), 400

        # Query to delete the password
         query = '''DELETE FROM passwords WHERE user_id = ? AND website = ?'''
         manager.cursor.execute(query, (self.user_id, website))
         manager.connect.commit()

        # Feedback based on rows affected
         if manager.cursor.rowcount > 0:
             return jsonify({"success": True, "message": f"Password for website '{website}' deleted successfully."}), 200
         else:
             return jsonify({"success": False, "message": f"No matching record found for website '{website}'."}), 404
     except sqlite3.DatabaseError as db_error:
         return jsonify({"success": False, "error": f"Database error while deleting password: {db_error}"}), 500
     except Exception as e:
         return jsonify({"success": False, "error": f"Unexpected error deleting password: {e}"}), 500
    def generate_password(self):
        try:
            # Define character sets
            lowercase = string.ascii_lowercase
            uppercase = string.ascii_uppercase
            digits = string.digits
            punctuation = string.punctuation

            # Combine all character sets
            all_characters = lowercase + uppercase + digits + punctuation

            # Prompt for password length
            length = 12

            if not length.isdigit() or int(length) < 11:
                return jsonify({"success": False, "error": "Invalid or no input. Using default length of 12."}), 400

            length = int(length)

            if length < 4:  # Minimum length to accommodate at least one of each type
                return jsonify({"success": False, "error": "Password length too short. Using default length of 12."}), 400

            # Guarantee inclusion of at least one character from each set
            password = [
                secrets.choice(lowercase),
                secrets.choice(uppercase),
                secrets.choice(digits),
                secrets.choice(punctuation),
            ]

            # Fill the rest of the password length with random choices from all characters
            password += [secrets.choice(all_characters) for _ in range(length - 4)]

            # Shuffle to randomize character positions
            secrets.SystemRandom().shuffle(password)

            # Join list into a string and return the password
            return jsonify({"success": True, "password": ''.join(password)}), 200

        except Exception as e:
            return jsonify({"success": False, "error": f"An error occurred during password generation: {e}"}), 500

    def close_connection(self):
        try:
            # Check if the user is logged in
            if not hasattr(self, 'user_id') or not self.user_id:
                return jsonify({"success": False, "error": "Please log in to close the connection."}), 400

            manager.cursor.close()
            manager.connect.close()

            return jsonify({"success": True, "message": "Database connection closed."}), 200
        except Exception as e:
            return jsonify({"success": False, "error": f"Error closing database: {e}"}), 500
