from flask import Flask, render_template, request, send_file, abort
from werkzeug.utils import secure_filename
import os
from crypto_utils import encrypt_file, decrypt_file
from config import AES_KEY, UPLOAD_FOLDER

app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return "Use the form on the home page to upload files", 405

    # existing POST logic below

    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    if file.filename == "":
        return "Empty filename", 400

    filename = secure_filename(file.filename)
    data = file.read()

    encrypted_data = encrypt_file(data, AES_KEY)

    with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as f:
        f.write(encrypted_data)

    return "File uploaded and encrypted successfully"


@app.route("/download/<filename>")
def download_file(filename):
    filename = secure_filename(filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        abort(404)

    with open(filepath, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_file(encrypted_data, AES_KEY)

    temp_path = os.path.join(UPLOAD_FOLDER, f"temp_{filename}")
    with open(temp_path, "wb") as f:
        f.write(decrypted_data)

    response = send_file(temp_path, as_attachment=True)

    # 🔐 Delete decrypted file after sending
    response.call_on_close(lambda: os.remove(temp_path))

    return response


if __name__ == "__main__":
    app.run(debug=True)
