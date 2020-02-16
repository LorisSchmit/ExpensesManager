from Transaction import Transaction
import datetime
from Account import CC_LUX
from commonFunctions import object2list
import csv
from tagging import tagObject
from importer import saveObject

def readNewCSVObject(file):
    with open(file,mode="r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=";")
        transacts = []
        for index,row in enumerate(csv_reader):
            if index > 3 and (row[2].find("PAYPAL") != -1 or row[2].find("SCHMIT LORIS CARLO, 130") != -1 or row[2].find("Loris Schmit, DE22660908000007898649") != -1 or row[2].find("RETRAIT BANCOMAT") != -1 or row[2].find("DECOMPTE VISA") != -1):
                comma_pos = row[2].rfind(",")
                sender = row[2][:comma_pos].replace(",","")
                reference = row[2][comma_pos + 2:].replace(",","")
                amount = row[3].replace(",", ".")
                date = datetime.datetime.strptime(row[0], "%d/%m/%Y")
                transact = Transaction(date, row[1].replace(",",""), sender, reference, amount, row[4], '', CC_LUX)
                transacts.append(transact)
    transacts = list(reversed(transacts))
    return transacts

def main():
    file = "/Users/lorisschmit1/PycharmProjects/BudgetManager/Movements/Movements.csv"
    transacts = readNewCSVObject(file)
    print(len(transacts))
    tagObject(transacts)
    transacts.reverse()
    saveObject(transacts,"Account Movements")
if __name__ == '__main__':
    main()