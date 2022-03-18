"""
DEBUG SYSTEM MONITOR

keeps track of all the resources the system is currently using

todo:
    add in cpu usage
    gpu usage
    memory percentage
    hardware model numbers
"""
import os, psutil

def memory_info(pid):
    """
    Keeps track of the memory used.

    todo:
        maybe keep a track on percentage and if so maybe only allocate it a certain amount of maximum memory?
    """
    ps = psutil.Process(pid)

    mem = (ps.memory_info().rss)/1_000_000
    mem = round(mem, 2)
    #print(f"{pid}\n{mem}")
    return mem
