#!
import csv
import datetime
from commonFunctions import readCSVtoList,object2list
import tagging

def find_nth(str, needle ,n):
    haystack = str
    pos = str.find(needle)
    nth_pos = pos
    for i in range(1,n):
        haystack = haystack[pos+1:]
        pos = haystack.find(needle)
        nth_pos += pos+1
    return nth_pos



def toMonths(transacts):
    #transacts = readCSV(file)
    months = []
    date = transacts[0].date
    month0 = date.month
    monthly_transacts = []
    for action in transacts:
        date = action.date
        month = date.month
        if month0 == month:
            monthly_transacts.append(action)
        else:
            months.append(monthly_transacts)
            monthly_transacts = []
            monthly_transacts.append(action)
        month0 = month
    if len(monthly_transacts) != 0:
        months.append(monthly_transacts)
    return months

def saveMonths(months):
    for month in months:
        date = month[0].date
        month_number = str(date.month)
        year = str(date.year)
        file_name = year+"/"+month_number+".csv"
        with open(file_name, mode="w+") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            for action in month:
                csv_writer.writerow(object2list(action))

def save(transacts,file_name):
    with open(file_name,mode="w+") as csv_file:
        csv_writer = csv.writer(csv_file,delimiter=";")
        for row in transacts:
            csv_writer.writerow(row)

def getFirstTransact():
    with open('Movements/Movements.csv',mode="r") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=";")
        month0 = 0
        first_transacts = []
        for index,row in enumerate(csv_reader):
            if index > 3:
                date = datetime.datetime.strptime(row[0], "%d/%m/%Y")
                if date.month != month0:
                    comma_pos = row[2].rfind(",")
                    recipient = row[2][:comma_pos]
                    reference = row[2][comma_pos + 2:]
                    amount = row[3].replace(",", ".")
                    transact = [row[0], row[1], recipient, reference, amount, row[4]]
                    first_transacts.append(transact)
                month0 = date.month
        first_transacts_tagged = importer.tag(first_transacts)
        for action in first_transacts_tagged:
            date = datetime.datetime.strptime(action[0], "%d/%m/%Y")
            file = str(date.year)+"/"+str(date.month)+".csv"
            transacts = list(readCSVtoList(file))
            transacts.insert(0,action)
            with open(file,mode="w") as w_file:
                csv_writer = csv.writer(w_file,delimiter=";")
                for new_action in transacts:
                    csv_writer.writerow(new_action)
                    print(new_action)
                print()

def reverseTransacts(file):
    transacts = readCSVtoList(file)
    transacts_reversed = list(reversed(transacts))
    return transacts_reversed



def main():
    file = "2020/1.csv"
    transacts = reverseTransacts(file)
    save(transacts,file)

if __name__ == "__main__":
    main()