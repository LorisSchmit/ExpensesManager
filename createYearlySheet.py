from budget import analyzeBudget,getBudget
from commonFunctions import getExpensesData,perTag,getTotalExpenses,biggestTag,total
from visualizeit import createGraph
from createBalanceSheets import drawImage, drawBalanceTable

from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from operator import itemgetter

def orderGraph(year,budget):
    if budget:
        data = analyzeBudget(year)
        tot = getBudget(year)
        name = "Budget "
        font_size = 19
    else:
        data = perTag(getExpensesData(year))
        tot = getTotalExpenses(year)
        name = "Expenses "
        font_size = 12

    max = biggestTag(data)[1]
    createGraph(data, "images/"+name + str(year), tot, max, font_size)

def createPDF(year):
    years = str(year)[2:] + "_" + str(year + 1)[2:]
    file_name = "Yearly Sheet"+years+".pdf"

    image_path_budget = "images/Budget "+str(year)+".svg"
    image_path_expenses = "images/Expenses "+str(year)+".svg"

    document_title = "Balance Sheet "+str(year)
    title = "Balance Sheet "+str(year)
    transacts = getExpensesData(year)
    total_spent = total(transacts)
    budget = getBudget(year)

    pdf = canvas.Canvas(file_name)

    pdf.setTitle(document_title)

    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(300, 790, title)

    drawImage(image_path_expenses, pdf, 245, 460, 0.6)
    drawImage(image_path_budget, pdf, -25, 510,0.5)

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(80, 430, "Budget: " + str(budget) + " €")
    pdf.drawString(320, 430, "Gesamtausgaben: " + str(total_spent) + " €")

    tags = perTag(transacts)
    drawCategoryTable(pdf, tags)

    pdf.line(50,165,530,165)
    drawBalanceTable(pdf, budget, total_spent, 50, 50)

    '''
    weeks = perWeek(transacts)
    drawWeeksTable(pdf, weeks, int(month), int(year))

    pdf.line(50, 220, 540, 220)

    budget = getBudgetPerMonth(getBudget(2018))
    drawBalanceTable(pdf, budget, total_spent)

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(50, 50, "Gesamtausgaben: " + str(total_spent) + " €")
    '''

    pdf.save()


def drawCategoryTable(pdf,tags):
    tag_list = []
    for key in tags.keys():
        element = [key,tags[key]]
        tag_list.append(element)
    tag_list = list(reversed(sorted(tag_list, key=itemgetter(1))))
    data = []
    subdata = []
    mod0 = 0
    for index,element in enumerate(tag_list):
        mod = index//7
        if mod != mod0:
            data.append(subdata)
            subdata = []
        mod0 = mod
        subdata.append([element[0],element[1]])
    data.append(subdata)

    for index0,ar in enumerate(data):
        rowHeights = len(ar) * [25]
        for index,element in enumerate(ar):
            value = str(element[1])+" €"
            ar[index][1] = value
        t = Table(ar, rowHeights=rowHeights)
        t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('FONTSIZE', (0, 0), (-1, -1), 15),
                               ]))
        pdf.setFont("Helvetica", 18)
        pdf.drawString(50, 380, 'Ausgaben pro Kategorie')
        pdf.line(50, 378, 245, 378)
        t.wrapOn(pdf, 500, 300)
        t.drawOn(pdf, 50+170*index0, 180)



def main():
    year = 2018
    #orderGraph(year,True)
    #orderGraph(year,False)
    createPDF(year)






if __name__ == "__main__":
    main()