# Import neccessary modules
import pyttsx3 # Import pyttsx3 for text-to-speech functionality
import threading # Import threading for concurrent execution of tasks
from tkinter import messagebox # Import messagebox from tkinter for displaying messages

class TTS:
    def __init__(self):
        """
        Initializes the text-to-speech (TTS) engine with default properties
        and sets up necessary flags and locks.
        """
        self.engine = pyttsx3.init()  # Initialize the TTS engine
        self.engine.setProperty("rate", 120)  # Set the speech rate to 120 words per minute
        self.is_running = False  # Flag to track if the TTS engine is currently running
        self.lock = threading.Lock()  # Lock to manage concurrent access to the TTS engine
        self.logout_requested = False  # Flag to indicate if logout has been requested

    def set_logout_requested(self):
        """
        Sets the logout_requested flag to True.
        """
        self.logout_requested = True

    def clear_logout_requested(self):
        """
        Clears the logout_requested flag, setting it to False.
        """
        self.logout_requested = False

    def update_is_running(self):
        """
        Updates the is_running flag based on the TTS engine's busy status.
        """
        self.is_running = self.engine.isBusy()

    def _speak(self, text):
        """
        Internal method to perform the actual speaking operation.
        :param text: Text to be spoken by the TTS engine
        :return: An error message if an error occurs, otherwise None
        """
        error_message = None  # Variable to store any error message
        with self.lock:
            self.is_running = True
            self.engine.say(text)  # Queue the text to be spoken
            try:
                self.engine.runAndWait()  # Process the queued commands and wait until speaking is finished
            except RuntimeError as e:
                # Store the error message if a RuntimeError occurs
                error_message = f"Error: {e}"
            finally:
                # Ensure that the logout_requested flag is cleared even if an exception occurs
                if self.logout_requested:
                    self.clear_logout_requested()
            self.is_running = False
        return error_message  # Return the error message (if any)

    def stop_speaking(self):
        """
        Stops the TTS engine from speaking and ensures the is_running flag is set to False.
        """
        with self.lock:
            self.engine.stop()  # Stop the TTS engine
            self.is_running = False  # Ensure the is_running flag is set to False

    def speak_text(self, text):
        """
        Speaks the given text using the TTS engine. If the engine is already speaking, 
        displays an informational message to the user.
        :param text: Text to be spoken by the TTS engine
        """
        if self.is_running:
            # If the TTS engine is currently speaking, show an informational message
            messagebox.showinfo("", "I am currently speaking. Please wait.")
        else:
            # Start a new thread to speak the text, allowing it to run in the background
            threading.Thread(target=self._speak, args=(text,), daemon=True).start()