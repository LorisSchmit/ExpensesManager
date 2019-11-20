import os
import csv
from convert import toMonths,saveMonths

def listdir_nohidden(path):
    files = []
    for f in os.listdir(path):
        if not f.startswith('.'):
            files.append(f)
    return files

year = "2019"

transacts = []

with open(year+"/8.csv",mode="r") as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=";")
    for row in csv_reader:
        transacts.append(row)

saveMonths(toMonths(transacts))