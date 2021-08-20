import os
import sys


def current_dir():
    """gets the current directory."""
    cudir = os.curdir
    print(os.getcwd())
    return cudir

def get_project_dir():
    """
    gets the project directory.

    problem: may not be foolproof. need a surefire way to get the project dir no matter where the file is located
    """
    os.chdir(sys.path[1])