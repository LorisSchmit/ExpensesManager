import PySimpleGUI as sg
import importer
from visualizeit import createGraphsYear
from createBalanceSheets import drawPDFCollection
from commonFunctions import getTotalExpenses
from budget import getBudgetPerYear, getTotalIncome
from importer import getPayPal
def importWidget():
    sg.change_look_and_feel('Dark Blue 3')

    layout = [  [sg.Text('Import movements as csv file: ',size=(25, 1)),sg.InputText(''),sg.FileBrowse()],
                [sg.Text('Import savings as csv file: ',size=(25, 1)),sg.InputText(''),sg.FileBrowse()],
                [sg.Text('Import PayPal transactions: ', size=(25, 1)), sg.InputText(''), sg.FileBrowse()],
                [sg.Text('Create Graphs for year: ', size=(25, 1)), sg.InputText(''), sg.Button('Create')],
                [sg.Text('Create Balance Sheets for year: ', size=(25, 1)), sg.InputText(''), sg.Button('Create')],
                [sg.Text('Show Accounting for year: ', size=(25, 1)), sg.InputText(''), sg.Button('Show')],
                [sg.Text('Accounting for year: ', size=(25, 1)), sg.Text('',key='-accounting-',size=(50,1))],
                [sg.Button('Ok'), sg.Button('Cancel'),sg.Button('Test')],
                ]

    window = sg.Window('Window Title', layout)


    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):   # if user closes window or clicks cancel
            break
        if event in (None, 'Ok'):
            file = values[0]
            importer.importSave(file)
        if event in (None, 'Test'):
            file = values[2]
            #getPayPal(file)
        if event in (None, 'Create'):
            year = values[3]
            createGraphsYear(year)
        if event in (None, 'Create1'):
            year = int(values[4])
            drawPDFCollection(year)
        if event in (None, 'Show'):
            year = int(values[5])
            total_expenses = str(getTotalExpenses(year))
            budget = str(getBudgetPerYear(year))
            output_text = 'Total : '+total_expenses+'€  Budget : '+budget+' €'
            print(output_text)
            window['-accounting-'].update(output_text)



    window.close()


importWidget()
