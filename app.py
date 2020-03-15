
import pandas as pd
import numpy as np
import pymongo
from flask import Flask, render_template
from flask import jsonify
import json
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from bson.json_util import dumps
import bson.json_util as json_util
import quandl
import requests

app = Flask(__name__, static_url_path='')

population_latlong = pd.read_csv('population_latlong.csv')
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
r = requests.get('https://www.worldometers.info/coronavirus/', headers=header)
dfs = pd.read_html(r.text)
covid16_table= dfs[0]
covid16_table = covid16_table.fillna('0')
covid16_table.rename(columns = {'Country,Other':'Country', 'Serious,Critical':'Critical'},inplace = True) 
#covid16_table.NewCases = covid16_table.NewCases.apply(lambda x: x.replace('+',''))
final_table = covid16_table
final_table.iloc[:,2:].apply(pd.to_numeric, errors='coerce')
#final_table= final_table.fillna('0')
final_table['NewCases']= final_table['NewCases'].apply(pd.to_numeric, errors='coerce')

final_table = final_table.sort_values(by=['NewCases'])
final_table = final_table.merge(population_latlong, on='Country')
final_table = final_table.drop(columns='Unnamed: 0')
final_table['TotalRecovered'] = final_table['TotalRecovered'].apply(pd.to_numeric, errors='coerce')
final_table['TotalDeaths'] = final_table['TotalDeaths'].apply(pd.to_numeric, errors='coerce')
final_table['Population'] = final_table['Population'] * 1000
final_table['PopulationAffected'] = final_table['TotalCases'] / final_table['Population'] *100
final_table['Cases Recovered'] =  final_table['TotalRecovered'] / final_table['TotalCases'] * 100
final_table['Cases Active'] =  final_table['ActiveCases'] / final_table['TotalCases'] * 100

final_table['Mortality Rate'] =  final_table['TotalDeaths'] / final_table['TotalCases'] * 100
final_table.to_csv('static/images/covid16_table.csv')



def do_lat_long():
    lat_long = pd.read_csv('static/images/covid16_table.csv')
    lat_long['TotalCases'] = lat_long['TotalCases'].apply(pd.to_numeric, errors='coerce')
    lat_long = lat_long.iloc[:-1,:]
    graphing_value = []
    
    for e in lat_long['TotalCases']:
    
        if e < 20:
            graphing_value.append(150)
        if e >= 20 and e < 100:  
            graphing_value.append(250)
        if e >= 100 and e < 200:    
            graphing_value.append(300)
        if e >= 200 and e < 400:  
            graphing_value.append(400)
        if e >= 400 and e < 1000:    
            graphing_value.append(500)
        if e >= 1000 and e < 2000:    
            graphing_value.append(600)    
        if e >= 2000 and e < 3000:    
            graphing_value.append(800)
        if e >= 3000 and e < 4000:    
            graphing_value.append(1000)    
        if e >= 4000 and e < 8000:    
            graphing_value.append(1200)
        if e >= 8000 and e < 22000:    
            graphing_value.append(1500)
        if e >= 22000:    
            graphing_value.append(3000)   
        
    lat_long['graphing_value'] = graphing_value
 
    lat_long = lat_long.fillna(0.000000)
    lat_long = lat_long.replace('\W', '')
    lat_long = lat_long.transpose() 
    lat_long = lat_long.to_dict()
    lat_long = [value for value in lat_long.values()]
    
    return lat_long




def dict_list():
    info_mongodbpairs = pd.read_csv('static/images/covid16_table.csv')
    info_mongodbpairs = info_mongodbpairs.iloc[:,1:]
    list_of_dicts = []
    info_mongodbpairs = info_mongodbpairs.transpose() 
    info_mongodbpairs = info_mongodbpairs.to_dict()
    list_of_dics = [value for value in info_mongodbpairs.values()]
    return list_of_dics


