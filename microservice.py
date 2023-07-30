from flask import Flask, request, Response
import csv
import io

app = Flask(__name__)

# In-memory storage for upload history
upload_history_data = []

@app.route('/export_upload_history', methods=['GET'])
def export_upload_history():
    # Create a CSV file
    output = io.StringIO()
    fieldnames = ["file_name", "upload_date", "user_id"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(upload_history_data)

    # Prepare the response with CSV content
    response = Response(output.getvalue(), content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=upload_history.csv'
    return response

# Function to handle new file uploads and update the upload history
def handle_upload(file_paths):
    global upload_history_data

    # Implement database logic here to get user_id and other relevant details
    # For demonstration purposes, let's assume we have a user_id variable
    user_id = 1

    for file_path in file_paths:
        # Extract the file name from the file path
        file_name = file_path.split("/")[-1]

        # Add the new upload record to the upload history
        upload_record = {
            "file_name": file_name,
            "upload_date": "2023-07-30",  # Replace this with the actual upload date
            "user_id": user_id,
        }
        upload_history_data.append(upload_record)

@app.route('/upload_files', methods=['POST'])
def upload_files():
    # Get the list of uploaded files from the request
    uploaded_files = request.files.getlist("file")

    # Save the uploaded files to the server (optional)
    # You can save the files to a directory on the server if needed

    # Get the file paths of the uploaded files
    file_paths = [file.filename for file in uploaded_files]

    # Update the upload history with the new uploads
    handle_upload(file_paths)

    return "Files uploaded successfully!"

if __name__ == '__main__':
    app.run()
