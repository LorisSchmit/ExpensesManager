from datetime import datetime
import csv


def readExpense(action):
    action.account.balance += action.amount
    #print("Expense of "+str(action.amount)+" from "+action.account.name)
    #print("Account balance "+str(CC_LUX.balance))
    action.account.update()

def transferAccount(emitter_account, receiver_account,amount):
    emitter_account.balance -= abs(amount)
    receiver_account.balance += abs(amount)
    #print("Transferring "+str(amount)+" from "+emitter_account.name+" to "+receiver_account.name)
    #print("Account balance "+str(CC_LUX.balance))
    updateAccounts([emitter_account,receiver_account])


def getBalances():
    with open("balances.csv", mode="r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        balances = []
        for row in csv_reader:
            balance = round(float(row[0]),2)
            date = datetime.fromtimestamp(int(row[1]))
            balances.append([balance,date])
    return balances

def saveBalances():
    with open("balances.csv", mode="w") as file:
        csv_writer = csv.writer(file, delimiter=",")
        for row in balances:
            csv_writer.writerow([str(row[0]),int(datetime.timestamp(row[1]))])

def updateAccounts(accounts):
    for account in accounts:
        date = datetime.now()
        index = balances_lookup[account.name]
        balances[index][0] = round(account.balance,2)
        balances[index][1] = date
    saveBalances()


class Account:
    def __init__(self,name):
        self.balances_lookup = {'Compte courant': 0, 'Girokonto': 1, 'Compte épargne': 2,
                                'PayPal': 3, 'Geldbeutel': 4, 'Visa': 5}
        self.name  = name
        self.balance = self.getBalance(name)[0]
        self.date = self.getBalance(name)[1]

    def getBalance(self, name):
        with open("balances.csv", mode="r") as file:
            csv_reader = csv.reader(file, delimiter=",")
            balances = []
            for row in csv_reader:
                balances.append(row)
        index = self.balances_lookup[name]
        balance = float(balances[index][0])
        date = datetime.fromtimestamp(int(balances[index][1]))
        return (balance,date)

    def transfer(self,amount, account):
        self.balance -= amount
        account.balance += amount

    def update(self):
        self.date = datetime.now()
        index = self.balances_lookup[self.name]
        balances[index][0] = round(self.balance,2)
        balances[index][1] = self.date
        saveBalances()

    def getDate(self):
        return self.date


balances_lookup = {'Compte courant': 0, 'Girokonto': 1, 'Compte épargne': 2,
                    'PayPal': 3, 'Geldbeutel': 4, 'Visa': 4}

balances = getBalances()

CC_LUX = Account('Compte courant')
GK_DE = Account('Girokonto')
CE_LUX = Account('Compte épargne')
PP = Account('PayPal')
GB = Account('Geldbeutel')
VISA = Account('Visa')


