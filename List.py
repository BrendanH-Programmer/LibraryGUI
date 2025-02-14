# Import necessary modules
import tkinter as tk # Import tkinter for GUI development
from tkinter import ttk # Import themed Tkinter for styled widgets
import sqlite3 # Import sqlite3 for SQLite database operations
import Sound # Import Sound module for playing sounds

class listAll:
    # Class-level variable to track if the window is open
    is_window_open = False
    ascending_order = True  # Indicates whether the records are sorted in ascending or descending order
    
    @classmethod
    def open_records_window(cls, sort_by="BookName"):
        """Open a window to display all books in the library."""
        if not cls.is_window_open:  # Check if the window is already open
            cls.is_window_open = True
            # Plays click noise when pressed
            Sound.Sound.play_click_sound()  # Play a sound effect indicating a button click

            # Establish a new SQLite connection and cursor
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()

            # Create a new Toplevel window for displaying records
            records_window = tk.Toplevel()
            records_window.title("All Books")
            records_window.geometry("850x400")

            # Create a Treeview widget to display records
            record_tree = ttk.Treeview(records_window, columns=("BookID", "BookName", "Author", "PublishedYear"), show="headings")
            record_tree.column("BookID", width=100)
            record_tree.column("BookName", width=350)
            record_tree.column("Author", width=250)
            record_tree.column("PublishedYear", width=150)
            
            # Set headings for columns and define sorting command for each heading
            record_tree.heading("BookID", text="Book ID", command=lambda: cls.sort_records(cursor, record_tree, "BookID"))
            record_tree.heading("BookName", text="Book Name", command=lambda: cls.sort_records(cursor, record_tree, "BookName"))
            record_tree.heading("Author", text="Author", command=lambda: cls.sort_records(cursor, record_tree, "Author"))
            record_tree.heading("PublishedYear", text="Published Year", command=lambda: cls.sort_records(cursor, record_tree, "PublishedYear"))
            record_tree.pack(expand=True, fill=tk.BOTH)

            # Bring list of books by specified column in specified order
            cls.sort_records(cursor, record_tree, sort_by)

            # Close the database connection when the window is closed
            def on_window_close():
                nonlocal conn
                conn.close()  # Close the SQLite connection
                records_window.destroy()  # Destroy the window
                cls.is_window_open = False  # Update the class variable to indicate window closure

            records_window.protocol("WM_DELETE_WINDOW", on_window_close)  # Call on_window_close when window is closed

    @classmethod
    def sort_records(cls, cursor, record_tree, column):
        """Sort records in the treeview widget based on the specified column."""
        cls.ascending_order = not cls.ascending_order  # Toggle sorting order
        sort_order = "ASC" if cls.ascending_order else "DESC"  # Determine sort order based on toggle
        # SQL query to fetch records sorted by the specified column
        query = f'SELECT BookID, BookName, Author, PublishedYear FROM tblBooks ORDER BY {column} {sort_order}'
        cursor.execute(query)
        rows = cursor.fetchall()
        # Clear existing records in the treeview
        for row in record_tree.get_children():
            record_tree.delete(row)
        # Insert sorted records into the treeview
        for row in rows:
            record_tree.insert("", tk.END, values=row)