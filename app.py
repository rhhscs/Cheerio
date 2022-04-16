import os
import sys
from flask import Flask, flash, make_response, request, redirect, render_template, url_for
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
    user = request.cookies.get("user")
    print(user)
    if user is None:
        return redirect("/login")
    else:
        return redirect("/problems")

@app.route("/about", methods=["GET"])
def about() -> str:
    """
    About Page

    Returns:
        str: a string to be parsed into HTML by the browser
    """
    return render_template("about.html")

@app.route("/rules", methods=["GET"])
def rules() -> str:
    """
    Contest Rules Page

    Returns:
        str: a string to be parsed into HTML by the browser
    """
    return render_template("rules.html")

@app.route("/upload/<problem_id>", methods=['GET'])
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
        file = request.files['code']
        # make sure there's a file that exists
        if (file is not None and file.filename is not "") \
            and (file.filename).endswith(tuple(EXTENSIONS)): # make sure the file ends with a valid extension
            file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
            results = code_judge.submit(
                problems.get_problem_info(int(problem_id)),
                None, #TODO: access Google account cookie
                os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)),
                request.form["language"]
            )
            return render_template("submit.html", filename=secure_filename(file.filename), results=results)
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

@app.route("/login", methods=['GET', 'POST'])
def login() -> str:
    """
    Authenticates user login

    Returns:
        str: the HTML for logging in
    """
    if request.method == 'GET':
        return render_template("login.html")
    else:
        resp = make_response(render_template("login.html"))
        print(request.form["userid"], file=sys.stdout) #TODO: do stuff with userid (log to db if user does not already exist)
        return resp

@app.route("/logout", methods=['GET'])
def logout() -> str:
    """
    Logs the user out

    Returns:
        str: the HTML for the place the user was redirected to
    """
    resp = make_response(redirect("/"))
    resp.delete_cookie("user") #TODO: make a logout template that just calls the logout function from Google API and redirects to /
    return resp

if __name__ == "__main__":
    app.run()