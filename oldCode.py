from commonFunctions import readCSVtoList,list2object
from importer import save,saveObject
import csv

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

def removeCommas():
    #files = defineFiles(2018,".csv")
    files = ["2019/10.csv","2019/11.csv","2019/12.csv"]
    for file in files:
        transacts = readCSVtoList(file)
        new_transacts = []
        for action in transacts:
            row = []
            for el in action:
                new_el = el.replace(",","")
                row.append(new_el)
            new_transacts.append(row)
        save(new_transacts,file)

def accountForIncome(file, account):
    transacts = readCSVtoObject(file)
    print(CE_LUX.name + " " + str(CE_LUX.balance))
    print(account.name + " " + str(account.balance))

    for action in transacts:
        if action.recipient.find("SCHMIT LORIS CARLO") != -1 and action.tag == "Einkommen":
            CE_LUX.transfer(action.amount, account)

    print(CE_LUX.name + " " + str(CE_LUX.balance))
    print(account.name + " " + str(account.balance))

def addAccount():
    #files = defineFiles(2018,".csv")
    files = ["savings.csv"]

    for file in files:
        transacts = []
        with open(file, mode="r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            for row in csv_reader:
                if len(row) <= 7:
                    if row[6] == "PayPal":
                        el = row
                        el.append("PayPal")
                    elif row[6] == "Visa":
                        el = row
                        el.append("Visa")
                    else:
                        el = row
                        el.append("Compte épargne")
                    print(el)
                    transacts.append(el)
            transacts_obj = []
            for action in transacts:
                transacts_obj.append(list2object(action))
        saveObject(transacts_obj,file[:-4])


if __name__ == '__main__':
    removeCommas()