
import pandas as pd
import numpy as np
from flask import Flask, render_template
from flask import jsonify
from flask import Flask, render_template, redirect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_url_path='')

population_latlong = pd.read_csv('population_latlong.csv')
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
r = requests.get('https://www.worldometers.info/coronavirus/', headers=header)
dfs = pd.read_html(r.text)
covid16_table= dfs[0]
covid16_table = covid16_table.fillna('0')
covid16_table.rename(columns = {'Country,Other':'Country', 'Serious,Critical':'Critical'},inplace = True) 
covid16_table = covid16_table.apply(lambda x: x.replace(',',''))
final_table = covid16_table

#final_table.iloc[:,2:] = final_table.iloc[:,2:].apply(pd.to_numeric, errors='coerce')
print(final_table)
#final_table= final_table.fillna('0')
#final_table['NewCases']= final_table['NewCases'].apply(pd.to_numeric, errors='coerce')

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


sorted_totals = final_table.sort_values(by=['TotalCases'], ascending=False)
sorted_totals  = sorted_totals.iloc[1:].fillna(0)
sorted_totals  =sorted_totals[['Country','TotalCases','TotalDeaths','ActiveCases']]
sorted_totals  = sorted_totals.rename(columns={"TotalCases": "Cases","TotalDeaths": "Deaths", "ActiveCases": "Active"})
sorted_totals = sorted_totals.set_index('Country')


sorted_popaffectcsv = final_table.sort_values(by=['PopulationAffected'], ascending=False)
sorted_popaffectcsv = sorted_popaffectcsv.iloc[:25,:]
sorted_popaffectcsv.to_csv('static/images/sorted_popaffectcsv.csv')

sorted_mortalityratecsv = final_table.iloc[:-1].sort_values(by=['Mortality Rate'], ascending=False)
sorted_mortalityratecsv = sorted_mortalityratecsv[sorted_mortalityratecsv["TotalCases"] > 20]
sorted_mortalityratecsv = sorted_mortalityratecsv.iloc[:25,:]
sorted_mortalityratecsv = sorted_mortalityratecsv.rename(columns={"Mortality Rate": "MortalityRate"})
sorted_mortalityratecsv.to_csv('static/images/sorted_mortalityratecsv.csv')


def do_lat_long():
    lat_long = pd.read_csv('static/images/covid16_table.csv')
    lat_long.iloc[:,2:] = lat_long.iloc[:,2:]
    lat_long['TotalCases'] = lat_long['TotalCases'].apply(pd.to_numeric, errors='coerce')
    lat_long = lat_long.iloc[:-1,:]
    graphing_value = []
    
    for e in lat_long['TotalCases']:
    
        if e < 20:
            graphing_value.append(150)
        if e >= 20 and e < 100:  
            graphing_value.append(200)
        if e >= 100 and e < 200:    
            graphing_value.append(300)
        if e >= 200 and e < 400:  
            graphing_value.append(400)
        if e >= 400 and e < 1000:    
            graphing_value.append(500)
        if e >= 1000 and e < 2000:    
            graphing_value.append(600)    
        if e >= 2000 and e < 3000:    
            graphing_value.append(700)
        if e >= 3000 and e < 4000:    
            graphing_value.append(800)    
        if e >= 4000 and e < 8000:    
            graphing_value.append(900)
        if e >= 8000 and e < 22000:    
            graphing_value.append(1000)
        if e >= 22000 and e < 35000:    
            graphing_value.append(1150)    
        if e >= 35000 and e < 55000:    
            graphing_value.append(1300)    
        if e >= 55000:    
            graphing_value.append(1500)   
        
    lat_long['Total'] = graphing_value






    graphing_active = []
    
    for e in lat_long['ActiveCases']:
    
        if e < 20:
            graphing_active.append(150)
        if e >= 20 and e < 100:  
            graphing_active.append(200)
        if e >= 100 and e < 200:    
            graphing_active.append(300)
        if e >= 200 and e < 400:  
            graphing_active.append(400)
        if e >= 400 and e < 1000:    
            graphing_active.append(500)
        if e >= 1000 and e < 2000:    
            graphing_active.append(600)    
        if e >= 2000 and e < 3000:    
            graphing_active.append(700)
        if e >= 3000 and e < 4000:    
            graphing_active.append(450)    
        if e >= 4000 and e < 8000:    
            graphing_active.append(600)
        if e >= 8000 and e < 22000:    
            graphing_active.append(700)
        if e >= 22000 and e < 35000:    
            graphing_active.append(800)    
        if e >= 35000 and e < 55000:    
            graphing_active.append(1300)    
        if e >= 55000:    
            graphing_active.append(1500)   
        
    lat_long['Active'] = graphing_active
 
 
    lat_long = lat_long.fillna(0.000000)
    lat_long = lat_long.replace('\W', '')
    lat_long = lat_long.transpose() 
    lat_long = lat_long.to_dict()
    lat_long = [value for value in lat_long.values()]
    
    return lat_long




