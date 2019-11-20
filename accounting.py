import csv
import datetime
#!

#balance_giro =
#balance_savings =


file_giro = 'expenses.csv'
file_savings = 'savings_transacts.csv'

transacts_giro = []
transacts_temp = []
transacts_savings_temp = []
transacts_savings = []


with open(file_giro) as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=",")
    for row in csv_reader:
        transacts_temp.append(row)

date_time_real_start = datetime.datetime.strptime("01/10/2018", '%d/%m/%Y')
date_time_real_end = datetime.datetime.strptime("30/09/2019", '%d/%m/%Y')

for action in transacts_temp:
    date_str = action[0]
    date = datetime.datetime.strptime(date_str,"%d/%m/%Y")
    if date > date_time_real_start:
        transacts_giro.append(action)

with open(file_savings) as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=",")
    for row in csv_reader:
        transacts_savings_temp.append(row)

for action in transacts_savings_temp:
    date_str = action[0]
    date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
    if date > date_time_real_start:
        transacts_savings.append(action)


tot_giro = 0
tot_savings = 0
tot_spent = 0
food = 0
atm = 0
visa = 0
rest = 0
num = len(transacts_giro)

rest_list = []



for n in transacts_giro:
    found = False
    #if n[1] != "UTILISATION CARTE DE DEBIT" and n[2].find("SCHMIT") == -1 and n[2].find("TRESORERIE") == -1:
        #print(n[0]+","+n[1]+","+n[2]+","+n[3]+","+n[4])
    tot_giro -= float(n[4])
    if n[2].find("SCHMIT LORIS") != -1 or n[2].find("TRESORERIE")!= -1 or n[3] == " Argent de poche et repas":
        tot_spent -= float(n[4])
        found = True
    if n[2].find("SCHECK-IN") != -1 or n[2].find("REWE") != -1:
        food -= float(n[4])
        found = True
    if n[2].find("RETRAIT") != -1:
        atm -= float(n[4])
        found = True
    if n[2].find("VISA") != -1:
        visa -= float(n[4])
        found = True
    if not found:
        rest_list.append(n)
        rest -= float(n[4])



for n in transacts_savings:
    amount = float(n[4])
    if amount > 0:
        tot_savings += float(n[4])

end = transacts_giro[0][0]
start = transacts_giro[num-1][0]

date_time_start = datetime.datetime.strptime(start, '%d/%m/%Y')
date_time_end = datetime.datetime.strptime(end, '%d/%m/%Y')


days = (date_time_real_end-date_time_real_start).days
weeks = days/7

#print("From "+start+" to "+end+", I spent "+str(tot_spent))
#print("That's "+str(days)+" days, so "+str(days/7)+" weeks")

per_week = tot_spent/weeks

#print(str(per_week)+" € per week")

#print(str(food)+" for food")

#print(str(atm)+" atm")

#print(str(visa)+" visa")

#print(str(rest)+" rest")

total = food + atm + visa + rest

#print(str(total)+" total")

print(tot_savings)