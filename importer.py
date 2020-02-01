import convert

import os
from tagging import tag,tagObject
import csv
import datetime
from Transaction import Transaction

from commonFunctions import readCSVtoObject,object2list,defineFiles,readCSVtoObject
from convert import readNewCSV,saveMonths

import tkinter as tk
from tkinter import filedialog

from commonFunctions import listdir_nohidden


def importNewFile(file):
    year = "2019"
    month = max(listdir_nohidden(year))
    latest_file = year+"/"+str(month)+".csv"

    with open(latest_file, mode="r") as csv_file:
        old_transacts = []
        csv_reader = csv.reader(csv_file,delimiter=";")
        for row in csv_reader:
            old_transacts.append(row)

    last_element = old_transacts[0]

    lines = readNewCSV(file)

    i = 0
    found = False
    new_transacts = []

    while not found and i<len(lines):
        if lines[i][0] == last_element[0]:
            if lines[i][1] == last_element[1]:
                found = True
        if not found:
            new_transacts.append(lines[i])
        i += 1
    new_transacts_tagged = tag(new_transacts)
    for action in new_transacts_tagged:
        print(action)
    new_transacts_tagged.extend(old_transacts)
    return new_transacts_tagged

def getFile():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.update()
    return file_path

def importSave(file):
    new_transacts_tagged = importNewFile(file)
    months = convert.toMonths(new_transacts_tagged)
    saveMonths(months)

def importPayPalOld(file):
    with open(file, mode="r") as csv_file:
        pp_transacts = []
        csv_reader = csv.reader(csv_file,delimiter=",")
        for index,row in enumerate(csv_reader):
            if row[3] != "Bank Deposit to PP Account" and index > 0:
                if row[9] != "":
                    amount = float(row[9])
                else:
                    amount = float(row[7])
                date = datetime.datetime.strptime(row[0], "%d/%m/%Y")
                pp_transacts.append(Transaction(date,row[4],row[3],row[37]+' '+row[38],amount,row[6],''))

    return pp_transacts

def importPayPal(file):
    with open(file, mode="r") as csv_file:
        pp_transacts = []
        csv_reader = csv.reader(csv_file,delimiter=",")
        for index,row in enumerate(csv_reader):
            if row[3] != "Bank Deposit to PP Account" and index > 0: #and (row[3] == "Express Checkout Payment" or row[3] == "Mobile Payment" or row[3] == "General Payment" or row[3] == "PreApproved Payment Bill User Payment")
                if row[9] != "":
                    amount = float(row[7])
                else:
                    amount = float(row[5])
                date = datetime.datetime.strptime(row[0], "%m/%d/%Y")
                pp_transacts.append(Transaction(date,row[3],row[11],'',amount,row[4],''))

    return pp_transacts

def includePayPalmonthly(pp_transacts):
    new_transacts = []
    file = str(pp_transacts[0].date.year) + "/" + str(pp_transacts[0].date.month)
    transacts = readCSVtoObject(file)
    i = 0
    for action in transacts:
        if i < len(pp_transacts):
            if action.date >= pp_transacts[i].date:
                new_transacts.append(pp_transacts[i])
                i += 1
            else:
                new_transacts.append(action)
        else:
            new_transacts.append(action)
    for action in new_transacts:
        print(str(action.date.day)+"/"+str(action.date.month)+" "+str(action.sender)+" "+str(action.amount))
    return new_transacts

def includePayPal(pp_transacts):
    new_transacts_months = []
    pp_months = convert.toMonths(pp_transacts)
    for pp_month in pp_months:
        file = str(pp_month[0].date.year) + "/" + str(pp_month[0].date.month)
        transacts = readCSVtoObject(file)
        new_transacts = []
        i = 0
        for action in transacts:
            if i < len(pp_month):
                if action.date >= pp_month[i].date:
                    new_transacts.append(pp_month[i])
                    new_transacts.append(action)
                    i += 1
                else:
                    new_transacts.append(action)
            else:
                new_transacts.append(action)
        for action in new_transacts:
            print(str(action.date.day)+"/"+str(action.date.month)+" "+str(action.sender)+" "+str(action.amount))
        new_transacts_months.append(new_transacts)
    return new_transacts_months

def saveObject(transacts,file):
    with open(file+".csv", mode="w+") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        for action in transacts:
            row = object2list(action)
            csv_writer.writerow(row)

def ditchPayPal(file):
    transacts = readCSVtoObject(file)
    new_transacts = []
    for action in transacts:
        if action.tag == "PayPal":
            print(action.sender+" "+str(action.amount))
        else:
            new_transacts.append(action)
    print()
    for action in new_transacts:
        print(action.sender+" "+str(action.amount))

    saveObject(new_transacts,file)

def getPayPal(file):
    pp_transacts = importPayPal(file)
    pp_transacts_tagged = tagObject(pp_transacts)
    new_transacts = includePayPal(pp_transacts_tagged)
    file_save = str(new_transacts[0].date.year) + "/" + str(new_transacts[0].date.month)
    # saveObject(month,file)
    print(file_save)


def main():
    files = defineFiles(2018,"")
    for file in files:
        print(file)
        ditchPayPal(file)


def secMain():
    file = getFile()
    new_savings_tagged = importNewFile()

if __name__ == "__main__":
    main()