def dict_list():
    info_mongodbpairs = pd.read_csv('static/images/covid16_table.csv')
    info_mongodbpairs = info_mongodbpairs.iloc[:,1:].fillna('0')
    info_mongodbpairs = info_mongodbpairs.drop(columns=['lat', 'long'])

    info_mongodbpairs =info_mongodbpairs.rename(columns={"TotalCases": "Total Cases", "PopulationAffected": "Population Affected", "NewCases": "New Cases","NewDeaths": "New Deaths", "TotalRecovered": "Total Recovered","TotalDeaths": "Total Deaths", "ActiveCases": "Active Cases"})
    info_mongodbpairs['Population Affected'] = info_mongodbpairs['Population Affected'].round(3).astype(str) + '%'
    info_mongodbpairs['Mortality Rate'] = info_mongodbpairs['Mortality Rate'].round(2).astype(str) + '%'
    info_mongodbpairs['Cases Active'] = info_mongodbpairs['Cases Active'].round(2).astype(str) + '%'
    info_mongodbpairs['Cases Recovered'] = info_mongodbpairs['Cases Recovered'].round(2).astype(str) + '%'
    info_mongodbpairs['Population'] = (info_mongodbpairs['Population'] /1000000).round(1).astype(str) + 'M'

    info_mongodbpairs =info_mongodbpairs.rename(columns={"Population": "A) World Population","Population Affected": "A) World Population Affected",  "Total Cases": "Aa) Total Cases",  "Total Recovered": "D) Total Recovered", "Cases Recovered": "D) Percentage Recovered","Total Deaths":"G) Total Deaths", "Mortality Rate": "G) Mortality Rate", "Active Cases": "E) Active Cases","Cases Active": "E) Percentage Active", "Critical": "F) Critical Condition", "Critical": "G) Critical Condition"})

    info_mongodbpairs = info_mongodbpairs.round(3)
    info_mongodbpairs = info_mongodbpairs.drop(columns=['New Cases', 'New Deaths'])
    info_mongodbpairs =  info_mongodbpairs.sort_values(by="Country")
    list_of_dicts = []
    info_mongodbpairs = info_mongodbpairs.transpose() 
    info_mongodbpairs = info_mongodbpairs.to_dict()
    list_of_dics = [value for value in info_mongodbpairs.values()]

    list_of_dics = sorted(list_of_dics, key=lambda k: k['Country']) 

    return list_of_dics


















