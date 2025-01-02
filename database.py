import os
import sqlite3
from cryptography.fernet import Fernet

class Password:
    # Initialize the class and connect to the database
    def __init__(self, db_name="password_manager.db", key_file="key.key"):
        try:
            self.db_name = db_name
            self.key_file = key_file
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # Load or generate the encryption key
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as keyfile:
                    self.encryption_key = keyfile.read()
            else:
                self.encryption_key = Fernet.generate_key()
                with open(self.key_file, 'wb') as keyfile:
                    keyfile.write(self.encryption_key)

            self.fernet = Fernet(self.encryption_key)
            self.create_tables()
            print("Successfully connected to the database and initialized encryption.")
        except Exception as e:
            print(f"An Error Occurred during initialization: {e}")

    # Create table for each user 
    def create_tables(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    password_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    website TEXT NOT NULL,
                    password TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                )
            ''')
            self.connect.commit()
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")

    # Encrypt a password
    def encrypt_password(self, plain_text_password):
        try:
            return self.fernet.encrypt(plain_text_password.encode()).decode()
        except Exception as e:
            print(f"Error encrypting password: {e}")
            return None

    # Decrypt a password
    def decrypt_password(self, encrypted_password):
        try:
            return self.fernet.decrypt(encrypted_password.encode()).decode()
        except Exception as e:
            print(f"Error decrypting password: {e}")
            return None

    def ensure_connection(self): # Ensures database connection is active 
      if self.connect is None:
          self.connect = sqlite3.connect(self.db_name)
          self.cursor = self.connect.cursor()
