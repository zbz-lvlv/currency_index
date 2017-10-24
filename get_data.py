import datetime as dt
import pandas_datareader.data as web
from pandas_datareader import wb
import os

tickers = ['USD=X',
           'EUR=X',
           'CNY=X',
           'JPY=X',
           'GBP=X',
           'INR=X',
           'BRL=X',
           'CAD=X',
           'RUB=X',
           'AUD=X',
           'MXN=X',
           'IDR=X',
           'TRY=X',
           'CHF=X',
           'SAR=X',
           'ARS=X',
           'SEK=X',
           'THB=X',
           'NGN=X',
           'IRR=X']

successfulTickers = []

countries = ['US',
             'EU',
             'CN',
             'JP',
             'GB',
             'IN',
             'BR',
             'CA',
             'RU',
             'AU',
             'MX',
             'ID',
             'TR',
             'CH',
             'SA',
             'AR',
             'SE',
             'TH',
             'NG',
             'IR']

successfulCountries = []

def getForexData(startDate, endDate, ticker):
    df = web.DataReader(ticker, 'yahoo', startDate, endDate);
    return df['Adj Close']

def getGDPData(startYear, endYear, country):
    df = wb.download(indicator='NY.GDP.MKTP.KD', country=[country], start=startYear, end=endYear)
    return df

print("Enter the currency code (eg. SGD)")
currencyCode = input();

if not os.path.exists(currencyCode + "_data"):
    os.makedirs(currencyCode + "_data")
    
if not os.path.exists("shared_gdp_data"):
    os.makedirs("shared_gdp_data")

for i in range(0, len(tickers)):
    
    tickers[i] = currencyCode + tickers[i];
    
    try:
        dfForex = getForexData(dt.datetime(2003, 12, 1), dt.datetime(2017, 10, 23), tickers[i]);
        dfForex.to_csv(currencyCode + "_data\\" + countries[i] + ".csv");
        
        dfGdp = getGDPData(2003, 2016, countries[i])
        dfGdp.to_csv("shared_gdp_data\\" + countries[i] + ".csv");
        
    except Exception: 
       print(tickers[i]);
       