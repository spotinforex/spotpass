import wx
from Backend import Password  # file containing  the Password class


class PasswordManagerApp(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 400))
        self.password_manager = Password()
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Add buttons for each functionality
        add_btn = wx.Button(panel, label="Add Password")
        find_btn = wx.Button(panel, label="Find Password")
        view_all_btn = wx.Button(panel, label="View All Passwords")
        view_limit_btn = wx.Button(panel, label="View Limited Passwords")
        delete_btn = wx.Button(panel, label="Delete Password")
        exit_btn = wx.Button(panel, label="Exit")

        # Bind buttons to their respective functions
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_password)
        find_btn.Bind(wx.EVT_BUTTON, self.on_find_password)
        view_all_btn.Bind(wx.EVT_BUTTON, self.on_view_all_passwords)
        view_limit_btn.Bind(wx.EVT_BUTTON, self.on_view_limited_passwords)
        delete_btn.Bind(wx.EVT_BUTTON, self.on_delete_password)
        exit_btn.Bind(wx.EVT_BUTTON, self.on_exit)

        # Add buttons to the layout
        for btn in [add_btn, find_btn, view_all_btn, view_limit_btn, delete_btn, exit_btn]:
            vbox.Add(btn, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(vbox)

    def on_add_password(self, event):
        dialog = wx.TextEntryDialog(self, "Enter details as 'ID,Website,Password':", "Add Password")
        if dialog.ShowModal() == wx.ID_OK:
            try:
                input_data = dialog.GetValue().split(",")
                if len(input_data) == 3:
                    add_id, add_website, add_password = input_data
                    self.password_manager.cursor.execute(
                        "INSERT INTO password_manager (id, website, password) VALUES (?, ?, ?)",
                        (int(add_id), add_website.strip(), add_password.strip()),
                    )
                    self.password_manager.connect.commit()
                    wx.MessageBox("Password added successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("Invalid input format. Please use 'ID,Website,Password'.", "Error", wx.OK | wx.ICON_ERROR)
            except Exception as e:
                wx.MessageBox(f"Error adding password: {e}", "Error", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()

    def on_find_password(self, event):
        dialog = wx.TextEntryDialog(self, "Enter ID or Website to search:", "Find Password")
        if dialog.ShowModal() == wx.ID_OK:
            query = dialog.GetValue().strip()
            try:
                self.password_manager.cursor.execute(
                    "SELECT * FROM password_manager WHERE id = ? OR website = ?", (query, query)
                )
                results = self.password_manager.cursor.fetchall()
                if results:
                    wx.MessageBox(f"Records found:\n{results}", "Search Results", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("No records found.", "Search Results", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error finding password: {e}", "Error", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()

    def on_view_all_passwords(self, event):
        try:
            self.password_manager.cursor.execute("SELECT * FROM password_manager")
            results = self.password_manager.cursor.fetchall()
            if results:
                wx.MessageBox(f"Passwords:\n{results}", "All Passwords", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("No passwords found.", "All Passwords", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error viewing passwords: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_view_limited_passwords(self, event):
        dialog = wx.TextEntryDialog(self, "Enter the number of passwords to view:", "View Limited Passwords")
        if dialog.ShowModal() == wx.ID_OK:
            try:
                limit = int(dialog.GetValue().strip())
                self.password_manager.cursor.execute("SELECT * FROM password_manager LIMIT ?", (limit,))
                results = self.password_manager.cursor.fetchall()
                if results:
                    wx.MessageBox(f"First {limit} Password(s):\n{results}", "Limited Passwords", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("No passwords found.", "Limited Passwords", wx.OK | wx.ICON_INFORMATION)
            except ValueError:
                wx.MessageBox("Please enter a valid number.", "Error", wx.OK | wx.ICON_ERROR)
            except Exception as e:
                wx.MessageBox(f"Error viewing passwords: {e}", "Error", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()

    def on_delete_password(self, event):
        dialog = wx.TextEntryDialog(self, "Enter ID of the password to delete:", "Delete Password")
        if dialog.ShowModal() == wx.ID_OK:
            delete_id = dialog.GetValue().strip()
            try:
                self.password_manager.cursor.execute("DELETE FROM password_manager WHERE id = ?", (delete_id,))
                self.password_manager.connect.commit()
                wx.MessageBox("Password deleted successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error deleting password: {e}", "Error", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()

    def on_exit(self, event):
        self.password_manager.close_connection()
        self.Close()


if __name__ == "__main__": # Running the code in a browser 
    app = wx.App(False)
    frame = PasswordManagerApp(None, "Password Manager")
    frame.Show()
    app.MainLoop()
