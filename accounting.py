from commonFunctions import defineFiles,importByFiles,total,readCSVtoObjectExpense,perWeek
from budget import getTotalIncome


def getData(transacts,budget):
    total_spent = total(transacts)
    spent_per_week = round(total_spent / 52, 2)
    budget_per_week = round(budget / 52, 2)
    deficit = round(total_spent + budget, 2)

    data = {'Total Expenses': total_spent}

def main():
    files = defineFiles(2018,".csv")
    budget = getTotalIncome(files)
    transacts = readCSVtoObjectExpense(7,"2019")
    getData(transacts,budget)
    total_spent = total(transacts)



if __name__ == "__main__":
    main()