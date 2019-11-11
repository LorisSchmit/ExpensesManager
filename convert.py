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

def convert(from_file,to_file):
    file = open(from_file,'r')
    file_write = open(to_file,'w+')

    for n,line in enumerate(file):
        if n>2:
            line_list = list(line)
            pos = line.rfind(",")
            line_list[pos] = "."
            line = "".join(line_list)
            line = line.replace(";", ",")
            comma_count = line.count(',')
            if comma_count>5:
                second_comma = find_nth(line, ',', 2)
                first_half = line[:second_comma+1]
                second_half = line[second_comma:]
                line = first_half+second_half.replace(',','',comma_count-4)
            if line.find('VISA') != -1 or line.find('SOURCE') != -1 or line.find('ARRETE') != -1:
                third_comma = find_nth(line,',',3)
                first_half = line[:third_comma]
                second_half = line[third_comma:]
                line = first_half +","+ second_half
            if n == 3:
                line = line[1:]
            file_write.write(line)

def toMonths(file):
    transacts = []
    with open(file, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=",")
        for row in csv_reader:
            transacts.append(row)
        csv_file.close()


    months = []
    date_str = transacts[0][0]
    date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
    month0 = date.month
    monthly_transacts = []
    for action in transacts:
        print(action)
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

    for month in months:
        date_str = month[0][0]
        date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        month_number = str(date.month)
        year = str(date.year)
        file_name = year+"/"+month_number+".csv"
        with open(file_name, mode="w+") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            for action in month:
                csv_writer.writerow(action)
            csv_file.close()




#convert('Movements.csv','expenses.csv')
#convert('savings_movements.csv','savings_transacts.csv')
#convert('19_20/Movements.csv','19_20/transacts.csv')
toMonths('expenses_tagged.csv')

#print(find_nth('03/10/2019,DECOMPTE VISA,DECOMPTE VISA AU 21/09/2019,-210.61 , EUR',',',4))

