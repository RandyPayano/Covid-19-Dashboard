
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



app = Flask(__name__, static_url_path='')


def listof_countries():
    url= 'https://www.worldometers.info/coronavirus/' 
    covid16_table = pd.read_html(url)
    covid16_table = covid16_table[0].fillna('0')
    covid16_table.rename(columns = {'Country,Other':'Country', 'Serious,Critical':'Critical'},inplace = True) 
    covid16_table.NewCases = covid16_table.NewCases.apply(lambda x: x.replace('+',''))
    lat_long = pd.read_csv('static/images/latandlong.csv')
    pop = pd.read_csv('static/images/pop.csv')
    latlongpop = lat_long.merge(pop, on="Country")
    final_table = latlongpop.merge(covid16_table, on="Country")
    final_table['TotalRecovered'] = pd.to_numeric(final_table['TotalRecovered'])

    final_table['NewCases'] = final_table['NewCases'].apply(pd.to_numeric, errors='coerce')

    final_table['Pct Affected of Pop'] = final_table['TotalCases'] / final_table['Population 2018'] * 100
    final_table['Pct Recovered Cases'] = final_table['TotalRecovered'] / final_table['TotalCases'] * 100
    final_table = final_table.round(5)
    final_table.to_csv("static/images/covid16_table.csv")
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
    allmydata = pd.read_csv('static/images/covid16_table.csv')    
    allmydata = allmydata

    top_newcases = pd.read_csv('static/images/covid16_table.csv')
    top_newcases = top_newcases.set_index("Country")
    top_newcases = top_newcases.sort_values(by=['NewCases'], ascending=False)
    top_newcases = top_newcases[['NewCases','NewDeaths']].head(15)
    return render_template("index.html", data = top_newcases.to_html())


@app.route('/names')
def namess():

   
   
    return jsonify(listof_countries())



 # Return MetaData for specific sample
@app.route("/metadata/<sample>")
def sample_metadata(sample):
    
    for dicte in dict_list():
        if dicte['Country'] == sample:
            dataDict = dicte
        
    return jsonify(dataDict)












if __name__ == '__main__':
    app.run(debug=True)


