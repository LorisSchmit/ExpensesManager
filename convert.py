#!
import csv
import datetime

def find_nth(str, needle ,n):
    haystack = str
    pos = str.find(needle)
    nth_pos = pos
    for i in range(1,n):
        haystack = haystack[pos+1:]
        pos = haystack.find(needle)
        nth_pos += pos+1
    return nth_pos

def readCSV(file):
    with open(file,mode="r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=";")
        transacts = []
        for index,row in enumerate(csv_reader):
            if index > 3:
                comma_pos = row[2].rfind(",")
                sender = row[2][:comma_pos]
                reference = row[2][comma_pos+2:]
                transact = [row[0],row[1],sender,reference,row[3],row[4]]
                transacts.append(transact)
    return transacts

def toMonths(transacts):
    #transacts = readCSV(file)
    months = []
    date_str = transacts[0][0]
    date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
    month0 = date.month
    monthly_transacts = []
    for action in transacts:
        date_str = action[0]
        date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        month = date.month
        if month0 == month:
            monthly_transacts.append(action)
        else:
            months.append(monthly_transacts)
            monthly_transacts = []
        month0 = month
    if len(monthly_transacts) != 0:
        months.append(monthly_transacts)

    return months

def saveMonths(months):
    for month in months:
        date_str = month[0][0]
        date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        month_number = str(date.month)
        year = str(date.year)
        file_name = year+"/"+month_number+".csv"
        with open(file_name, mode="w+") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            for action in month:
                csv_writer.writerow(action)