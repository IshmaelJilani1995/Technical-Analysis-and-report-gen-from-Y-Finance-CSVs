from jinja2  import Environment, FileSystemLoader #jinja for templating
from weasyprint import HTML #to turn HTMl into PDF
import os #for the renaming
import pandas as pd #pandas for the dataframes and 
import json #to convert the json storage file (other storage types can be used ofc)
#Just seperating the location line from the environment line

LocationString = FileSystemLoader('templates') 
#load templates as env, so the info can be passed
env = Environment(loader=LocationString)
#load template.html as report
report = env.get_template("reporttemplate.html")
# open json list of tickers and set to tickers list
with open("tickers.json", "r") as tickersjson:
    tickers = json.load(tickersjson)

for i in range(len(tickers)):
    #create a data frame from the csv in the CSVS folder
    dataframe = pd.read_csv('CSVS/'+tickers[i]+'.csv', parse_dates=True, index_col=0)
    #add a column to the dataframe which shows change over the day (data per day in CSV)
    dataframe['Change']=dataframe['Open']-dataframe['Close']
    #generate most basic descriptive stats for this basic starting prototype
    desc = dataframe.describe()
    #turn the dataframe into html (pandas is overpowered >:D)
    deschtml = desc.to_html()
    #open and write the html to the names file - in futre other analysis will be in other files
    o = open("templates/dynamictable.html", "w")
    o.write(deschtml)
    #creating a dictionary of variables to be passed
    specificdata = {
    "ticker" : tickers[i],
    }
#using the specific data, generate a full html string for the specific templated info. 
# Render a report with the specific data, report was declared as the template template.html earlier
    rawhtmltext = report.render(specificdata)
    #set the specific ticker to name to rename pdf
    name = tickers[i]
    #turn html string into pdf
    HTML(string=rawhtmltext).write_pdf("reports/report.pdf", stylesheets=["templates/formatting.css"])
    #basic rename
    os.rename('reports/report.pdf', 'reports/'+name+'.pdf')
