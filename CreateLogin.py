# Import necessary modules
import tkinter as tk # Tkinter for GUI
from tkinter import ttk, messagebox  # ttk for themed widgets, messagebox for dialog boxes
import sqlite3  # SQLite for database management
import hashlib  # hashlib for hashing passwords
import Library  # Import Library module for opening library management interface (assumed to be a custom module)

class UserRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Registration")  # Set the window title
        self.successful_login = False  # Flag to track successful login
        
        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()

        # Create the user interface
        self.create_widgets()
        
        # Bind the closing function to the window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.closing)

    def create_widgets(self):
        # Create labels and entries for the username
        self.username_label = ttk.Label(self.root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)  # Position the label
        
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)  # Position the entry field

        # Create labels and entries for the password
        self.password_label = ttk.Label(self.root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)  # Position the label
        
        self.password_entry = ttk.Entry(self.root, show="*")  # Hide password input
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)  # Position the entry field

        # Create a register button
        self.register_button = ttk.Button(self.root, text="Register", command=self.create_user)
        self.register_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)  # Position the button

    def create_user(self):
        # Retrieve user input
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            # Insert the user into the database
            self.cursor.execute('''
                INSERT INTO tblLogin (username, password)
                VALUES (?, ?)
            ''', (username, hashed_password))
            self.conn.commit()  # Commit the transaction
            # Show a success message
            messagebox.showinfo("Success", f"User '{username}' registered successfully!")
            self.successful_login = True  # Set successful login flag
            self.root.destroy()  # Close the window after registration
        except sqlite3.IntegrityError:
            # If the username is already taken, show an error message
            messagebox.showerror("Error", f"Username '{username}' is already taken!")

    def closing(self):
        # Close the database connection when the window is closed
        self.conn.close()
        self.root.destroy()

# Create a Tkinter window and run the application
if __name__ == "__main__":
    root = tk.Tk()  # Initialize the main window
    app = UserRegistrationApp(root)  # Create an instance of the application
    root.mainloop()  # Run the Tkinter event loop
