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
    x=os.system("pwd > project_dir.txt") # echos the project directory to the project dir folder. assumes unix.
    if x!=0: os.system("cd > project_dir.txt") # if not unix, it will be DOS/Windows

    with open("project_dir.txt", "r") as f:
        dir = f.read()
    os.chdir(dir[:-1])
    return dir

def get_user_dir(user, game_dir): return f"./users/{user}"