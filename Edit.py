# Import necessary modules for GUI, sound, image processing, and database interactions
from tkinter import simpledialog, messagebox, filedialog # Tkinter dialog boxes
import Sound  # Custom module for sound effects
import Library  # Custom module for library operations
import datetime  # For handling date and time
import Image  # For image processing
from Image import CustomImage  # Custom class for image handling

class Edit:
    @staticmethod
    def edit_record(conn, cursor, tree):
        """
        Edit a selected book record from the treeview widget. This includes updating the book's name,
        author, published year, and associated image.
        :param conn: SQLite database connection object
        :param cursor: SQLite database cursor object
        :param tree: Tkinter treeview widget displaying the list of books
        """
        # Play a click sound when the edit button is clicked
        Sound.Sound.play_click_sound()
        
        # Get the selected item from the treeview
        selection = tree.selection()
        if selection:
            item = selection[0]

            # Extract the values of the selected book's details
            values = tree.item(item, "values")
            if len(values) == 5:
                BookID, current_name, current_author, current_year, current_image_data = values
            else:
                # Display an error message if the number of values is incorrect
                messagebox.showerror("Value Error", "Incorrect number of values in the tree.")
                return

            # Ask for the new book name, pre-fill with current name
            new_name = simpledialog.askstring("Edit Book", "Enter new book name:", initialvalue=current_name)
            if new_name is None:
                return

            # Check if the new name is different from the current name
            if new_name != current_name:
                while True:
                    # Check if the new book name already exists in the database
                    cursor.execute("SELECT BookID FROM tblBooks WHERE BookName = ?", (new_name,))
                    existing_book = cursor.fetchone()
                    if existing_book:
                        # Display a warning if a book with the same name already exists
                        messagebox.showwarning("Input Error", "A book with the same name already exists. Please choose a different name.")
                        new_name = simpledialog.askstring("Edit Book", "Enter new book name:", initialvalue=current_name)
                        if new_name is None:
                            return
                    else:
                        break

            # Ask for the new author when editing a book, pre-fill with current author
            new_author = simpledialog.askstring("Edit Book", "Enter new author name:", initialvalue=current_author)
            if new_author is None:
                return

            # Ask for the new published year, pre-fill with current year
            new_year = simpledialog.askstring("Edit Book", "Enter new published year:", initialvalue=current_year)
            if new_year is None:
                return

            # Validate the new published year
            current_year = datetime.datetime.now().year
            while True:
                if not new_year.isdigit() or len(new_year) != 4:
                    # Display a warning if the year is not a 4-digit number
                    messagebox.showwarning("Input Error", "Published Year must be a 4-digit number.")
                    new_year = simpledialog.askstring("Edit Book", "Enter new published year:", initialvalue=current_year)
                    if new_year is None:
                        return
                else:
                    year_int = int(new_year)
                    if not (0 <= year_int <= current_year):
                        # Display a warning if the year is not within the valid range
                        messagebox.showwarning("Input Error", f"Published Year must be between 0000 and {current_year}.")
                        new_year = simpledialog.askstring("Edit Book", "Enter new published year:", initialvalue=current_year)
                        if new_year is None:
                            return
                    else:
                        break

            # Fetch the current image data from the database
            cursor.execute("SELECT Image FROM tblBooks WHERE BookID = ?", (BookID,))
            result = cursor.fetchone()
            if result:
                current_image_data = result[0]
            else:
                current_image_data = None

            # Ask the user to select a new image file (optional)
            new_file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
            new_image_data = None
            if new_file_path:
                # Load the new image data
                new_image_data = CustomImage.load_image(new_file_path)

            try:
                # Update the database with new details
                cursor.execute('''
                    UPDATE tblBooks
                    SET BookName = ?, Author = ?, PublishedYear = ?, Image = ?
                    WHERE BookID = ?
                ''', (new_name, new_author, new_year, new_image_data or current_image_data, BookID))
                # Save the changes to the database
                conn.commit()
                # Display a success message
                messagebox.showinfo("Success", "Record updated successfully!")
            except Exception as e:
                # Display an error message if the update was unsuccessful
                messagebox.showerror("Database Error", f"Error updating record: {e}")
        else:
            # Display a warning if no book has been selected for editing
            messagebox.showwarning("Selection Error", "No record selected.")

        # After the edit operation is complete, update the list of books
        Library.Library.load_full_book_list(cursor, tree)
