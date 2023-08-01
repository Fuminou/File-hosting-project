from flask import Flask, request, jsonify, Response
import csv
import io
from db import get_db, close_db
import os

app = Flask(__name__)

@app.teardown_appcontext
def close_database(error):
    close_db(error)

@app.route('/export_upload_history', methods=['POST'])
def export_upload_history():
    # Get the database instance within the app context
    file_db = get_db()

    # Query the upload history from the database
    upload_history_data = file_db.get_all_files()

    # Create a list of dictionaries to represent each row in the CSV file
    rows = [{'file_name': row[0], 'file_size': format_file_size(len(row[1]))} for row in upload_history_data]

    # Create a CSV file
    output = io.StringIO()
    fieldnames = ["file_name", "file_size"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

    # Prepare the response with CSV content
    response = Response(output.getvalue(), content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=upload_history.csv'
    return response

def format_file_size(file_size):
    # Function to convert file size in bytes to a human-readable format (KB, MB, GB, etc.)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if file_size < 1024.0:
            return f"{file_size:.2f} {unit}"
        file_size /= 1024.0

# Function to handle new file uploads and update the upload history
def handle_upload(file_paths):
    # Get the database instance within the app context
    file_db = get_db()

    for file_path in file_paths:
        # Extract the file name from the file path
        file_name = file_path.split("/")[-1]

        # Get the file size
        file_size = os.path.getsize(file_path)

        # Read the file content
        with open(file_path, "rb") as f:
            file_content = f.read()

        # Insert the file into the database
        file_db.insert_file(file_name, file_content, file_size)

@app.route('/upload_files', methods=['POST', 'GET'])
def upload_files():
    # Get the list of uploaded files from the request
    uploaded_files = request.files.getlist("file")

    # Get the file paths of the uploaded files
    file_paths = [file.filename for file in uploaded_files]

    # Update the upload history with the new uploads
    handle_upload(file_paths)

    return "Files uploaded successfully!"

if __name__ == '__main__':
    app.run()
