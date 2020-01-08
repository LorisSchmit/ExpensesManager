import csv
from Transaction import Transaction
import plotly.graph_objects as go
import chart_studio
from commonFunctions import total,readCSVtoObject,perTag,defineFiles,biggestTag
#!

def showTags():
    for i in range(1,10):
        month = str(i)
        transacts = getTransacts(month,"2019")
        print(month+" : "+str(total(transacts)))
        tags = perTag(transacts)
        print(tags)
        print(biggestTag(tags))

def createGraphCollection(months):
    for month in months:
        transacts = readCSVtoObject(month)
        tags = perTag(transacts)
        tot = total(transacts)
        max = biggestTag(tags)[1]
        createGraph(tags, month,tot,max,19)

def embedGraph():
    with open('token.txt', mode="r") as token_file:
        username = token_file.readline()
        api_key = token_file.readline()
    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

def createGraph(data,name,tot,max,font_size):
    labels = list(data.keys())
    values = list(data.values())
    rot_fact = (3/8-max/tot)*8*55
    if rot_fact<0:
        rot_fact = 0
    layout = dict(showlegend=False,font=dict(size=font_size),margin=dict(l=0, r=0, t=0, b=0))
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)],layout=layout)
    fig.update_traces(textinfo='label',hoverinfo='percent+value',rotation=rot_fact,)
    #fig.show()
    fig.write_image(name+".svg")

def createGraphsYear(year):
    months = defineFiles(int(year), "")
    createGraphCollection(months)

def main():
    year = "2019"
    createGraphsYear(int(year))

if __name__ == "__main__":
    main()