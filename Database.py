# Import the necessary module for SQLite database operations
import sqlite3  # SQLite for database management

class Database:
    @staticmethod
    def Connection():
        """
        Establish a connection to the SQLite database.
        If the database file does not exist, it will be created.
        :return: sqlite3.Connection object
        """
        return sqlite3.connect("library.db")

    @staticmethod
    def initialize_db():
        """
        Initialize the database by creating necessary tables if they don't exist.
        This ensures that the database is ready for use with the required schema.
        """
        # Connect to the database (creates the file if it doesn't exist)
        conn = sqlite3.connect("library.db")
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Create tblBooks table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tblBooks (
                BookID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each book
                BookName TEXT NOT NULL,  -- Name of the book (cannot be empty)
                Author TEXT NOT NULL,  -- Name of the author (cannot be empty)
                PublishedYear TEXT NOT NULL,  -- Year the book was published (cannot be empty)
                Image BLOB  -- Image data of the book (optional)
            )
        ''')

        # Commit the transaction to save the changes to the database
        conn.commit()
        # Close the database connection
        conn.close()
