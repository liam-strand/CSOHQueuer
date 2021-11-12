import time
import os

class FileLock:

    def setLock(filename):
        os.open(f"{filename}.lock", os.O_CREAT|os.O_)