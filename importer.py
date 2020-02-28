import convert

import os
from tagging import tag,tagObject
import csv
import datetime
from Transaction import Transaction
from Account import CC_LUX,CE_LUX,GK_DE,PP,VISA, GB, readExpense, transferAccount

from commonFunctions import readCSVtoObject,object2list,list2object,readCSVtoList,readCSVtoObject, accountName2account, defineFiles, displayTransacts
from convert import saveMonths,save

import tkinter as tk
from tkinter import filedialog

from commonFunctions import listdir_nohidden

def readNewCSV(file):
    with open(file,mode="r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=";")
        transacts = []
        for index,row in enumerate(csv_reader):
            if index > 3:
                comma_pos = row[2].rfind(",")
                recipient = row[2][:comma_pos]
                reference = row[2][comma_pos+2:]
                amount = row[3].replace(",",".")
                transact = [row[0],row[1],recipient,reference,amount,row[4],'',CC_LUX]
                transacts.append(transact)
    return transacts

def readNewCSVObject(file, account):
    with open(file,mode="r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=";")
        transacts = []
        for index,row in enumerate(csv_reader):
            if index > 3:
                if account == VISA:
                    recipient = row[1].replace(",","")
                    reference = ''
                    amount = float(row[3].replace(",","."))
                    date = datetime.datetime.strptime(row[0], "%d/%m/%Y")
                    transact = Transaction(date,'Credit Card Transaction',recipient,reference,amount,row[4],'',account)
                    readExpense(transact)
                    transacts.append(transact)
                else:
                    comma_pos = row[2].rfind(",")
                    recipient = row[2][:comma_pos].replace(",","")
                    reference = row[2][comma_pos + 2:].replace(",","")
                    typ = row[1]
                    amount = float(row[3].replace(",", "."))
                    date = datetime.datetime.strptime(row[0], "%d/%m/%Y")
                    transact = Transaction(date, typ, recipient, reference, amount, row[4], '', account)
                    transacts.append(transact)
    return transacts

def importNewFile(file,account):
    year = "2020"
    month = max(listdir_nohidden(year))
    latest_file = year+"/"+str(month)+".csv"
    with open(latest_file, mode="r") as csv_file:
        old_transacts = []
        csv_reader = csv.reader(csv_file,delimiter=";")
        for row in csv_reader:
            acc = row[7]
            row1 = row[:-1]
            row1.append(acc)
            row2 = []
            for el in row1:
                row2.append(el.replace(",",""))
            obj = list2object(row2)
            old_transacts.append(obj)
    no_last_element = False
    if len(old_transacts)>0:
        last_element = old_transacts[len(old_transacts)-1]
    elif month >1:
        latest_file = year+"/"+str(month-1)
        old_transacts = readCSVtoObject(latest_file)
        last_element = old_transacts[len(old_transacts)-1]
    else:
        latest_file = str(int(year)-1) + "/" + str(12)
        old_transacts = readCSVtoObject(latest_file)
        last_element = old_transacts[len(old_transacts) - 1]

    lines = list(readNewCSVObject(file,account))

    i = 0
    found = False
    new_transacts = []
    account_movements = []

    while not found and i<len(lines) and not no_last_element:
        action = lines[i]
        if action.date == last_element.date and action.reference == last_element.reference:
            found = True
        if not found:
            print(action.recipient)
            if action.reference.find("PAYPAL") != -1 or action.recipient.find("SCHMIT LORIS CARLO") != -1 or action.recipient.find("Loris Schmit") != -1 or action.reference.find("RETRAIT BANCOMAT") != -1 or action.type.find("DECOMPTE VISA") != -1:
                account_movements.append(action)
                if action.reference.find("PAYPAL") != -1:
                    emitter_account = CC_LUX
                    receiver_account = PP
                elif action.recipient.find("SCHMIT LORIS CARLO") != -1:
                    if action.type == "VERSEMENT":
                        emitter_account = GB
                        receiver_account = CC_LUX
                        action.account = GB
                    else:
                        emitter_account = CE_LUX
                        receiver_account = CC_LUX
                        action.account = CE_LUX
                elif action.recipient.find("Loris Schmit") != -1:
                    emitter_account = CC_LUX
                    receiver_account = GK_DE
                elif action.reference.find("RETRAIT BANCOMAT") != -1:
                    emitter_account = CC_LUX
                    receiver_account = GB
                elif action.type.find("DECOMPTE VISA") != -1:
                    emitter_account = CC_LUX
                    receiver_account = VISA
                transferAccount(emitter_account,receiver_account,action.amount)
            else:
                new_transacts.append(action)
                readExpense(action)
        i += 1
    if no_last_element:
        new_transacts = lines

    new_transacts.reverse()
    tagObject(new_transacts)
    tagObject(account_movements)
    old_transacts.extend(new_transacts)
    transacts = old_transacts
    return transacts,account_movements

def getFile():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.update()
    return file_path

def importSave(file,account):
    print("CC_LUX balance "+str(CC_LUX.balance))
    print("PP balance "+str(PP.balance))
    imported_transacts = importNewFile(file,account)
    new_transacts = imported_transacts[0]
    account_movements = imported_transacts[1]
    old_account_movements = readCSVtoObject('Account Movements')
    account_movements.extend(old_account_movements)
    months = convert.toMonths(new_transacts)
    print("CC_LUX balance "+str(CC_LUX.balance))
    print("PP balance "+str(PP.balance))
    displayTransacts(new_transacts)
    saveMonths(months)
    saveObject(account_movements,"Account Movements")


def importPayPal(file):
    with open(file, mode="r") as csv_file:
        pp_transacts = []
        csv_reader = csv.reader(csv_file,delimiter=",")
        for index,row in enumerate(csv_reader):
            if row[3] != "Bank Deposit to PP Account" and index > 0:
                if row[9] != "":
                    amount = float(row[7])
                else:
                    amount = float(row[5])
                date = datetime.datetime.strptime(row[0], "%m/%d/%Y")
                transact = Transaction(date,row[3],row[11],'',amount,row[4],'',PP)
                readExpense(transact)
                pp_transacts.append(transact)
    return pp_transacts


def importDE(file):
    rows = []
    with open(file,mode="r",encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=";")
        for row in csv_reader:
            rows.append(row)
    transacts_list = rows[14:-3]
    transacts = []
    for row in transacts_list:
        amount_str = ('-')*(row[12] == 'S')+row[11].replace(',','.')
        amount = float(amount_str)
        transact = Transaction(datetime.datetime.strptime(row[0],'%d.%m.%Y'), row[2], row[3],row[8].replace("\n",""),amount,row[10],'',GK_DE)
        readExpense(transact)
        transacts.append(transact)
    transacts = list(reversed(transacts))
    return transacts

def includeTransacts(pp_transacts):
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
        new_transacts_months.append(new_transacts)
    return new_transacts_months


def includeMonthlyTransacts(pp_transacts):
    new_transacts = []
    file = str(pp_transacts[0].date.year) + "/" + str(pp_transacts[0].date.month)
    transacts = readCSVtoObject(file)
    i = 0
    for action in transacts:
        if i < len(pp_transacts):
            try:
                while action.date >= pp_transacts[i].date:
                    new_transacts.append(pp_transacts[i])
                    i += 1
                new_transacts.append(action)
            except IndexError:
                pass
        else:
            new_transacts.append(action)
    for action in new_transacts:
        print(object2list(action))
    return new_transacts

def saveObject(transacts,file):
    with open(file+".csv", mode="w+") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        for action in transacts:
            row = object2list(action)
            csv_writer.writerow(row)

def ditch(file,tag):
    transacts = readCSVtoObject(file)
    new_transacts = []
    for action in transacts:
        if action.tag != tag:
            new_transacts.append(action)
    saveObject(new_transacts,file)

def accountFor(file, tag, account):
    transacts = readCSVtoObject(file)
    print(CC_LUX.name+" "+str(CC_LUX.balance))
    print(account.name+" "+str(PP.balance))

    for action in transacts:
        if action.tag == tag:
            CC_LUX.transfer(-action.amount, account)

    print(CC_LUX.name + " " + str(CC_LUX.balance))
    print(account.name + " " + str(PP.balance))


def getPayPal(file):
    print("PP balance "+str(PP.balance))
    pp_transacts = importPayPal(file)
    pp_transacts_tagged = tagObject(pp_transacts)
    new_transacts = includeMonthlyTransacts(pp_transacts_tagged)
    file_save = str(new_transacts[0].date.year) + "/" + str(new_transacts[0].date.month)
    saveObject(new_transacts,file_save)
    #ditch(file_save,'PayPal')
    print("PP balance "+str(PP.balance))
    #accountFor(file_save,'PayPal',PP)

def getDE(file):
    transacts = importDE(file)
    transacts_tagged = tagObject(transacts)
    new_transacts = includeMonthlyTransacts(transacts_tagged)
    file_save = str(new_transacts[0].date.year) + "/" + str(new_transacts[0].date.month)
    #saveObject(new_transacts, file_save)
    #ditch(file_save, 'DE Konto')
    accountFor(file_save, 'DE Konto', GK_DE)

def getVisa(file):
    transacts = readNewCSVObject(file, VISA)
    transacts.reverse()
    transacts_tagged = tagObject(transacts)
    new_transacts = includeTransacts(transacts_tagged)
    for month in new_transacts:
        displayTransacts(month)
    saveMonths(new_transacts)
    # ditch(file_save, 'DE Konto')
    # addAccount()


def accountMovements():
    files = defineFiles(2019,"")
    files.extend(defineFiles(2018,""))
    new_transacts = []
    print(CC_LUX.name + " " + str(CC_LUX.balance))
    print(CE_LUX.name + " " + str(CE_LUX.balance))
    print(PP.name + " " + str(PP.balance))
    print(VISA.name + " " + str(VISA.balance))
    for file in files:
        transacts = readCSVtoObject(file)
        new_transacts = []
        for action in transacts:
            if action.tag != "PayPal":
                new_transacts.append(action)
            else:
                print(object2list(action))
        #saveObject(new_transacts,file)

    print(CC_LUX.name + " " + str(CC_LUX.balance))
    print(CE_LUX.name + " " + str(CE_LUX.balance))
    print(PP.name + " " + str(PP.balance))
    print(VISA.name + " " + str(VISA.balance))
    #saveObject(new_transacts,"Account Movements")



def main():
    file = "/Users/lorisschmit1/PycharmProjects/BudgetManager/Movements/Movements (7) copy.csv"
    #importSave(file,CC_LUX)
    #accountMovements()
    #files = defineFiles(2019,"")
    #for file in files:
       # ditch(file,'Visa')

if __name__ == "__main__":
    main()





