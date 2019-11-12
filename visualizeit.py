import csv
import datetime
from Transaction import Transaction
from fpdf import FPDF
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import chart_studio
import chart_studio.plotly as py
#!

def getTransacts(month,year):
    file_name = year + "/" + str(month+1) + ".csv"
    transacts = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            transacts.append(Transaction(row[0],row[1],row[2],row[3],-float(row[4]),row[5],row[6]))
        csv_file.close()
    return transacts

def total(transacts):
    tot = 0
    for action in transacts:
        if action.tag != "income":
            tot += action.amount
    return tot

def perTag(transacts):
    tags = {}
    truth_table = []
    tot = 0
    tag = ""
    for el in transacts:
        truth_table.append(True)
    for i in range(0,len(transacts)):
        if truth_table[i]:
            tot = transacts[i].amount
            tag = transacts[i].tag
            for j in range(i+1,len(transacts)):
                if transacts[i].tag == transacts[j].tag and truth_table[j]:
                    tot += transacts[j].amount
                    truth_table[j] = False
            tot = round(tot,2)
            tags[tag] = tot
    return tags

def biggestTag(tags):
    max_key = next(iter(tags))
    max = tags[max_key]
    for tag in tags:
        if tags[tag] > max:
            max_key = tag
            max = tags[tag]
    return (max_key,max)




def perMonth(transacts):
    tot = 0
    for action in transacts:
        if action.tag != "income":
            tot += float(action.amount)
    tot = round(tot,2)
    return tot


def showTags():
    for i in range(1,10):
        month = str(i)
        transacts = getTransacts(month,"2019")
        print(month+" : "+str(perMonth(transacts)))
        tags = perTag(transacts)
        print(tags)
        print(biggestTag(tags))

def createGraphCollection(data):
    n = len(data)
    specs_sub = []
    specs = []
    for i in range(0,3):
        for j in range(0,4):
            type = {"type": "domain"}
            specs_sub.append(type)
        specs.append(list(specs_sub))

        specs_sub = []
    print(specs)
    fig = make_subplots(rows=n//3, cols=n//3+1,specs=specs)
    print(str(n//3) + "   " + str(n//3+1))
    for i,month in enumerate(data):
        labels = list(month.keys())
        values = list(month.values())
        row = i//3+1
        col = i%3+1
        print(str(row)+"   "+str(col))
        fig.add_trace(
            go.Pie(labels=labels, values=values,name=str(i+1)+"/2019"),
            row=i%3+1,col=i//3+1
        )
    fig.update_layout(width=400, height=1000,showlegend=False)
    fig.update_traces(hoverinfo='label+percent', textinfo='label+value')
    fig.show()
    #embedGraph()
    #py.plot(fig, filename='gdp_per_cap', auto_open=True)

def embedGraph():
    with open('token.txt', mode="r") as token_file:
        username = token_file.readline()
        api_key = token_file.readline()
    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

def createGraph(data,month_index,year,tot):
    labels = list(data.keys())
    values = list(data.values())
    title = months[month_index]+" "+year
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(textinfo='label+value',hoverinfo='percent')
    fig.update_layout(height=900)
    fig.update(layout_title_text=title, layout_showlegend=False, layout_title_x=0.5)
    fig.update_layout(
        annotations=[
            go.layout.Annotation(
                x=0.86,
                y=0.96,
                xref="paper",
                yref="paper",
                text="<b>Total : "+str(tot)+" €</b>",
                font=dict(
                    color="black",
                    size=20
                ),
                showarrow=False,
            )
        ]
    )
    fig.show()
    #fig.write_image("images/"+title+".pdf")



months = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober"]
year = "2019"
tag_collection = []
transacts = getTransacts(1,year)
tags = perTag(transacts)
tot = total(transacts)
#embedGraph()
createGraph(tags,1,year,tot)
'''
for month_index,month in enumerate(months):
    transacts = getTransacts(month_index,year)
    tags = perTag(transacts)
    createGraph(tags,month_index,year)
    tag_collection.append(tags)
'''
