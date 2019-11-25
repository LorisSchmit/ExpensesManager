import csv
from Transaction import Transaction
import plotly.graph_objects as go
import chart_studio
from commonFunctions import total,readCSVtoObject,perTag
#!



def biggestTag(tags):
    max_key = next(iter(tags))
    max = tags[max_key]
    for tag in tags:
        if tags[tag] > max:
            max_key = tag
            max = tags[tag]
    return (max_key,max)


def showTags():
    for i in range(1,10):
        month = str(i)
        transacts = getTransacts(month,"2019")
        print(month+" : "+str(total(transacts)))
        tags = perTag(transacts)
        print(tags)
        print(biggestTag(tags))

def createGraphCollection(months,year):
    for month_index, month in enumerate(months):
        transacts = readCSVtoObject(month_index, year)
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
    layout = dict(showlegend=False,
                  font=dict(
                      size=19
                  ),
                  )
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)],layout=layout)
    fig.update_traces(textinfo='label',hoverinfo='percent+value',rotation=rot_fact,)
    #fig.show()
    fig.write_image("images/"+title+".svg")

def main():
    year = "2019"
    tag_collection = []
    transacts = readCSVtoObject(7,year)
    tags = perTag(transacts)
    tot = total(transacts)
    #embedGraph()
    max = biggestTag(tags)[1]
    #createGraph(tags,7,year,tot,max)
    createGraphCollection(months,year)

if __name__ == "__main__":
    months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober"]
    main()