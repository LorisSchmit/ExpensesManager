import os
import csv
from commonFunctions import weekNumberToDates
import datetime

def listdir_nohidden(path):
    files = []
    for f in os.listdir(path):
        if not f.startswith('.'):
            files.append(f)
    return files

year = "2019"


print(weekNumberToDates(2019,0))

