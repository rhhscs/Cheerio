import os
import sys

def run_python(inp, script, out):
    """
    Judges a Python file

    Args:
        inp (string): location of the input file
        script (string): location of the code to be judged
        out (string): location of the output file
    """
    try:
        os.system(f"type {inp} | python {script} 1 > {out} 2>&1")
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
    os.system(f"g++ -o main {script} 2> {out}") # tosses errors into output file, if there are errors then file won't be empty
    # TODO: check if file is empty, if empty return
    os.system(f"type {inp} | main 1 > {out} 2>&1")

def run_java(inp, script, out):
    pass

LANGUAGE_MAP = {"python": run_python, "java": run_java, "c/c++": run_cpp}
def judge(inp, script, out, language):
    """
    Executes the code then

    Args:
        inp (string): location of the input file
        script (string): location of the code to be judged
        out (string): location of the output file
        language (string): string of language chosen from when code was submitted
    """
    try:
        LANGUAGE_MAP[language](inp, script, out)
    except:
        print("error", file=sys.stderr)