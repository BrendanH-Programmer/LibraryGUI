# Import neccessary modules
from tkinter import messagebox # Import messagebox from tkinter for displaying messages
import Sound # Import Sound module for handling sound-related functionalities
import Library # Import Library module for managing the library interface

class Delete:
    @staticmethod
    def delete_record(conn, cursor, tree):
        """
        Delete a selected book record from the database and the treeview.
        :param conn: SQLite database connection object.
        :param cursor: Database cursor for executing SQL queries.
        :param tree: Treeview widget containing the list of books.
        """
        # Play a click sound when the delete button is clicked
        Sound.Sound.play_click_sound()
        
        # Get the selected item from the treeview
        selection = tree.selection()
        
        # Check if an item is selected
        if selection:
            # Ask for confirmation before deletion
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
            
            # If user confirms deletion
            if confirm:
                # Get the selected item and its BookID
                item = selection[0]
                BookID = tree.item(item, "values")[0]
                
                # Execute SQL command to delete the record from the database
                cursor.execute('DELETE FROM tblBooks WHERE BookID = ?', (BookID,))
                conn.commit()
                
                # Delete the selected item from the treeview
                tree.delete(item)
        else:
            # Display a warning message if no book was selected for deletion
            messagebox.showwarning("Selection Error", "No record selected.")
        
        # Update the list of books in the library after the deletion
        Library.Library.load_full_book_list(cursor, tree)
