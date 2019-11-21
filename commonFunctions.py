import csv
from Transaction import Transaction

def defineFiles(start_year):
    files = []
    for i in range(1,13):
        if i>=10:
            files.append(str(start_year)+"/"+str(i)+".csv")
        else:
            files.append(str(start_year+1)+"/"+str(i)+".csv")
    files.sort()
    return files

def total(transacts):
    tot = 0
    for action in transacts:
        if action.tag != "Einkommen":
            tot += action.amount
    return round(tot,2)

def readCSVtoList(file):
    with open(file,mode="r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=";")
        transacts = []
        for row in csv_reader:
            transacts.append(row)
    return transacts

def readCSVtoObject(month,year):
    file_name = year + "/" + str(month+1) + ".csv"
    transacts = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        for row in csv_reader:
            transacts.append(Transaction(row[0],row[1],row[2],row[3],-float(row[4]),row[5],row[6]))
    return transacts

def importByFiles(files):
    transacts = []
    for file in files:
        with open(file, mode="r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            for row in csv_reader:
                transacts.append(Transaction(row[0], row[1], row[2], row[3], float(row[4]), row[5], row[6]))
    return transacts