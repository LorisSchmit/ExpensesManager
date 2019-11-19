import os
import csv

def listdir_nohidden(path):
    files = []
    for f in os.listdir(path):
        if not f.startswith('.'):
            files.append(f)
    return files

year = "2019 copy"

dir = listdir_nohidden(year)

for file in dir:
    with open(year+"/"+file,mode="r") as csv_file:
        transacts = []
        csv_reader = csv.reader(csv_file,delimiter=",")
        for row in csv_reader:
            transacts.append(row)
    with open(year+"/"+file,mode="w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")
        for row in transacts:
            csv_writer.writerow(row)
