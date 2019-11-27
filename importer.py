from convert import toMonths,saveMonths,readNewCSV
from tagging import tag
import csv
import os

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



def main():
    file = getFile()
    new_transacts_tagged = importNewFile(file)
    months = toMonths(new_transacts_tagged)
    saveMonths(months)

def secMain():
    file = getFile()
    new_savings_tagged = importNewFile()

if __name__ == "__main__":
    main()




