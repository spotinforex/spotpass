import re

class Format:
    def __init__(self):
        pass
    
    def is_strong_password(self, password):  # Function to check strong password input validation
        try:
            if len(password) < 8:
                return False, "Password must be at least 8 characters long."
            if not any(char.isdigit() for char in password):
                return False, "Password must include at least one digit."
            if not any(char.isupper() for char in password):
                return False, "Password must include at least one uppercase letter."
            if not any(char in "!@#$%^&*()-_+=<>?/\\|{}[]:;" for char in password):
                return False, "Password must include at least one special character."
            return True, "Strong password."
        except Exception as e:
            return False, f"An error occurred while checking the password: {e}"

    def get_valid_string(self, prompt):  # Function to check string input validation
        try:
            min_length = 1
            if len(prompt.strip()) >= min_length:
                return True, prompt.strip()
            else:
                return False, f"Input must be at least {min_length} characters long."
        except Exception as e:
            return None, f"An error occurred while validating the string: {e}"

    def is_valid_email(self, email):  # Function to check email input validation
        try:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(pattern, email):
                return True, "Valid email."
            else:
                return False, "Invalid email format."
        except Exception as e:
            return False, f"An error occurred while validating the email: {e}"

    def get_valid_int(self, prompt):  # Function to check number validation
        try:
            value = int(prompt.strip())
            return value
        except ValueError:
            return False, "Invalid input. Please enter a numeric value."
        except Exception as e:
            return False, f"An error occurred while validating the number: {e}"
