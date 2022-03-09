import os
import sys
import threading
import code_judge.config

def run_python(inp, script, out):
    """
    Judges a Python file

    Args:
        inp (string): location of the input file
        script (string): location of the code to be judged
        out (string): location of the output file
    """
    try:
        os.system(f"type {inp} | {config.RUN_PYTHON} {script} 1 > {out} 2>&1")
    except:
        print("error", file=sys.stderr)

def run_cpp(inp, script, out):
    """
    Judges a C++ file

    Args:
        inp (string): location of the input file
        script (string): location of the code to be judged
        out (string): location of the output file
    """
    os.system(f"{config.COMPILE_CPP} main {script} 2> {out}") # tosses errors into output file, if there are errors then file won't be empty
    # TODO: check if file is empty, if empty return
    os.system(f"type {inp} | main 1 > {out} 2>&1")

def run_java(inp, script, out):
    os.system(f"{config.COMPILE_JAVA} {script}")
    os.system(f"type {inp} | {script[:len(script) - 5]} > {out} 2>&1")

def compare(user_out, exp_out) -> str:
    """
    Compares the user output against the expected output

    Args:
        user_out (str): location of the file the user outputted to
        exp_out (str): location of the file with the expected output

    Returns:
        str: submission status
    """
    with open(user_out, "r") as user_output_file, open(exp_out, "r") as expected_output_file:
        user_output = user_output_file.readlines()
        expected_output = expected_output_file.readlines()
        if len(user_output) < len(expected_output):
            return "WA"
        else:
            for i in range(len(expected_output)):
                if user_output[i].strip() != expected_output[i].strip():
                    return "WA"
    return "AC"

LANGUAGE_MAP = {"python": run_python, "java": run_java, "c/c++": run_cpp}
def judge(inp, script, out, language):
    """
    Executes the code then checks if the code is correct

    Args:
        inp (string): location of the input file
        script (string): location of the code to be judged
        out (string): location of the output file
        language (string): string of language chosen from when code was submitted

    Returns:
        str: submission status
    """
    if not language in LANGUAGE_MAP:
        return "Invalid"
    try:
        LANGUAGE_MAP[language](inp, script, out)
        # TODO: run this on a thread and limit the resources the thread gets for MLE and TLE errors
        return compare(out, None) #TODO: get the expected output based on the question it's being submitted to, test cases, etc.
    except:
        print("error", file=sys.stderr)

def submit(problem, user, script, language):
    pass #TODO: write this function
