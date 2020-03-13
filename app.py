
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

header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"}

r = requests.get('https://www.worldometers.info/coronavirus/', headers=header)
dfs = pd.read_html(r.text)
covid16_table= dfs[0]
covid16_table = covid16_table.fillna('0')
covid16_table.rename(columns = {'Country,Other':'Country', 'Serious,Critical':'Critical'},inplace = True) 
#covid16_table.NewCases = covid16_table.NewCases.apply(lambda x: x.replace('+',''))
final_table = covid16_table
final_table.iloc[:,2:].apply(pd.to_numeric, errors='coerce')
final_table= final_table.fillna('0')
final_table = final_table.sort_values(by=['NewCases'], ascending=False)
final_table.to_csv('static/images/covid16_table.csv')

def listof_countries():

   
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"}

    r = requests.get('https://www.worldometers.info/coronavirus/', headers=header)
    dfs = pd.read_html(r.text)
    covid16_table= dfs[0]
    covid16_table = covid16_table.fillna('0')
    covid16_table.rename(columns = {'Country,Other':'Country', 'Serious,Critical':'Critical'},inplace = True) 
    covid16_table.NewCases = covid16_table.NewCases.apply(lambda x: x.replace('+',''))
    final_table = covid16_table
    final_table.iloc[:,2:].apply(pd.to_numeric, errors='coerce')
    final_table= final_table.fillna('0')

    return list(final_table['Country'])

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
    covid16_table['sortingnewcases'] = covid16_table['sortingnewcases'].str.replace(',', '')
    covid16_table['sortingnewcases'] = covid16_table['sortingnewcases'].apply(pd.to_numeric)
    sorted_newcases = covid16_table[covid16_table['sortingnewcases'] > 0 ].sort_values(by=['sortingnewcases'], ascending=False)
    sorted_newcases = sorted_newcases.set_index('Country')
    sorted_newcases = sorted_newcases[['NewCases', 'NewDeaths']].fillna(0)


    info_mongodbpairs = pd.read_csv('static/images/covid16_table.csv')
    summarycases =  info_mongodbpairs.iloc[:1,2:6] 

    #TotalCases
    totalcases = summarycases.iloc[:,:1]
    totalcases = totalcases.set_index('TotalCases')
    #NewCases
    newcases = summarycases.iloc[:,1:2]
    newcases = newcases.set_index('NewCases')
    #TotalDeaths
    totaldeaths = summarycases.iloc[:,2:3]
    totaldeaths = totaldeaths.set_index('TotalDeaths')
    #NewDeaths
    newdeaths = summarycases.iloc[:,3:4]
    newdeaths = newdeaths.set_index('NewDeaths')

    return render_template("index.html", sorted_newcases = sorted_newcases.to_html(), totalcases = totalcases.to_html(), summary = summarycases.to_html(),newcases=newcases.to_html() )


@app.route('/names')
def namess():

   
    list_countries = pd.read_csv('static/images/covid16_table.csv')
    
    return jsonify(list(list_countries['Country']))



 # Return MetaData for specific sample
@app.route("/metadata/<sample>")
def sample_metadata(sample = "China"):
    
    for dicte in dict_list():
        if dicte['Country'] == sample:
            dataDict = dicte
        
    return jsonify(dataDict)



if __name__ == '__main__':
    app.run(debug=True)


