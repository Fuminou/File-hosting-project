"""
Finally working on the damn db.
Just a simple sqlite database with one table used to keep all the files.
There are better db schemes for this like multiple tables by file type to help keep queries fast for fat files but...
I'm just too fucking lazy.

Table scheme is just a 3 column table, rowid, file_name (primary key), blob containing the file binaries
"""

import sqlite3

"""
Gonna make the whole damn db a class so its exposed to that monkey through method calls.
"""


class Database:
    """
    Simple database object using sqlite under the hood.
    interacting with the db can be done via methods calls on a db object instantiated elsewhere.
    """

    def __init__(self) -> None:
        self.conn = sqlite3.connect("file_store.db")  # establish the connection
        self.cursor = self.conn.cursor()  # create the cursor object

        # create the table, note; this is no longer needed after spinning up the db for the first time
        self.cursor.execute("CREATE TABLE IF NOT EXISTS files (filename TEXT PRIMARY KEY, contents BLOB)")
        self.conn.commit()

    """
    Close db objects when no longer needed
    """

    def close(self) -> None:
        self.cursor.close()
        self.conn.close()

    """
    Simple method that inserts a file into the database
    """

    def insert_file(self, file_name: str, file_content: bytes) -> None | str:
        try:
            self.cursor.execute("INSERT INTO files (filename, contents) VALUES (?, ?)", (file_name, file_content))
            self.conn.commit()
        except Exception as e:
            print(e)
            return "Duplicate file names are not allowed!"

    """
    Simple query method to find a file by its name, may add queries by index in the future
    """

    def query_file(self, file_name: str) -> list | str:
        try:
            self.cursor.execute("SELECT * FROM files WHERE filename = ?", (file_name,))
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return "There was an error retrieving those entries"

    """
    Returns only the contents of the queried file.
    """

    def query_file_content(self, file_name: str) -> bytes:
        return self.query_file(file_name)[0][1]

    """
    Writes the contents of the file to the local machines file system
    """

    def download_file(self, path: str, file_name: str) -> None:
        with open(path, "wb") as f:
            f.write(self.query_file_content(file_name))

    """
    Gets all the files in the db
    """

    def get_all_files(self) -> list | str:
        try:
            self.cursor.execute("SELECT * FROM files")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return "there was an error retrieving those entries"

    """
    Wipes the database, technically just wipes one table, but that's all we have
    """

    def clear_db(self) -> None:
        self.cursor.execute("DELETE FROM files")
        self.conn.commit()


# spinning up the db for the first time
if __name__ == "__main__":
    db = Database()

    db.download_file("C:/Users/user/Downloads/db_test.pdf", "C:/Users/user/Downloads/FIT2081-Notes (1).pdf")

    # little test script here to see if we can actually add shit
    db.clear_db()
    # db.insert_file("wumba", "wumbo")
    # db.insert_file("wiggle", "waggle")
    # print(db.query_file_content("wiggle"))

    db.close()