@app.route("/")
def home_page():
    # GET SORTED NEW CASES AND DEATHS

    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
    scrape_r = requests.get('https://www.worldometers.info/coronavirus/', headers=header)
    covid16_table = pd.read_html(scrape_r.text)
    covid16_table= covid16_table[0]
    covid16_table.rename(columns = {'Country,Other':'Country', 'Serious,Critical':'Critical'},inplace = True) 
    startswithlist = []

    for i in covid16_table.NewCases:
        if str(i).startswith('+'):
            startswithlist.append(i[1:])
        else:
            startswithlist.append(i)

    covid16_table['sortingnewcases'] = startswithlist        
    covid16_table['sortingnewcases'] = covid16_table['sortingnewcases']
    covid16_table['sortingnewcases'] = covid16_table['sortingnewcases'].apply(pd.to_numeric)
  
    sorted_newcases = covid16_table[covid16_table['sortingnewcases'] > 0 ]
    print(sorted_newcases)
    sorted_newcases = sorted_newcases.set_index('Country')
    sorted_newcases = sorted_newcases[['NewCases', 'NewDeaths']].fillna(0)
    sorted_newcases = sorted_newcases.iloc[1:,:]

    final_table = pd.read_csv('static/images/covid16_table.csv')
    final_table = final_table.iloc[:,1:]
    print(final_table)
    #TotalCases
    totalcases = final_table.iloc[-1:,1:2]
    totalcases = totalcases.set_index('TotalCases')
    #NewCases
    newcases =  final_table.iloc[-1:,2:3]
    newcases = newcases.set_index('NewCases')
    #TotalDeaths
    totaldeaths = final_table.iloc[-1:,3:4]
    totaldeaths = totaldeaths.set_index('TotalDeaths')
    #NewDeaths
    newdeaths = final_table.iloc[-1:,4:5]
    newdeaths = newdeaths.set_index('NewDeaths')
    #Totalrecovered
    totalrecovered= final_table.iloc[-1:,5:6]
    totalrecovered = totalrecovered.set_index('TotalRecovered')
    #Activecases
    activecases =  final_table.iloc[-1:,6:7]
    activecases = activecases.set_index('ActiveCases')
    #Pop % Affected
    popaffected = final_table.iloc[-1:,12:13].round(4).astype(str) + '%'
    popaffected  = popaffected.set_index("PopulationAffected")
    #Percentage Recovered
    pctrecovered = final_table.iloc[-1:,13:14].round(2).astype(str) + '%'
    pctrecovered = pctrecovered.set_index('Cases Recovered')
    #Percentage Active
    pctactive = final_table.iloc[-1:,14:15].round(2).astype(str) + '%'
    pctactive = pctactive.set_index('Cases Active')
   #Mortality Rate %
    mortalityrate= final_table.iloc[-1:,15:16].round(2).astype(str) + '%'
    mortalityrate = mortalityrate.set_index('Mortality Rate')
   

  
    return render_template("index.html", sorted_newcases = sorted_newcases.to_html(), totalcases = totalcases.to_html(), newdeaths = newdeaths.to_html(),newcases=newcases.to_html(), totaldeaths=totaldeaths.to_html(), totalrecovered = totalrecovered.to_html(), activecases = activecases.to_html(), popaffected = popaffected.to_html(), pctrecovered = pctrecovered.to_html(), pctactive = pctactive.to_html(), mortalityrate = mortalityrate.to_html())


@app.route('/names')
def namess():

   
    list_countries = pd.read_csv('static/images/covid16_table.csv')
    
    return jsonify(list(list_countries['Country']))


@app.route('/latandlong')
def namesss():

   
    return jsonify(do_lat_long())



 # Return MetaData for specific sample
@app.route("/metadata/<sample>")
def sample_metadata(sample = "China"):
    
    for dicte in dict_list():
        if dicte['Country'] == sample:
            dataDict = dicte
        
    return jsonify(dataDict)



if __name__ == '__main__':
    app.run(debug=True)


