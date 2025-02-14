# Import neccessary modules
import Sound  # Import the Sound module for playing click sound
import tkinter as tk # Import tkinter for GUI development
from tkinter import messagebox # Import messagebox for displaying messages

class Search:
    @staticmethod
    def search_books(cursor, search_entry, tree):
        """
        Search for books based on the provided query and display the results in the treeview.
        :param cursor: Database cursor for executing SQL queries.
        :param search_entry: Entry widget containing the search query.
        :param tree: Treeview widget for displaying search results.
        """
        # Play a click sound when the search button is clicked
        Sound.Sound.play_click_sound()
        
        # Get the search query from the search entry
        query = search_entry.get()
        
        # If the query is empty, fetch all records
        if not query:
            # Show a message to the user asking for a search query
            messagebox.showinfo("Search Query", "Please enter a search query.")
            # Set the query to an empty string to fetch all records
            query = ""
        else:
            # Clear the existing items in the treeview to display new search results
            for item in tree.get_children():
                tree.delete(item)

        # Fetch records that match the search query from the database
        cursor.execute('''
            SELECT * FROM tblBooks
            WHERE BookName LIKE ? OR Author LIKE ? OR PublishedYear LIKE ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        # Fetch all rows that match the search criteria
        rows = cursor.fetchall()
        
        # Insert the matching rows into the treeview for display
        for row in rows:
            tree.insert("", tk.END, values=row)