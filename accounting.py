from commonFunctions import defineFiles,importByFiles,total
from budget import getTotalIncome


def main():
    files = defineFiles(2018)
    transacts = importByFiles(files)
    total_spent = total(transacts)
    spent_per_week = round(total_spent/52,2)
    budget = getTotalIncome(files)
    budget_per_week = round(budget/52,2)
    deficit = round(total_spent + budget,2)

    print(str(total_spent)+" € spent ")
    print(str(spent_per_week)+" € spent per week")
    print(str(budget) +" € of budget")
    print(str(budget_per_week) + " € of budget per week")
    print(str(deficit)+" € of deficit")
    print()



if __name__ == "__main__":
    main()