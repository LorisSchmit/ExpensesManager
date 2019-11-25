from reportlab.pdfgen import canvas
from reportlab.lib import colors
from operator import itemgetter

from commonFunctions import perWeek,readCSVtoObjectExpense,monthNumberToMonthName,total,perTag
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

from reportlab.platypus import Table, TableStyle

from budget import getBudgetPerYear,getBudgetPerMonth


def drawMyRuler(pdf):
    pdf.drawString(100, 810, 'x100')
    pdf.drawString(200, 810, 'x200')
    pdf.drawString(300, 810, 'x300')
    pdf.drawString(400, 810, 'x400')
    pdf.drawString(500, 810, 'x500')
    pdf.drawString(600, 810, 'x600')
    pdf.drawString(700, 810, 'x700')
    pdf.drawString(800, 810, 'x800')

    pdf.drawString(10, 100, 'y100')
    pdf.drawString(10, 200, 'y200')
    pdf.drawString(10, 300, 'y300')
    pdf.drawString(10, 400, 'y400')
    pdf.drawString(10, 500, 'y500')
    pdf.drawString(10, 600, 'y600')
    pdf.drawString(10, 700, 'y700')
    pdf.drawString(10, 800, 'y800')


def drawPDF(file,month,year):
    file_name = "Balance Sheets/"+str(month+1)+"-"+file+".pdf"
    image_path = "images/"+file+".svg"
    document_title = file
    title = file
    transacts = readCSVtoObjectExpense(month, year)
    total_spent = total(transacts)

    pdf = canvas.Canvas(file_name)
    #drawMyRuler(pdf)

    pdf.setTitle(document_title)

    drawImage(image_path,pdf)

    pdf.setFont("Helvetica", 18)

    tags = perTag(transacts)
    pdf.drawString(350,720,'Ausgaben pro Kategorie')
    pdf.line(350,718,546,718)
    t_category = drawCategoryTable(tags)
    t_category.wrapOn(pdf,500,300)
    t_category.drawOn(pdf,400,700-len(tags)*25)

    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(300, 780, title)

    pdf.setFont("Helvetica", 18)


    weeks = perWeek(transacts)
    pdf.drawString(50, 320, 'Ausgaben pro Woche')
    pdf.line(50,318,225,318)
    t_weeks = drawWeeksTable(weeks,8)
    t_weeks.wrapOn(pdf,500, 300)
    t_weeks.drawOn(pdf,50, 250)

    pdf.line(50, 220, 540, 220)


    pdf.drawString(50,185,'Bilanz')
    pdf.line(50, 183, 100, 183)
    budget = getBudgetPerMonth(getBudgetPerYear(2018))
    t_balance = drawBalanceTable(budget,total_spent)
    t_balance.wrapOn(pdf,500,300)
    t_balance.drawOn(pdf,50,95)

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(50,50,"Gesamtausgaben: "+str(total_spent)+" €")


    pdf.save()


def drawImage(image_path,pdf):
    drawing = svg2rlg(image_path)
    #drawing.renderScale = 0.001
    renderPDF.draw(drawing, pdf,  -150, 350)

def drawWeeksTable(weeks,month):
    data = []
    week_dates =[]
    for week in weeks.keys():
        start = week[0].strftime("%d/%m")
        end = week[1].strftime("%d/%m")
        if week[0].month == week[1].month:
            week_dates.append(start+" - "+end)
        elif week[0].month < month:
            week_dates.append("     - " + end)
        elif week[1].month > month:
            week_dates.append(start + " -     ")
    data.append(reversed(week_dates))
    week_values = list(reversed(list(weeks.values())))
    week_values_str = []
    for value in week_values:
        week_values_str.append(str(value)+" €")
    data.append(week_values_str)
    rowHeights = len(data)*[25]
    t=Table(data,rowHeights=rowHeights)
    t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('ALIGN',(0,0),(-1,-1),'CENTER'),
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('FONTSIZE', (0, 0), (-1, -1), 15),
                           ]))
    return t

def drawCategoryTable(tags):
    data = []
    for key in tags.keys():
        data.append([key,tags[key]])
    rowHeights = len(data) * [25]
    data = list(reversed(sorted(data, key=itemgetter(1))))
    for index,element in enumerate(data):
        value = str(element[1])+" €"
        data[index][1] = value
    t = Table(data, rowHeights=rowHeights)
    t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('FONTSIZE', (0, 0), (-1, -1), 15),
                           ]))
    return t

def drawBalanceTable(budget,spent):
    data = [['Gesamtausgaben',str(spent)+" €"],
            ['Budget pro Monat', str(budget)+" €"]]
    balance = round(budget-spent,2)

    style =[('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('FONTSIZE', (0, 0), (-1, -1), 15),
                           ]
    if balance > 0 :
        balance_str = "Suffizit"
        style.append(['BACKGROUND', (0, 2), (1, 2), colors.lightgreen])
    else:
        balance_str = "Defizit"
        style.append(['BACKGROUND', (0, 2), (1, 2), colors.rgb2cmyk(255, 150, 110)])

    data.append([balance_str,str(balance)+" €"])


    rowHeights = len(data) * [25]
    t = Table(data,rowHeights=rowHeights)
    t.setStyle(TableStyle(style))
    return t



def drawPDFCollection():
    for i in range(0,9):
        file = monthNumberToMonthName(i)+" 2019"
        print(file)
        drawPDF(file,i,"2019")


def main():
    #drawPDF("Januar 2019",0,"2019")
    drawPDFCollection()
    #test()
    transacts = readCSVtoObjectExpense(7, "2019")
    #drawCategoryTable(transacts)
if __name__ == "__main__":
    main()

