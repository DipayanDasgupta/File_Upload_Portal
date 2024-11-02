from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, storage

app = Flask(__name__)

# Firebase Admin SDK configuration with the correct JSON file
cred = credentials.Certificate('file-upload-portal-e5d77-firebase-adminsdk-tir7y-32f62f936f.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'file-upload-portal-e5d77.appspot.com'  # Replace with your project ID
})

bucket = storage.bucket()

# Allowed extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('upload.html', message="No file part")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('upload.html', message="No selected file")
    
    if file and allowed_file(file.filename):
        blob = bucket.blob(f"files/{file.filename}")
        blob.upload_from_file(file)
        blob.make_public()
        file_url = blob.public_url
        return render_template('upload.html', message="File uploaded successfully!", file_url=file_url)

    return render_template('upload.html', message="Invalid file extension")

# Route to view all files
@app.route('/files')
def list_files():
    blobs = bucket.list_blobs(prefix='files/')
    file_urls = [(blob.name, blob.public_url) for blob in blobs]
    return render_template('files.html', file_urls=file_urls)

if __name__ == "__main__":
    app.run(debug=True)

