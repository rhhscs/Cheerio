import os
import sys
import time
from multiprocessing.pool import ThreadPool
from multiprocessing import TimeoutError
import code_judge.config

def run_python(inp: str, script: str, out: str):
    """
    Runs a Python file

    Args:
        inp (string): the location of the input file
        script (string): location of the code to be judged
        out (string): location of the output file
    """
    os.system(f"type \"{inp}\" | {code_judge.config.RUN_PYTHON} \"{script}\" 1 > \"{out}\" 2>&1")

def run_cpp(inp: str, script: str, out: str):
    """
    Runs a C++ file

    Args:
        inp (string): the location of the input file
        script (string): location of the code to be judged
        out (string): location of the output file
    """
    os.system(f"{code_judge.config.COMPILE_CPP} main {script} 2> {out}") # tosses errors into output file, if there are errors then file won't be empty
    # TODO: check if file is empty, if empty return
    os.system(f"type {inp} | main 1 > {out} 2>&1")

def run_java(inp: str, script: str, out: str):
    """
    Runs a Java file

    Args:
        inp (str): the location of the input file
        script (str): location of the code to be judged
        out (str): location of the output file
    """
    os.system(f"{code_judge.config.COMPILE_JAVA} {script}")
    os.system(f"type {inp} | {script[:len(script) - 5]} > {out} 2>&1")

def compare(user_out, exp_out) -> str:
    """
    Compares the user output against the expected output

    Args:
        user_out (str): location of the file the user outputted to
        exp_out (str): the expected output

    Returns:
        str: submission status
    """
    with open(user_out, "r") as user_output_file:
        user_output = user_output_file.readlines()
        expected_output = exp_out.split("\n")
        if expected_output[-1] == "":
            del expected_output[-1]
        if len(user_output) < len(expected_output):
            return "WA"
        else:
            for i in range(len(expected_output)):
                if user_output[i].strip() != expected_output[i].strip():
                    return "WA"
    return "AC"

LANGUAGE_MAP = {"python": run_python, "java": run_java, "c/c++": run_cpp}
def judge(inp, expected_out, script, language, mem_lim, time_lim):
    """
    Executes the code then checks if the code is correct

    Args:
        inp (string): the input
        expected_out (string): the execpted output
        script (string): location of the code to be judged
        language (string): string of language chosen from when code was submitted
        mem_lim (int): maximum amount of memory the code execution is allowed to use in MB
        time_lim (int): maximum run time the code is allowed in seconds

    Returns:
        map: submission status
    """
    pool = ThreadPool(processes=1)
    result = None
    run_time = None
    if not language in LANGUAGE_MAP:
        return "Invalid"
    with open("./in.txt", "w") as input_file:
        input_file.write(inp)
    try:
        # TODO: make MLE a thing
        start_time = time.time()
        result = pool.apply_async(LANGUAGE_MAP[language], ("./in.txt", script, "./out.txt")).get(timeout=time_lim)
        run_time = time.time() - start_time
    except TimeoutError:
        result = "TLE"
        run_time = f">{time_lim}"
    if result is None:
        result = compare("./out.txt", expected_out)
    return {"status": result, "time": run_time}

def submit(problem, user, script, language):
    results = []
    for i in range(len(problem["input"])):
        status = judge(
            problem["input"][i][f"batch_{i + 1}"], 
            problem["output"][i][f"batch_{i + 1}"], 
            script, 
            language,
            int(problem["mem_lim"]),
            int(problem["time_lim"])
        )
        results.append(status)
    return results
