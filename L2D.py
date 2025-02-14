# Import neccessary modules
import tkinter as tk # Import tkinter for GUI development
from tkinter import ttk # Import ttk (themed Tkinter) for themed widgets

class L2D:
    # Define color dictionaries for light and dark modes
    light_mode_colors = {
        "bg": "lightblue",  # Background color
        "text": "black",  # Text color
        "add_button_bg": "#90EE90",  # Add button background color (light green)
        "delete_button_bg": "#FF0000",  # Delete button background color (red)
        "edit_button_bg": "#FFFF00",  # Edit button background color (yellow)
        "view_records_button_bg": "white",  # View records button background color
        "toggle_button_bg": "#87CEFA",  # Toggle mode button background color
        "speak_button_bg": "orange",  # Speak button background color
        "logout_button_bg": "lightcoral",  # Logout button background color
        "search_button_bg": "lightgray",  # Search button background color
        "treeview_heading_bg": "#ADD8E6",  # Treeview heading background color (light blue)
        "treeview_heading_fg": "black",  # Treeview heading foreground color (black)
        "button_bg": "white",  # Generic button background color
        "button_fg": "black"  # Generic button foreground color
    }

    dark_mode_colors = {
        "bg": "#1e1e1e",  # Background color (dark gray)
        "text": "white",  # Text color (white)
        "add_button_bg": "black",  # Add button background color (black)
        "delete_button_bg": "black",  # Delete button background color (black)
        "edit_button_bg": "black",  # Edit button background color (black)
        "view_records_button_bg": "black",  # View records button background color (black)
        "toggle_button_bg": "black",  # Toggle mode button background color (black)
        "speak_button_bg": "black",  # Speak button background color (black)
        "logout_button_bg": "black",  # Logout button background color (black)
        "search_button_bg": "gray",  # Search button background color
        "treeview_heading_bg": "#444",  # Treeview heading background color (dark gray)
        "treeview_heading_fg": "white",  # Treeview heading foreground color (white)
        "button_bg": "black",  # Generic button background color (black)
        "button_fg": "white"  # Generic button foreground color (white)
    }

    @staticmethod
    def set_theme(root, colors):
        """
        Sets the theme for the application by applying the provided color scheme.
        :param root: Tkinter root window
        :param colors: Dictionary of colors for the theme
        """
        # Create a ttk style object for setting styles
        style = ttk.Style()

        # Set the root window's background color
        root.configure(bg=colors["bg"])

        # Configure Treeview heading styles with provided background and foreground colors
        style.configure("Treeview.Heading", background=colors["treeview_heading_bg"], foreground=colors["treeview_heading_fg"], font=("Helvetica", 10, "bold"))
        
        # Configure a generic button style
        style.configure("TButton", background=colors["button_bg"], foreground=colors["button_fg"])

        # Configure specific button styles using colors from the dictionary
        style.configure("Add.TButton", background=colors["add_button_bg"], foreground=colors["text"])
        style.configure("Delete.TButton", background=colors["delete_button_bg"], foreground=colors["text"])
        style.configure("Edit.TButton", background=colors["edit_button_bg"], foreground=colors["text"])
        style.configure("ViewRecords.TButton", background=colors["view_records_button_bg"], foreground=colors["text"])
        style.configure("Toggle.TButton", background=colors["toggle_button_bg"], foreground=colors["text"])
        style.configure("Speak.TButton", background=colors["speak_button_bg"], foreground=colors["text"])
        style.configure("Logout.TButton", background=colors["logout_button_bg"], foreground=colors["text"])
        style.configure("Search.TButton", background=colors["search_button_bg"], foreground=colors["text"])

        # Update all buttons in the root window with their respective styles
        for widget in root.winfo_children():
            if isinstance(widget, ttk.Button):
                # Determine which style to use based on the button's text
                style_name = {
                    "Add Record": "Add.TButton",
                    "Delete Record": "Delete.TButton",
                    "Edit Record": "Edit.TButton",
                    "View All Books": "ViewRecords.TButton",
                    "Toggle Mode": "Toggle.TButton",
                    "Speak Book Details": "Speak.TButton",
                    "Logout": "Logout.TButton",
                    "Search": "Search.TButton"
                }.get(widget.cget("text"), "TButton")  # Default to generic style if no match is found

                # Apply the style to the button
                widget.configure(style=style_name)
            elif isinstance(widget, tk.Frame):
                # Update frame background colors
                widget.configure(bg=colors["bg"])
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label):
                        # Update label background and foreground colors
                        child.configure(background=colors["bg"], foreground=colors["text"])
                    elif isinstance(child, ttk.Entry):
                        # Update entry background and foreground colors
                        child.configure(background=colors["bg"], foreground=colors["text"])
                    elif isinstance(child, ttk.Button):
                        # Update button styles within the frame
                        button_style_name = {
                            "Search": "Search.TButton"
                        }.get(child.cget("text"), "TButton")  # Default to generic style if no match is found
                        child.configure(style=button_style_name)
