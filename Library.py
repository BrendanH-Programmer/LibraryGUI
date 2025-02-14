# Import neccessary modules
import tkinter as tk # Import tkinter for GUI development
from tkinter import ttk, messagebox # Import themed Tkinter for styled widgets
import Database  # Module for database operations
import Image  # Module for handling images
import Sound  # Module for playing sounds
import Add  # Module for adding records
import Edit  # Module for editing records
import Remove  # Module for removing records
import Search  # Module for searching records
import L2D  # Module for light and dark mode settings
from L2D import L2D  # Import L2D class for theme settings
import Logout  # Module for logout functionality
from Logout import Logout  # Import Logout class for handling logout
import Speak  # Module for speaking book details
from Speak import SpeakBook  # Import SpeakBook class for text-to-speech
from PIL import Image as PILImage, ImageTk, UnidentifiedImageError  # PIL library for image handling
import io  # Module for handling binary data
from List import listAll  # Module for listing all records
from TTS import TTS  # Module for text-to-speech functionality

class Library:
    def __init__(self, root, cursor):
        """
        Initialize the Library class with the root window and database cursor.
        :param root: The Tkinter root window
        :param cursor: Database cursor for executing SQL queries
        """
        self.root = root
        self.cursor = cursor
        self.current_image_viewer = None  # Keep track of the currently open image viewer

    def create_image_viewer(self, root):
        """
        Create a new image viewer window to display book covers.
        :param root: The Tkinter root window
        :return: The new image viewer window and image label
        """
        global current_image_viewer
        image_viewer_window = tk.Toplevel(root)
        image_viewer_window.title("Book Cover")
        image_viewer_window.geometry("350x350")
        
        image_label = tk.Label(image_viewer_window)
        image_label.pack(expand=True, fill=tk.BOTH)

        def on_viewer_close():
            """
            Handle the image viewer window close event.
            """
            global current_image_viewer
            image_viewer_window.destroy()
            current_image_viewer = None

        image_viewer_window.protocol("WM_DELETE_WINDOW", on_viewer_close)
            
        # Update the current image viewer reference
        current_image_viewer = image_viewer_window
        
        return image_viewer_window, image_label
    
    def update_image_viewer(self, image_label, photo):
        """
        Update the image viewer with the provided photo.
        :param image_label: The label widget in the image viewer
        :param photo: The PhotoImage object to display
        """
        if image_label:
            image_label.config(image=photo)
            image_label.image = photo  # Keep a reference to prevent garbage collection

    def on_book_selected(self, event, tree):
        """
        Handle the event when a book is selected in the Treeview.
        :param event: The event object
        :param tree: The Treeview widget
        """
        global current_image_viewer
        selected_item = tree.selection()
        if not selected_item:
            return

        if self.current_image_viewer:
            self.current_image_viewer.destroy()

        # Create a new image viewer for the selected book
        image_viewer_window, image_label = self.create_image_viewer(self.root)

        book_id = tree.item(selected_item[0], "values")[0]
        image_data = Image.CustomImage.fetch_image_data(self.cursor, book_id)

        # Display the current image for the book
        if image_data:
            photo = Image.CustomImage.binary_to_photoimage(image_data)
            self.update_image_viewer(image_label, photo)
        else:
            self.update_image_viewer(image_label, None)
            
        # Update the current image viewer reference
        self.current_image_viewer = image_viewer_window

    def load_full_book_list(cursor, tree):
        """
        Load the full list of books and display them in the Treeview widget.
        :param cursor: Database cursor for executing SQL queries
        :param tree: The Treeview widget
        """
        cursor.execute("SELECT * FROM tblBooks")
        records = cursor.fetchall()
        for record in tree.get_children():
            tree.delete(record)
        for row in records:
            tree.insert("", tk.END, values=row)

    @staticmethod
    def manage_library():
        """
        Main function to manage the library system. Sets up the GUI and initializes the library management functionalities.
        """
        # Establish database connection
        Library.conn = Database.Database.Connection()
        Library.cursor = Library.conn.cursor()

        # Create the main root window
        root = tk.Tk()
        style = ttk.Style()
        style.theme_use('alt')
        root.title("Library Management")

        # Set up the Treeview widget to display book records
        tree = ttk.Treeview(root, columns=("BookID", "BookName", "Author", "PublishedYear"), show="headings")
        tree.column("BookID", width=100)
        tree.column("BookName", width=350)
        tree.column("Author", width=250)
        tree.column("PublishedYear", width=150)
        tree.heading("BookID", text="Book ID")
        tree.heading("BookName", text="Book Name")
        tree.heading("Author", text="Author")
        tree.heading("PublishedYear", text="Published Year")
        tree.pack(pady=10)

        # Set the initial theme of the GUI
        L2D.set_theme(root, L2D.light_mode_colors)
        is_light_mode = True

        def toggle_mode():
            """
            Toggle between light and dark mode for the GUI.
            """
            nonlocal is_light_mode
            is_light_mode = not is_light_mode
            if is_light_mode:
                L2D.set_theme(root, L2D.dark_mode_colors)
            else:
                L2D.set_theme(root, L2D.light_mode_colors)
        
        # Create a button to toggle between light and dark mode
        toggle_button = ttk.Button(root, text="Toggle Mode", command=toggle_mode)
        toggle_button.pack()

        # Instantiate the library object
        library = Library(root, Library.cursor)

        # Create buttons for various functionalities
        view_records_button = ttk.Button(root, text="View Records", command=lambda: listAll.open_records_window(), style="TButton")
        view_records_button.pack(side=tk.TOP, padx=5, pady=10)

        add_button = ttk.Button(root, text="Add Record", command=lambda: Add.Add.add_record_task(Library.conn, Library.cursor, tree), style="TButton")
        add_button.pack(side=tk.LEFT, padx=5, pady=10)

        delete_button = ttk.Button(root, text="Delete Record", command=lambda: Remove.Delete.delete_record(Library.conn, Library.cursor, tree), style="TButton")
        delete_button.pack(side=tk.LEFT, padx=5, pady=10)

        edit_button = ttk.Button(root, text="Edit Record", command=lambda: Edit.Edit.edit_record(Library.conn, Library.cursor, tree), style="TButton")
        edit_button.pack(side=tk.LEFT, padx=5, pady=10)

        # Create a search frame and search widgets
        search_frame = tk.Frame(root, bg=L2D.light_mode_colors["bg"] if is_light_mode else L2D.dark_mode_colors["bg"])
        search_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=10)

        search_label = ttk.Label(search_frame, text="Search:", background=L2D.light_mode_colors["bg"] if is_light_mode else L2D.dark_mode_colors["bg"], foreground=L2D.light_mode_colors["text"] if is_light_mode else L2D.dark_mode_colors["text"])
        search_label.pack(side=tk.LEFT)

        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        search_button = ttk.Button(search_frame, text="Search", command=lambda: Search.Search.search_books(Library.cursor, search_entry, tree), style="TButton")
        search_button.pack(side=tk.LEFT, padx=5)

        # Create a button to speak book details
        speak_button = ttk.Button(root, text="Speak Book Details", command=lambda: SpeakBook.speak_book_details(Library.cursor, tree), style="TButton")
        speak_button.pack(side=tk.LEFT, padx=5, pady=10)

        tts = TTS()

        # Create a logout button
        logout_button = ttk.Button(root, text="Logout", command=lambda: Logout.logout(root, tts))
        logout_button.pack(pady=10)

        # Bind the Treeview select event to display book cover
        tree.bind("<ButtonRelease-1>", lambda event: library.on_book_selected(event, tree))

        # Bind the on_closing function to the window close event
        root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, tts))

        # Load the full book list into the Treeview
        Library.load_full_book_list(Library.cursor, tree)

        # Set the initial theme mode
        toggle_mode()
        root.mainloop()

    @staticmethod
    def view_records(tree):
        """
        View the records of books in the Treeview.
        :param tree: The Treeview widget
        """
        Sound.Sound.play_click_sound()
        Library.cursor.execute("SELECT * FROM tblBooks")
        records = Library.cursor.fetchall()
        for record in tree.get_children():
            tree.delete(record)
        for row in records:
            tree.insert("", tk.END, values=row)

def on_closing(root, tts):
    """
    Handle the event when the main window is closed.
    :param root: The Tkinter root window
    :param tts: The Text-to-Speech (TTS) instance
    """
    Logout.logout(root, tts)
