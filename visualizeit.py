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
    return round(tot,2)

def perTag(transacts):
    tags_temp = {}
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
            tot = round(tot, 2)
            tags_temp[tag] = tot

    rest = 0
    for tag in tags_temp:
        if tags_temp[tag] >= 20:
            tags[tag] = tags_temp[tag]
        elif tags_temp[tag] > 0:
            rest += float(tags_temp[tag])
    rest = round(rest, 2)
    tags['rest'] = rest
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

def createGraphCollection(months,year):
    for month_index, month in enumerate(months):
        transacts = getTransacts(month_index, year)
        tags = perTag(transacts)
        tot = total(transacts)
        max = biggestTag(tags)[1]
        createGraph(tags, month_index, year,tot,max)

def embedGraph():
    with open('token.txt', mode="r") as token_file:
        username = token_file.readline()
        api_key = token_file.readline()
    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

def createGraph(data,month_index,year,tot,max):
    labels = list(data.keys())
    values = list(data.values())
    rot_fact = (3/8-max/tot)*8*55
    if rot_fact<0:
        rot_fact = 0
    title = months[month_index]+" "+year
    layout = dict(showlegend=False, width=400, height=515, margin=dict(l=5,t=0,r=10,b=0),
                  font=dict(
                      size=19
                  ),
                  annotations=[
                      go.layout.Annotation(
                          x=1,
                          y=0.97,
                          xref="paper",
                          yref="paper",
                          text="Total : " + str(tot) + " €",
                          font=dict(
                              color="black",
                              size=20
                          ),
                          showarrow=False,
                      )
                    ],
                  )
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)],layout=layout)
    fig.update_traces(textinfo='label',hoverinfo='percent+value',rotation=rot_fact,)
    #fig.show()
    fig.write_image("images/"+title+".pdf")



months = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober"]
year = "2019"
tag_collection = []
transacts = getTransacts(7,year)
tags = perTag(transacts)
tot = total(transacts)
#embedGraph()
max = biggestTag(tags)[1]
#createGraph(tags,7,year,tot,max)
createGraphCollection(months,year)