@app.route("/")
def home_page():
    # GET SORTED NEW CASES AND DEATHS

    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
    r = requests.get('https://www.worldometers.info/coronavirus/', headers=header)
    dfs = pd.read_html(r.text)
    covid16_table= dfs[0]
    covid16_table = covid16_table.fillna('0')
    covid16_table.rename(columns = {'Country,Other':'Country', 'Serious,Critical':'Critical'},inplace = True) 
    final_table = covid16_table


    startswithlist = []

    for i in covid16_table.NewCases:
        if "," in str(i):
            startswithlist.append(i[1:].replace(',', ''))
            
        else:
         
            startswithlist.append(i)


    covid16_table['sortingnewcases'] = startswithlist
    covid16_table['sortingnewcases'] = covid16_table['sortingnewcases'].apply(pd.to_numeric)
    sorted_newcases = covid16_table[covid16_table['sortingnewcases'] > 0 ]
    sorted_newcases = sorted_newcases.sort_values(by=['sortingnewcases'], ascending=False)

    sorted_newcases = sorted_newcases.set_index('Country')
    sorted_newcases = sorted_newcases[['NewCases', 'NewDeaths']].fillna(0)
    sorted_newcases = sorted_newcases.rename(columns={'NewCases':"Cases", "NewDeaths": "Deaths"})
    sorted_newcases = sorted_newcases.iloc[:,:]





    final_table = pd.read_csv('static/images/covid16_table.csv')
    final_table = final_table.iloc[:,1:]
    
    lengthy = len(final_table)-1
    #TotalCases
    totalcases = final_table.iloc[-1:,1:2]
    totalcases = totalcases.rename(columns={"TotalCases": "Confirmed Cases"})
    totalcases = totalcases.set_index('Confirmed Cases')

    #NewCases
    newcases =  final_table.iloc[-1:,2:3]
  
    newcases = newcases.rename(columns={"NewCases": "New Cases"})
    newcases = newcases.set_index('New Cases')
    #TotalDeaths
    totaldeaths = final_table.iloc[-1:,3:4]
    totaldeaths = totaldeaths.rename(columns={"TotalDeaths": "Total Deaths"})
    totaldeaths = totaldeaths.set_index('Total Deaths')
    #NewDeaths
    newdeaths = final_table.iloc[-1:,4:5]
    newdeaths = newdeaths.rename(columns={"NewDeaths": "New Deaths"})
    newdeaths = newdeaths.set_index('New Deaths')
    #Totalrecovered
    totalrecovered= final_table.iloc[-1:,5:6]
    totalrecovered = totalrecovered.set_index('TotalRecovered')
    #Activecases
    activecases =  final_table.iloc[-1:,6:7]
    activecases = activecases.set_index('ActiveCases')
 
    #Pop % Affected
  
    popaffected = final_table.loc[lengthy:,['PopulationAffected']].round(4).astype(str) + '%'
 
    popaffected = popaffected.rename(columns={"PopulationAffected": "Population Affected"})
    popaffected  = popaffected.set_index("Population Affected")

    #Percentage Recovered
    pctrecovered = final_table.loc[lengthy:,['Cases Recovered']].round(2).astype(str) + '%'
    pctrecovered = pctrecovered.set_index('Cases Recovered')



    #Percentage Active
    pctactive = final_table.loc[lengthy:,['Cases Active']].round(2).astype(str) + '%'
    pctactive = pctactive.set_index('Cases Active')
   #Mortality Rate %
    mortalityrate= final_table.loc[lengthy:,['Mortality Rate']].round(2).astype(str) + '%'
    mortalityrate = mortalityrate.set_index('Mortality Rate')
   
    # NEWSSSSSSSSSSSSSSSSSSSSSSSSSS

  
    page = requests.get('http://newsapi.org/v2/everything?q=Corona?Virus&from=2020-03-10&sortBy=publishedAt&apiKey=71788d9278894c70987a0a2d0e8c6120')
    page = page.json()


    articlesource = []
    articletitle = []
    articleimage = []
    articlewhen = []
    articleurl = []
    for e in range(4):
        articlesource.append(page['articles'][e]['source']['name'])
        articletitle.append(page['articles'][e]['title'])
        articleurl.append(page['articles'][e]['url'])
        articleimage.append(page['articles'][e]['urlToImage'])
        articlewhen.append(page['articles'][e]['publishedAt'])
        
    dictionary1= {'articlesource': articlesource[0], 'title': articletitle[0], 'img_url':articleurl[0], 'articleimage': articleimage[0], 'articlewhen':articlewhen[0] }
    dictionary2= {'articlesource': articlesource[1], 'title': articletitle[1], 'img_url':articleurl[1], 'articleimage': articleimage[1], 'articlewhen':articlewhen[1] }    
    dictionary3= {'articlesource': articlesource[2], 'title': articletitle[2], 'img_url':articleurl[2], 'articleimage': articleimage[2], 'articlewhen':articlewhen[2] }
    dictionary4= {'articlesource': articlesource[3], 'title': articletitle[3], 'img_url':articleurl[3], 'articleimage': articleimage[3], 'articlewhen':articlewhen[3] }


    mydictlisty = [dictionary1,dictionary2]

  
    return render_template("index.html", mydictlisty = mydictlisty, dictionary1 = dictionary1, dictionary2= dictionary2,dictionary3= dictionary3, dictionary4= dictionary4, sorted_totals =sorted_totals.to_html(), sorted_newcases = sorted_newcases.to_html(), totalcases = totalcases.to_html(), newdeaths = newdeaths.to_html(),newcases=newcases.to_html(), totaldeaths=totaldeaths.to_html(), totalrecovered = totalrecovered.to_html(), activecases = activecases.to_html(), popaffected = popaffected.to_html(), pctrecovered = pctrecovered.to_html(), pctactive = pctactive.to_html(), mortalityrate = mortalityrate.to_html())


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


