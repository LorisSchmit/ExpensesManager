from reportlab.pdfgen import canvas
from reportlab.lib import colors
from operator import itemgetter

import os

from commonFunctions import perWeek,readCSVtoObjectExpense,monthNumberToMonthName,total,perTag,defineFiles
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

from reportlab.platypus import Table, TableStyle

from budget import getBudgetPerMonth,getBudget


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


def drawPDF(file,month,year,start_year):
    years = str(start_year)[2:]+"_"+str(start_year+1)[2:]

    file_name = "Balance Sheets"+years+"/"+year+"-"+str(month)+".pdf"

    image_path = file+".svg"
    document_title = month+" "+year
    title = monthNumberToMonthName(int(month)-1)+" "+year
    transacts = readCSVtoObjectExpense(file)
    total_spent = total(transacts)

    pdf = canvas.Canvas(file_name)

    pdf.setTitle(document_title)

    drawImage(image_path,pdf)

    tags = perTag(transacts)
    drawCategoryTable(pdf,tags)

    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(300, 780, title)

    weeks = perWeek(transacts)
    drawWeeksTable(pdf,weeks,int(month),int(year))

    pdf.line(50, 220, 540, 220)

    budget = getBudgetPerMonth(getBudget(2018))
    drawBalanceTable(pdf,budget,total_spent)

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(50,50,"Gesamtausgaben: "+str(total_spent)+" €")

    if not ("Balance Sheets"+years in os.listdir()):
        os.mkdir("Balance Sheets"+years)
    pdf.save()



def drawImage(image_path,pdf):
    drawing = svg2rlg(image_path)
    renderPDF.draw(drawing, pdf,  -150, 350)

def drawWeeksTable(pdf,weeks,month,year):
    data = []
    week_dates =[]
    for week in weeks.keys():
        start = week[0].strftime("%d/%m")
        end = week[1].strftime("%d/%m")
        if week[0].month == week[1].month:
            week_dates.append(start+" - "+end)
        elif week[0].month < month and (week[0].year == year):
            week_dates.append("     - " + end)
        elif week[1].month > month or (week[0].year > year):
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
    pdf.setFont("Helvetica", 18)
    pdf.drawString(50, 320, 'Ausgaben pro Woche')
    pdf.line(50, 318, 225, 318)
    t.wrapOn(pdf, 500, 300)
    t.drawOn(pdf, 50, 250)

def drawCategoryTable(pdf,tags):
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
    pdf.setFont("Helvetica", 18)
    pdf.drawString(350, 720, 'Ausgaben pro Kategorie')
    pdf.line(350, 718, 546, 718)
    t.wrapOn(pdf, 500, 300)
    t.drawOn(pdf, 400, 700 - len(tags) * 25)

def drawBalanceTable(pdf,budget,spent):
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
    pdf.drawString(50, 185, 'Bilanz')
    pdf.line(50, 183, 100, 183)
    t = Table(data,rowHeights=rowHeights)
    t.setStyle(TableStyle(style))
    t.wrapOn(pdf, 500, 300)
    t.drawOn(pdf, 50, 95)
    return t

def drawPDFCollection(start_year):
    files = defineFiles(start_year,"")
    for file in files:
        month = file[5:]
        year = file[:4]
        drawPDF(file,month,year,start_year)

def main():
    #drawPDF("2018/10","10","2018",2018)
    drawPDFCollection(2018)
    #test()
    #drawCategoryTable(transacts)
if __name__ == "__main__":
    main()

