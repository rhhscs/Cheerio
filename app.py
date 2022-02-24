import os
import sys
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./code_files/"
EXTENSIONS = [".py", "java", "c", "cpp"]

app = Flask(__name__)

@app.route("/", methods=['GET'])
def upload():
    return render_template("upload.html")

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        if 'code' not in request.files:
            flash("No file, invalid")
            return redirect(request.url)
        print("files", request.files, file=sys.stdout)
        print("request", request.form, file=sys.stdout)
        file = request.files['code']
        if file is not None and file.filename is not "":
            print(file, file=sys.stdout)
            file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
            filename = file.filename
            return render_template("submit.html", filename=file.filename)
        else:
            return "<p>Invalid</p>"
    return "<p>Ran</p>"

if __name__ == "__main__":
    app.run()