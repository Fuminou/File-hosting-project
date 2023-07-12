import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD

upload_window = None
view_files_window = None
view_upload_history_window = None
uploaded_files = []

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
    # Implement the upload functionality here
    pass

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

def open_view_upload_history():
    global view_upload_history_window

    # Hide the main window
    window.withdraw()

    # Create a new window for viewing upload history
    view_upload_history_window = tk.Toplevel()
    view_upload_history_window.title("View Upload History")
    view_upload_history_window.geometry("400x300")

    # Create a back button to return to the main window
    btn_back = tk.Button(view_upload_history_window, text="Back", command=go_back_view_upload_history)
    btn_back.pack()

def go_back_upload_files():
    global upload_window

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
btn_view_upload_history = tk.Button(window, text="View Upload History", command=open_view_upload_history, width=15, height=2)

# Position the buttons using the place() geometry manager
btn_upload_files.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
btn_view_files.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
btn_view_upload_history.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

# Start the main loop
window.mainloop()
