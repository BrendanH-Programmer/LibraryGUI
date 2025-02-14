# Import necessary modules for image handling
from PIL import Image, ImageTk, UnidentifiedImageError  # PIL library for image handling, conversion, and error handling
import io  # For handling binary data and in-memory streams
from tkinter import messagebox  # For displaying error messages in the GUI

class CustomImage:
    @staticmethod
    def fetch_image_data(cursor, book_id):
        """
        Fetches the binary image data for a given book from the database.
        :param cursor: SQLite database cursor object
        :param book_id: ID of the book whose image data is to be fetched
        :return: Binary image data or None if not found
        """
        # Execute SQL query to fetch image data for the given book ID
        cursor.execute("SELECT Image FROM tblBooks WHERE BookID = ?", (book_id,))
        result = cursor.fetchone()
        return result[0] if result else None  # Return image data if found, else None

    @staticmethod
    def binary_to_photoimage(binary_data):
        """
        Converts binary image data to a PhotoImage object for display in Tkinter.
        :param binary_data: Binary data of the image
        :return: PhotoImage object or None if conversion fails
        """
        if binary_data:
            try:
                # Convert binary data to a BytesIO stream
                image_data = io.BytesIO(binary_data)
                # Open the image from the stream
                img = Image.open(image_data)
                # Convert the image to a PhotoImage object
                return ImageTk.PhotoImage(img)
            except UnidentifiedImageError:
                # Display an error message if the image format is not recognized
                messagebox.showerror("Image Error", "Unable to recognize the image format.")
            except Exception as e:
                # Display a general error message for any unexpected errors
                messagebox.showerror("Image Error", f"Unexpected error while converting to PhotoImage: {e}")
        return None  # Return None if binary data is empty or conversion fails

    @staticmethod
    def load_image(file_path, target_width=300, target_height=300, quality=75):
        """
        Loads an image from the given file path, resizes it, and returns its binary data.
        :param file_path: Path to the image file
        :param target_width: Target width for resizing the image
        :param target_height: Target height for resizing the image
        :param quality: Quality for saving the resized image
        :return: Binary data of the resized image or None if loading fails
        """
        try:
            # Open the image file
            with Image.open(file_path) as img:
                # Resize the image to the target dimensions
                img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                # Create a BytesIO buffer to save the resized image
                buffer = io.BytesIO()
                # Save the resized image to the buffer in JPEG format with the specified quality
                img.save(buffer, format="JPEG", quality=quality)
                # Return the binary data from the buffer
                return buffer.getvalue()
        except FileNotFoundError:
            # Display an error message if the image file is not found
            messagebox.showerror("Image Error", f"File not found: {file_path}")
        except UnidentifiedImageError:
            # Display an error message if the image format is not recognized
            messagebox.showerror("Image Error", f"Unidentified image format: {file_path}")
        except Exception as e:
            # Display a general error message for any unexpected errors
            messagebox.showerror("Image Error", f"Unexpected error while loading image: {e}")
        return None  # Return None if loading fails
