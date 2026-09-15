"""программа для работы с процессами"""

import subprocess
import os
import multiprocessing as mp
import time

def main():
    print("Starting")
    print(f"PID main : {os.getpid()}")
    print(f"PID parent main : {os.getppid()}")
    proc = mp.Process(welcome())
    proc.start()


def welcome():
    print("Hello")
    print(f"PID : {os.getpid()}")
    print(f"PID : {os.getppid()}")
    time.sleep(5)
    work()

def work():
    print("Working")
    print(f"PID : {os.getpid()}")
    time.sleep(5)
    finish()

def finish():
    print(f"PID : {os.getpid()}")
    time.sleep(5)
    print("Finished")

proc_main = mp.Process(main())
proc_main.start() 
