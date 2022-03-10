import os
import glob

for file in glob.glob("./code_files/*.*", recursive=True):
    os.remove(file)