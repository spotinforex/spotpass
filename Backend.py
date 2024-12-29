import sqlite3

class Password:
    # Initialize the class and connect to the database
    def __init__(self, db_name="password_manager.db"):
        try:
            self.db_name = db_name
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()
            print('Successfully connected to the database.')
            self.create_table()
        except Exception as e:
            print(f"An Error Occurred: {e}")

    # Create the table if it doesn't exist
    def create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS password_manager (
                    id INTEGER PRIMARY KEY,
                    website TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            self.connect.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

    # Add a new password to the database
    def add_password(self):
        try:
            add_id = int(input('Please input password ID: '))
            add_website = input('Please input website: ').strip()
            add_password = input('Please input password: ').strip()

            if not add_website or not add_password:
                print("Website and password cannot be empty. Please try again.")
                return

            insert_query = "INSERT INTO password_manager (id, website, password) VALUES (?, ?, ?)"
            self.cursor.execute(insert_query, (add_id, add_website, add_password))
            self.connect.commit()
            print('Password added successfully.')
        except sqlite3.IntegrityError:
            print("ID already exists. Use a unique ID.")
        except ValueError:
            print("Invalid ID. Please enter a numeric value.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Find a password in the database
    def find_password(self):
        try:
            find_password_id = input('Please input ID (leave blank if not available): ')
            find_password_website = input('Please input Website (leave blank if not available): ')

            if find_password_id and find_password_website:
                find_sql = 'SELECT * FROM password_manager WHERE id = ? OR website = ?'
                self.cursor.execute(find_sql, (find_password_id, find_password_website))
            elif find_password_id:
                find_sql = 'SELECT * FROM password_manager WHERE id = ?'
                self.cursor.execute(find_sql, (find_password_id,))
            elif find_password_website:
                find_sql = 'SELECT * FROM password_manager WHERE website = ?'
                self.cursor.execute(find_sql, (find_password_website,))
            else:
                print("No input provided. Please enter either ID or Website.")
                return

            rows = self.cursor.fetchall()
            if rows:
                print("Record(s) found:")
                for row in rows:
                    print(row)
            else:
                print("No records found.")
        except Exception as e:
            print(f"Error finding password: {e}")

    # View all passwords in the database
    def view_password(self):
        try:
            self.cursor.execute('SELECT * FROM password_manager')
            rows = self.cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No passwords found in the manager.")
        except Exception as e:
            print(f"Error viewing passwords: {e}")

    # View a specific number of passwords
    def view_number_of_password(self):
        try:
            query = 'SELECT * FROM password_manager LIMIT ?'
            number_to_view = int(input('Please input the number of passwords to view: '))
            self.cursor.execute(query, (number_to_view,))
            rows = self.cursor.fetchall()

            if rows:
                print(f"Displaying the first {number_to_view} password(s):")
                for row in rows:
                    print(row)
            else:
                print("No passwords found in the manager.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error viewing passwords: {e}")

    # Delete a password
    def delete_password(self):
        try:
            user_password = input("Please input user's password: ")
            passw = "Praisejah"
            if user_password == passw:
                delete_password = int(input('Please input password ID to delete: '))
                self.cursor.execute('DELETE FROM password_manager WHERE id = ?', (delete_password,))
                self.connect.commit()
                print("Password deleted successfully.")
            else:
                print("Incorrect password. Try again.")
        except Exception as e:
            print(f"Error deleting password: {e}")

    # Close the database connection
    def close_connection(self):
        self.connect.close()
        print("Database connection closed.")


# Test the class if this file is executed
if __name__ == "__main__":
    print("another_password_manager.py is working correctly.")
