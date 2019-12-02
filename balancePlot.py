import csv
from Transaction import Transaction
import plotly.graph_objects as go

def importSavings():
    transacts =[]
    with open("savings.csv", mode="r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        for index, row in enumerate(csv_reader):
            transacts.append(Transaction(row[0], row[1], row[2], row[3], float(row[4]), row[5], row[6]))
    return transacts

def getBalance(year):
    with open("balance"+year,mode="r") as file:
        balance0 = float(file.readline())
    return balance0

def calculateBalance(balance0,transacts):
    balance = []
    balance.append(['01/10/2018',balance0])
    for action in transacts:
        new_balance = balance[len(balance)-1][1] + action.amount
        balance.append([action.date,new_balance])

    return balance

def plotBalance(balance):
    x = []
    y = []
    for element in balance:
        x.append(element[0])
        y.append(element[1])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y))
    fig.show()

def main():
    savings = importSavings()
    balance0 = getBalance("2018")
    balance = calculateBalance(balance0,savings)
    plotBalance(balance)

if __name__ == "__main__":
    main()

