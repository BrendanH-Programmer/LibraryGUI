# Import necessary modules
import tkinter as tk  # Tkinter for GUI
from tkinter import simpledialog, messagebox, filedialog  # Tkinter dialog boxes
import Library  # Module for library management
import Sound  # Module for playing sounds
import datetime  # Module for handling date and time
import Image  # Module for handling images
from Image import CustomImage  # Custom image handling from the Image module
from PIL import Image, ImageTk, UnidentifiedImageError  # PIL library for image handling and conversion

class Add:
    @staticmethod
    def add_record_task(conn, cursor, tree):
        # Play click sound when the method is invoked
        Sound.Sound.play_click_sound()
        
        while True:
            # Prompt user to enter the book name
            BookName = simpledialog.askstring("Input", "Enter Book name:")
            
            if BookName is None:
                # If the user cancels the dialog, exit the loop
                break
            elif not BookName.strip():
                # If the input is empty, display a warning message
                messagebox.showwarning("Input Error", "Book name is required.")
            else:
                # Check if the book already exists in the database
                cursor.execute("SELECT COUNT(*) FROM tblBooks WHERE BookName = ?", (BookName,))
                count = cursor.fetchone()[0]
                if count > 0:
                    # If a book with the same name exists, display a warning message
                    messagebox.showwarning("Duplicate Book", "A book with this name already exists.")
                else:
                    # If the input is valid and no duplicate is found, exit the loop
                    break 

        if BookName is not None:
            while True:
                # Prompt user to enter the author's name
                Author = simpledialog.askstring("Input", "Enter Author name:")
                
                if Author is None:
                    # If the user cancels the dialog, exit the loop
                    break
                elif not Author.strip():
                    # If the input is empty, display a warning message
                    messagebox.showwarning("Input Error", "Author name is required.")
                else:
                    # If the input is valid, exit the loop
                    break

            if Author is not None:
                # Get the current year to validate the published year
                current_year = datetime.datetime.now().year

                while True:
                    # Prompt user to enter the published year
                    PublishedYear = simpledialog.askstring("Input", "Enter Published Year (4-digit format):")

                    if PublishedYear is None:
                        # If the user cancels the dialog, exit the loop
                        break

                    if not PublishedYear:
                        # If the input is empty, display a warning message
                        messagebox.showwarning("Input Error", "Published Year is required.")
                    elif not PublishedYear.isdigit() or len(PublishedYear) != 4:
                        # If the input is not a 4-digit number, display a warning message
                        messagebox.showwarning("Input Error", "Published Year must be a 4-digit number.")
                    elif not 0 <= int(PublishedYear) <= current_year:
                        # If the input is not within the valid range, display a warning message
                        messagebox.showwarning("Input Error", f"Published Year must be between 0000 and {current_year}.")
                    else:
                        # If the input is valid, exit the loop
                        break

                if PublishedYear is not None:
                    # Open a file dialog to select an image file
                    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
                    if not file_path:
                        # If no file is selected or dialog is canceled, display a warning message
                        messagebox.showwarning("Input Error", "Please select an image file.")
                        return
                    
                    # Load the selected image file
                    image_data = CustomImage.load_image(file_path)
                    if not image_data:
                        # If there's an error loading the image, display an error message
                        messagebox.showerror("Image Error", "Error reading image file.")
                        return

                    try:
                        # Insert the new book record into the database
                        cursor.execute('''
                            INSERT INTO tblBooks (BookName, Author, PublishedYear, Image)
                            VALUES (?, ?, ?, ?)
                        ''', (BookName, Author, PublishedYear, image_data))
                        # Commit the transaction to save changes
                        conn.commit()

                        # Retrieve the ID of the newly inserted book
                        BookID = cursor.lastrowid

                        # Insert the new book into the treeview widget for display
                        tree.insert("", tk.END, values=(BookID, BookName, Author, PublishedYear))

                        # Display a success message
                        messagebox.showinfo("Success", "Book added successfully!")
                    except Exception as e:
                        # If there's an error inserting the record, display an error message
                        messagebox.showerror("Database Error", f"Error adding record to the database: {e}")
    
        # After adding the new book, update the list of books in the UI
        Library.Library.load_full_book_list(cursor, tree)
