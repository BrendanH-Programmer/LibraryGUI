# Import neccessary modules
import tkinter as tk # Import tkinter for GUI development
from Login import Login  # Import the Login class for user authentication
from CreateLogin import UserRegistrationApp  # Import the UserRegistrationApp class for user registration
from Library import Library  # Import the Library class for managing the library interface

def login_and_load_library():
    """
    Function to handle user authentication and library loading.
    """
    # Create an instance of the Login class
    login_instance = Login()
    
    # Display the login GUI and authenticate user credentials
    success = login_instance.login_gui()
    
    # If login is successful
    if success:
        # Create an instance of the Library class
        library_instance = Library()
        
        # Load and manage the library interface
        library_instance.manage_library()

# Call the function to handle login and library loading
login_and_load_library()
