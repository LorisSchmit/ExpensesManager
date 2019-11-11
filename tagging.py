import csv

file_giro = 'expenses.csv'

file_tagged = 'expenses_tagged.csv'

def auto_tag():
    transacts_giro = []
    rest_list = []
    copy_list = []

    with open(file_giro) as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=",")
        for row in csv_reader:
            transacts_giro.append(row)
        csv_file.close()

    with open(file_tagged, mode="w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for n in transacts_giro:
            if n[2].find("SCHMIT LORIS CARLO") != -1 or n[2].find("TRESORERIE")!= -1 or n[3] == " Argent de poche et repas":
                tag = "income"
            elif n[2].find("SCHECK-IN") != -1 or n[2].find("REWE") != -1 or n[2].find("KAUFLAND") != -1 or  n[2].find("DER FRISCHE MARKT") != -1 or n[2].find("Cactus") != -1:
                tag = "food"
            elif n[2].find("RETRAIT") != -1:
                tag = "atm"
            elif n[2].find("VISA") != -1:
                tag = "visa"
            elif n[2].find("DECATHLON") != -1 or n[2].find("BASISLAGER") != -1 or n[2].find("BIKE & OUTDOOR") != -1:
                tag = "sport"
            elif n[2].find("1und1") != -1 or n[2].find("Rundfunk ARD ZDF") != -1 or n[2].find("Stadtwerke Karlsruhe") != -1:
                tag = "nebenkosten"
            elif n[2].find("DM-Drogerie Markt") != -1 or n[2].find("Rossmann") != -1:
                tag = "drogerie"
            elif n[2].find("PayPal") != -1:
                tag = "paypal"
            elif n[2].find("AMAZON") != -1:
                tag = "amazon"
            else:
                rest_list.append(n)
                for row in copy_list:
                    tag = input("tag: ")
            csv_writer.writerow([n[0],n[1],n[2],n[3],n[4],n[5],tag])
        print(len(rest_list))
        csv_file.close()
    return transacts_giro

'''
def tag_rest():
    transacts = []
    with open(file_tagged, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        for row in csv_reader:
            transacts.append(row)
        csv_file.close()

    with open(file_tagged, mode="w") as csv_file:
        csv_writer = csv.writer(csv_file,delimiter=',')
        for n in transacts:
            if n[6] == "":
                print(n)
                tag = input("tag: ")
            else:
                tag = n[6]
            csv_writer.writerow([n[0], n[1], n[2], n[3], n[4], n[5], tag])

'''

#transacts = auto_tag()
tag_rest()