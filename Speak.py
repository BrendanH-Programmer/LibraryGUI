# Import neccessary modules
from tkinter import messagebox # Import messagebox from tkinter for displaying messages
import Sound # Import Sound module for handling sound-related functionalities
import TTS # Import TTS module for text-to-speech functionality
import Library # Import Library module for managing the library interface

# Initialize the TTS engine
tts = TTS.TTS()

class SpeakBook:
    @staticmethod
    def speak_book_details(cursor, tree):
        """
        Speak the details of the selected book using the TTS engine.
        :param cursor: Database cursor to execute SQL queries.
        :param tree: Treeview widget containing the list of books.
        """
        # Play a click sound when the speak button is clicked
        Sound.Sound.play_click_sound()
        
        # Get the selected item from the treeview
        selected_item = tree.selection()
        if not selected_item:
            # Display a warning message if no book has been selected
            messagebox.showwarning("Selection Error", "No book selected.")
            return
        
        # Extract the first selected item
        item = selected_item[0]
        # Get the values (columns) associated with the selected item
        values = tree.item(item, "values")
        
        # Check if values are present
        if values:
            # Extract the book details
            book_name = values[1]  # Book Name
            author = values[2]     # Author
            published_year = values[3]  # Published Year

            # Speak the book details using the TTS engine
            tts.speak_text(f"Book Name: {book_name}, Author: {author}, Published in: {published_year}")