import datetime as dt
from datetime import date
from datetime import datetime
from dateutil.rrule import rrule, DAILY
from dateutil import parser
import pandas as pd
import os
import math

def getCountries(currencyName):
    countries = os.listdir(currencyName + "_data")
    for i in range(0, len(countries)):
        countries[i] = countries[i][:-4] #remove file extension
    return countries

def getGDPData(country):
    
    df = pd.read_csv("shared_gdp_data\\" + country + ".csv", index_col = 1, names = ['Country', 'GDP']);
    return df

def getForexData(country, currencyName):
     
    df = pd.read_csv(currencyName + "_data\\" + country + ".csv", names = ['Date', 'Price']);
    df = getForexDataChange(df)
    df.set_index('Date', inplace = True)
    
    return df

def getForexDataChange(df):
    
    changes = [1.0];
    
    for i in range(0, len(df['Price']) - 1):
        change = float(df['Price'].iloc[i + 1]) / float(df['Price'].iloc[i])
        changes.append(change)
    
    df['Change'] = pd.Series(changes, index=df.index)
    return df

def getIndexChanges(forex, gdp):
    
    dateTimes = []
    indexChanges = []
    
    gdp.drop(gdp.tail(1).index,inplace=True)
    
    #Loop through every day
    for dateTime in rrule(DAILY, dtstart=dt.datetime(2003, 12, 1), until=dt.datetime(2017, 10, 23)):
        
        dtStr = str(dateTime.year).zfill(4) + "-" + str(dateTime.month).zfill(2) + "-" + str(dateTime.day).zfill(2)
        
        if(dtStr in forex.index):
            
            dateTimes.append(dateTime)
            
            year = dateTime.year;
            if year == 2017:
                year = 2016
            indexChanges.append(calculateWeightedGeometricMean(forex.loc[dtStr], gdp.loc[str(year)]))
        
    df = pd.DataFrame({'Date' : dateTimes, 'Change': indexChanges})
    return df

def calculateWeightedGeometricMean(forex, gdp):
    
    a = 1;
    
    #Loop through every country/currency
    for i in range(0, len(forex)):
        
        #clean data  
        try:
            val = float(forex.iloc[i])
        except ValueError:
            forex.iloc[i] = '1'
            
        if forex.iloc[i] == '0':
            forex.iloc[i] = '1';
        if(math.isnan(float(forex.iloc[i]))):
            forex.iloc[i] = '1'
        
        try:
            val = float(gdp.iloc[i])
        except ValueError:
            gdp.iloc[i] = '1'
            
        if gdp.iloc[i] == '0':
            gdp.iloc[i] = '1';
        if(math.isnan(float(gdp.iloc[i]))):
            gdp.iloc[i] = '1'
        
        a = a * pow(float(forex.iloc[i]), float(gdp.iloc[i]) / 1000000000000.0) #divide 1,000,000,000,000 1 trillion
        
    a = pow(a, 1 / calculateSumOfGDP(gdp))
    
    return a
        
def calculateSumOfGDP(gdps):
    
    a = 0.0
    
    for gdp in gdps:
        if not (math.isnan(float(gdp))):
            a = a + float(gdp)
        
    return a / 1000000000000.0

def getIndex(indexChanges):
    
    indices = []
    index = 100.0
    
    for i in range(0, len(indexChanges)):
        
        #Clean data
        if indexChanges['Change'].iloc[i] != indexChanges['Change'].iloc[i]:
            indexChanges['Change'].iloc[i] = 1.0
        
        index = index * indexChanges['Change'].iloc[i]
        indices.append([indexChanges['Date'].iloc[i], index])
        
    return indices

print("Enter the currency code (eg. SGD)")
currencyName = input()
countries = getCountries(currencyName)

gdpAllDf = pd.DataFrame()
forexAllDf = pd.DataFrame()

for i in range(0, len(countries)):
    
    gdpDf = getGDPData(countries[i])
    gdpDf = gdpDf.iloc[::-1] #Reverse, to be in ascending date
    forexDf = getForexData(countries[i], currencyName)
    
    gdpAllDf[countries[i]] = gdpDf['GDP'];
    forexAllDf[countries[i]] = forexDf['Change'];
    
indexChanges = getIndexChanges(forexAllDf, gdpAllDf)

indices = getIndex(indexChanges)

df = pd.DataFrame(indices);
df.to_csv(currencyName + '_Index.csv');
    
    
    
    
    
   


