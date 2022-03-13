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
    os.system("pwd > project_dir.txt")
    with open("project_dir.txt", "r") as f:
        dir = f.read()
    os.chdir(dir[:-1])
    return dir

def get_user_dir(user, game_dir): return f"./users/{user}"