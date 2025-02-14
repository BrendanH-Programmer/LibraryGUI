# Import neccessary modules
import tkinter as tk # Import tkinter for GUI development
from tkinter import ttk, messagebox # Import themed Tkinter for styled widgets and messagebox for displaying messages
from hashlib import sha256 # Import hashlib for cryptographic hashing
import TTS  # Import TTS module for text-to-speech functionality
from TTS import TTS  # Import TTS class for TTS functionality
import Database  # Import Database module for database operations
import threading # Import threading for concurrent execution of tasks
import Library  # Import Library module for managing library interface
from CreateLogin import UserRegistrationApp  # Import UserRegistrationApp from CreateLogin.py

tts = TTS()  # Initialize TTS engine

class Speak:
    """
    Class for handling speech messages.
    """
    @staticmethod
    def success_message():
        """
        Speak a success message.
        """
        success_message = "Logged in successfully!" 
        tts.speak_text(success_message)

    @staticmethod
    def error_message():
        """
        Speak an error message.
        """
        error_message = "Invalid username or password"    
        tts.speak_text(error_message)     
        
                             
class Login:
    """
    Class for user authentication and login GUI.
    """
    @staticmethod
    def attempt_login(conn, username, password):
        """
        Attempt user login by validating username and password.
        :param conn: SQLite database connection object.
        :param username: Username entered by the user.
        :param password: Password entered by the user.
        :return: True if login is successful, False otherwise.
        """
        hashed_password = sha256(password.encode()).hexdigest()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM tblLogin WHERE username = ? AND password = ?", (username, hashed_password))
            user = cursor.fetchone()
            return user is not None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def login(username_var, password_var, root):
        """
        Perform user login.
        :param username_var: Tkinter StringVar object containing username.
        :param password_var: Tkinter StringVar object containing password.
        :param root: Tkinter root window object.
        """
        conn = Database.Database.Connection()
        
        try:
            if Login.attempt_login(conn, username_var.get(), password_var.get()):
                # Define a function to handle successful login and speak a success message
                def handle_success():
                    Speak.success_message()
                
                # Create a thread to handle the success message and start the thread
                success_thread = threading.Thread(target=handle_success)
                success_thread.start()
                
                # Show a success message and destroy the login window
                messagebox.showinfo("Success", "Logged in successfully!")
                root.destroy()
                
                # Open the library management interface after successful login
                Library.Library.manage_library()
            else:
                # Define a function to handle login error and speak an error message
                def handle_error(msg):
                    tts.speak_text(msg)

                # Create a thread to handle the error message and start the thread
                error_thread = threading.Thread(target=handle_error, args=("Invalid username or password",))
                error_thread.start()
                
                # Show an error message for invalid login credentials
                messagebox.showerror("Login Failed", "Invalid username or password")
        except Exception as e:
            # Show an error message if an exception occurs during login process
            error_message = f"An error occurred: {e}"
            messagebox.showerror("Error", error_message)
        finally:
            # Close the database connection
            conn.close()

    @staticmethod
    def open_registration_window():
        """
        Open the user registration window.
        """
        root = tk.Tk()
        registration_app = UserRegistrationApp(root)
        root.mainloop()

    @staticmethod
    def login_gui():
        """
        Display the login GUI.
        """
        root = tk.Tk()
        root.title("Login")
        root.geometry("300x200")

        username_var = tk.StringVar()
        password_var = tk.StringVar()

        lbl_user = ttk.Label(root, text="Username:")
        ent_user = ttk.Entry(root, textvariable=username_var)
        lbl_user.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ent_user.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        lbl_pass = ttk.Label(root, text="Password:")
        ent_pass = ttk.Entry(root, textvariable=password_var, show='*')
        lbl_pass.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        ent_pass.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        btn_login = ttk.Button(root, text="Login", command=lambda: Login.login(username_var, password_var, root))
        btn_login.grid(row=2, column=0, columnspan=2, pady=10)

        btn_create_user = ttk.Button(root, text="Create User", command=Login.open_registration_window)
        btn_create_user.grid(row=3, column=0, columnspan=2, pady=10)

        root.grid_columnconfigure(1, weight=1)
        root.mainloop()

if __name__ == "__main__":
    Login.login_gui()
