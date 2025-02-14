# Import neccessary modules
import Sound  # Import the Sound module for playing click sound
import Login  # Import the Login module for user authentication
import tkinter as tk # Import tkinter for GUI development
from tkinter import messagebox # Import messagebox for displaying messages
import TTS  # Import the TTS module for text-to-speech functionality

tts = TTS.TTS()  # Initialize the TTS engine

class Logout:
    @staticmethod
    def logout(root, tts):
        """
        Log out the user and close the application window.
        :param root: Tkinter root window.
        :param tts: TTS object for handling text-to-speech functionality.
        """
        # Check if TTS engine is currently speaking
        if tts.is_running:
            # Notify the user that logout cannot be performed while speaking
            messagebox.showinfo("Logout Error", "Cannot log out while speaking. Please wait.")
        else:
            # Play a click sound when the logout button is clicked
            Sound.Sound.play_click_sound()
            
            # Stop TTS speech before logging out
            tts.stop_speaking()
            
            # Speak a logout message
            tts.speak_text("Logged out successfully")
            
            # Destroy the application window
            root.destroy()
            
            # Open the login GUI after successful logout
            Login.Login.login_gui()

def on_closing(root, tts):
    """
    Callback function to handle window closing event.
    :param root: Tkinter root window.
    :param tts: TTS object for handling text-to-speech functionality.
    """
    # Call the logout function to perform logout and window closing operations
    Logout.logout(root, tts)
