RUN_PYTHON = "python"
COMPILE_CPP = "g++ -o"
COMPILE_JAVA = "javac"

BAN_LIST = [
    "open", # don't let people read files (python, c++)
    "ofstream", # some cpp file read thing
    "File", # java.io.File;
]