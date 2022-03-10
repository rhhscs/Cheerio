import os
import sys
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename

import code_judge
import problems

UPLOAD_FOLDER = "./code_files/"
EXTENSIONS = [".py", ".java", ".c", ".cpp"]

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index() -> str:
    """
    Home page

    Returns:
        str: a string to be parsed into HTML by the browser
    """
    return render_template("index.html")

@app.route("/about", methods=["GET"])
def about() -> str:
    """
    About Page

    Returns:
        str: a string to be parsed into HTML by the browser
    """
    return render_template("about.html")

@app.route("/upload/<problem_id>", methods=['GET']) #TODO: change this path to /upload later
def upload(problem_id: str) -> str:
    """
    Directs user to the page to upload a code file

    Args:
        problem_id (str): the id of the problem, specified in URL

    Returns:
        string: a string to be parsed into HTML by browser
    """
    return render_template("upload.html", problem_id=problem_id)

@app.route("/submit/<problem_id>", methods=['GET', 'POST'])
def submit(problem_id: str) -> str:
    """
    Handles the user uploading the code file to the server

    Args:
        problem_id (str): the id of the problem, specified in URL

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
            code_judge.submit(
                problems.get_problem_info(int(problem_id)),
                None, # TODO: get user by cookie later
                os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)),
                request.form["language"]
            )
            return render_template("submit.html", filename=secure_filename(file.filename))
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
    return render_template("problem.html", data=problems.get_problem_info(int(problem_id)), problem_id=problem_id)

@app.route("/problems", methods=['GET'])
def list_all_problems() -> str:
    """
    Lists all the problems on client side

    Returns:
        str: the HTML formatted version of all problems
    """
    return render_template("problems.html", data=problems.get_all_problem_info())

if __name__ == "__main__":
    app.run()