from database import Password

manager = Password('password_manager.db')  # Instantiating the Password manager class

class Backend:
    def __init__(self):
        print('Backend class initialized.')
        self.user_id = None  # To store logged-in user ID

    def create_account(self):
        try:
            manager.ensure_connection() # optionally ensures that connect is active.  
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email: ").strip()
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            encrypted_password = manager.encrypt_password(password)

            query = '''INSERT INTO users (first_name, last_name, email, username, password)
                       VALUES (?, ?, ?, ?, ?)'''
            manager.cursor.execute(query, (first_name, last_name, email, username, encrypted_password))
            manager.connect.commit()
            print("Account created successfully.")
            self.login()  # Optionally prompt the user to log in immediately
        except Exception as e:
            print(f"Error creating account: {e}")

    def login(self):
        try:
            manager.ensure_connection()
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            query = '''SELECT user_id, password FROM users WHERE username = ?'''
            manager.cursor.execute(query, (username,))
            user = manager.cursor.fetchone()

            if user:
                user_id, encrypted_password = user
                decrypted_password = manager.decrypt_password(encrypted_password)
                if decrypted_password == password:
                    self.user_id = user_id  # Store the logged-in user's ID
                    print("Login successful!")
                    
                else:
                    print("Invalid password.")
            else:
                print("Invalid username.")
        except Exception as e:
            print (f'An error occurred as {e}')

    def add_password(self):
        try:
            manager.ensure_connection()
            if not self.user_id: # Ensure that password adding cannot be acccessed without a login
                print("Please log in to add a password.")
                return

            website = input("Website: ").strip()
            password = input("Password: ").strip()
            encrypted_password = manager.encrypt_password(password)

            query = '''INSERT INTO passwords (user_id, website, password) VALUES (?, ?, ?)'''
            manager.cursor.execute(query, (self.user_id, website, encrypted_password))
            manager.connect.commit()
            print("Password added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def find_password(self):
        try:
            manager.ensure_connection()
            if not self.user_id:
                print("Please log in to find a password.")
                return

            find_password_website = input('Please input Website (leave blank if not available): ').strip()
            
            if find_password_website:
                query = '''SELECT website, password FROM passwords WHERE website = ? AND user_id = ?'''
                manager.cursor.execute(query, (find_password_website, self.user_id))
            else:
                print("No input provided. Please enter either ID or Website.")
                return

            records = manager.cursor.fetchall()

            if records: # statements checks if passwords are found 
                for website, encrypted_password in records:
                    decrypted_password = manager.decrypt_password(encrypted_password)
                    print(f"Website: {website}\nPassword: {decrypted_password}")
            else:
                print("No records found.")
        except Exception as e:
            print(f"Error finding password: {e}")
    def update_password(self):
        try:
        # Ensure the database connection is active
          manager.ensure_connection()

          if not hasattr(self, 'user_id') or not self.user_id:
              print("Please log in to update a password.")
              return

        # Gather inputs
          website = input("Website: ").strip()
          updated_password = input("Please type in the updated password: ").strip()

        # Validate inputs
          if not website:
              print("Please input a website to update.")
              return
          if not updated_password:
              print("Please input the updated password.")
              return

        # Encrypt the new password
          encrypted_password = manager.encrypt_password(updated_password)

        # Execute the update query
          query = '''UPDATE passwords SET password = ? WHERE website = ? AND user_id = ?'''
          manager.cursor.execute(query, (encrypted_password, website, self.user_id))
          manager.connect.commit()

        # Check if the update affected any rows
          if manager.cursor.rowcount > 0:
              print("Password updated successfully.")
          else:
              print("No record found for this website under your account.")
        except Exception as e:
            print(f"Error Updating password: {e}")
    
    def view_password(self):
     try:
        # Ensure a logged-in user
          if not hasattr(self, 'user_id') or not self.user_id:
              print("Please log in to view your saved passwords.")
              return

        # Fetch passwords for the logged-in user
          query = '''SELECT website, password FROM passwords WHERE user_id = ?'''
          manager.cursor.execute(query, (self.user_id,))
          rows = manager.cursor.fetchall()

        # Display results if any are found
          if rows:
              print("Your saved passwords:")
              for website, encrypted_password in rows:
                  decrypted_password = manager.decrypt_password(encrypted_password)
                  print(f"Website: {website} | Password: {decrypted_password}")
          else:
              print("No saved passwords found for your account.")
     except Exception as e:
          print(f"Error Veiwing password: {e}")
    
    def delete_password(self):
     try:
          # Ensure a logged-in user
          if not hasattr(self, 'user_id') or not self.user_id:
              print("Please log in to delete a password.")
              return

          # Input for website or password ID
          website = input("Please input the website of the password to delete: ").strip()

          if not website:
              print("Website cannot be empty.")
              return

          # Query to delete the password
          query = '''DELETE FROM passwords WHERE user_id = ? AND website = ?'''
          manager.cursor.execute(query, (self.user_id, website))
          manager.connect.commit()

          # Feedback based on rows affected
          if manager.cursor.rowcount > 0:
              print("Password deleted successfully.")
          else:
              print("No matching record found.")
     except Exception as e:
          print(f"Error deleting password: {e}")
    
    def close_connection(self): # closes and logs the user out of the database
        try:
          if not hasattr(self, 'user_id') or not self.user_id:
                print("Please log in to delete a password.")
                return 
          manager.cursor.close()
          manager.connect.close()
          print("Database connection closed.")
        except Exception as e:
            print(f"Error closing database: {e}")
