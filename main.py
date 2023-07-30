import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from db import *
import requests
import shutil
import os

upload_window = None
view_files_window = None
view_upload_history_window = None
uploaded_files = []
view_uploaded_files = []

#################################################
# DATABASE STUFF HERE                           #
#################################################
file_db = Database()

def open_upload_files():
    global upload_window

    # Hide the main window
    window.withdraw()

    # Create a new window for uploading files
    upload_window = tk.Toplevel()
    upload_window.title("Upload Files")
    upload_window.geometry("400x500")

    # Create a back button to return to the main window
    btn_back = tk.Button(upload_window, text="Back", command=go_back_upload_files)
    btn_back.pack(pady=10)

    # Create a label for drag and drop area
    lbl_drag_drop = tk.Label(upload_window, text="Drag and drop files here", bg="lightgray", width=30, height=10)
    lbl_drag_drop.pack(pady=10)

    # Enable drag and drop functionality for the label
    lbl_drag_drop.drop_target_register(DND_FILES)
    lbl_drag_drop.dnd_bind('<<Drop>>', handle_drop)

    # Create a button to manually choose files
    btn_choose_files = tk.Button(upload_window, text="Choose Files", command=choose_files)
    btn_choose_files.pack(pady=10)

    # Create a listbox to display uploaded files
    list_files = tk.Listbox(upload_window, width=40, height=10)
    list_files.pack(pady=10)

    # Create an upload button
    btn_upload = tk.Button(upload_window, text="Upload", command=upload_files)
    btn_upload.pack(pady=10)

    # Store the listbox widget in a global variable for later use
    upload_window.list_files = list_files


def handle_drop(event):
    files = event.data
    file_list = window.tk.splitlist(files)
    handle_files(file_list)


def choose_files():
    files = filedialog.askopenfilenames()
    handle_files(files)


def handle_files(files):
    for file in files:
        if file not in uploaded_files:
            uploaded_files.append(file)
            upload_window.list_files.insert(tk.END, file)


def upload_files():

    # grabbing all the files from the machine using the provided path strings
    for path in uploaded_files:
        with open(path, "rb") as f:
            binaries = f.read()
            file_db.insert_file(path, binaries)

    # Update the view uploaded files list
    global view_uploaded_files
    view_uploaded_files = uploaded_files.copy()

    # Create a pop-up window to display the message
    popup_window = tk.Toplevel(upload_window)
    popup_window.title("Upload Status")
    popup_window.geometry("200x100")

    # Create a label to show the upload status message
    lbl_status = tk.Label(popup_window, text="Files have been uploaded!")
    lbl_status.pack(pady=20)

    def close_popup():
        # Destroy the pop-up window and go back to the main screen
        popup_window.destroy()
        window.deiconify()

    def close_window():
        # Destroy the pop-up window and go back to the main screen
        upload_window.destroy()
        window.deiconify()

    # Automatically close the pop-up window after a delay (e.g., 2000 milliseconds)
    popup_window.after(1000, close_popup)
    upload_window.after(1000, close_window)


def open_view_files():
    global view_files_window

    # Hide the main window
    window.withdraw()

    # Create a new window for viewing files
    view_files_window = tk.Toplevel()
    view_files_window.title("View Files")
    view_files_window.geometry("400x300")

    # Create a back button to return to the main window
    btn_back = tk.Button(view_files_window, text="Back", command=go_back_view_files)
    btn_back.pack()

    # Add the desired functionality for the View Files window here

list_files_view_upload_history = None  # Store the listbox widget for later use

def open_view_upload_history():
    global view_upload_history_window
    global list_files_view_upload_history  # Make the listbox widget global

    # Hide the main window
    window.withdraw()

    # Create a new window for viewing upload history
    view_upload_history_window = tk.Toplevel()
    view_upload_history_window.title("View Upload History")
    view_upload_history_window.geometry("400x300")

    # Create a back button to return to the main window
    btn_back = tk.Button(view_upload_history_window, text="Back", command=go_back_view_upload_history)
    btn_back.pack()

    # Create a listbox to display uploaded files
    list_files_view_upload_history = tk.Listbox(view_upload_history_window, width=40, height=10)
    list_files_view_upload_history.pack(pady=10)

    # Populate the listbox with the uploaded files for view upload history
    for file in view_uploaded_files:
        list_files_view_upload_history.insert(tk.END, file)

    # Create an "Export CSV" button
    btn_export_csv = tk.Button(view_upload_history_window, text="Export CSV", command=export_csv)
    btn_export_csv.pack()

def export_csv():
    # Make a request to the microservice's /export_upload_history endpoint
    url = "http://localhost:5000/export_upload_history"
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Check if the old CSV file exists
        if os.path.exists("upload_history.csv"):
            # Save the received CSV data to a temporary file on the client's machine
            with open("temp_upload_history.csv", "wb") as temp_file:
                temp_file.write(response.content)

            # Create a new CSV file and transfer the old and new contents to it
            with open("upload_history.csv", "rb") as old_file, open("temp_upload_history.csv", "rb") as new_file:
                with open("upload_history_new.csv", "wb") as combined_file:
                    shutil.copyfileobj(old_file, combined_file)
                    shutil.copyfileobj(new_file, combined_file)

            # Remove the temporary file
            os.remove("temp_upload_history.csv")

            # Remove the old CSV file
            os.remove("upload_history.csv")

            # Rename the new CSV file to "upload_history.csv"
            os.rename("upload_history_new.csv", "upload_history.csv")

            print("CSV file exported successfully!")
        else:
            # If the old CSV file doesn't exist, create a new one
            with open("upload_history.csv", "wb") as csv_file:
                csv_file.write(response.content)

            print("CSV file exported successfully!")
    else:
        print("Failed to export CSV file.")
        
def go_back_upload_files():
    global upload_window
    global uploaded_files

    # Clear the uploaded files list
    uploaded_files = []

    # Destroy the upload window
    upload_window.destroy()

    # Show the main window
    window.deiconify()


def go_back_view_files():
    global view_files_window

    # Destroy the view files window
    view_files_window.destroy()

    # Show the main window
    window.deiconify()


def go_back_view_upload_history():
    global view_upload_history_window

    # Destroy the view upload history window
    view_upload_history_window.destroy()

    # Show the main window
    window.deiconify()


# Create the main window
window = TkinterDnD.Tk()

# Set the window size
window.geometry("500x500")

# Add a "Welcome" label
label_welcome = tk.Label(window, text="Welcome to my file hosting program!", font=("Helvetica", 16))
label_welcome.pack(pady=20)

# Create the buttons
btn_upload_files = tk.Button(window, text="Upload Files", command=open_upload_files, width=15, height=2)
btn_view_files = tk.Button(window, text="View Files", command=open_view_files, width=15, height=2)
btn_view_upload_history = tk.Button(window, text="View Upload History", command=open_view_upload_history, width=15,
                                    height=2)

# Position the buttons using the place() geometry manager
btn_upload_files.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
btn_view_files.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
btn_view_upload_history.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

# Start the main loop
window.mainloop()
file_db.close()
