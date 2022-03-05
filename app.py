import os
import sys
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename

import code_judge
import problems

UPLOAD_FOLDER = "./code_files/"
EXTENSIONS = [".py", ".java", ".c", ".cpp"]

app = Flask(__name__)

@app.route("/", methods=['GET']) #TODO: change this path to /upload later
def upload() -> str:
    """
    Directs user to the page to upload a code file

    Returns:
        string: a string to be parsed into HTML by browser
    """
    return render_template("upload.html")

@app.route("/submit", methods=['GET', 'POST'])
def submit() -> str:
    """
    Handles the user uploading the code file to the server

    Returns:
        string: an HTML string for browser to parse
    """
    if request.method == 'POST':
        if 'code' not in request.files:
            flash("No file, invalid")
            return redirect(request.url)
        print("files", request.files, file=sys.stdout)
        print("request", request.form, file=sys.stdout)
        file = request.files['code']
        # make sure there's a file that exists
        if (file is not None and file.filename is not "") \
            and (file.filename).endswith(tuple(EXTENSIONS)): # make sure the file ends with a valid extension
            print(file, file=sys.stdout)
            file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
            filename = file.filename
            #TODO: get problem as well and submit + judge code
            return render_template("submit.html", filename=file.filename)
        else:
            return "<p>Invalid file</p>"
    return "<p>Ran</p>"

@app.route("/problem/<problem_id>", methods=['GET'])
def display_problem(problem_id: str) -> str:
    """
    Handles user requesting a specific problem

    Args:
        problem_id (str): the id of the problem, specified in URL

    Returns:
        str: the HTML of the problem template
    """
    return render_template("problem.html", data=problems.get_problem_info(int(problem_id)))

if __name__ == "__main__":
    app.run()