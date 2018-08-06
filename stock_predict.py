## Model I will work with in the future for stock analysis
## I plan on building it as a classifier, with the classes being 'Buy', 'Hold', and 'Sell' initially
## Later on I might improve this to specifically predict stock prices.
## However, I'm not confident in this, as predicting future stocks is incredibly complex,
## as shown by the Efficient Market Hypothesis

import quandl
from pandas_datareader import data as web
import datetime as dt
import numpy as np
import pandas as pd
from sklearn import mixture as mix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import fix_yahoo_finance

def stock_predict(ticker):
    ## Chose to start from 1995, default end is today's date
    #df = web.get_data_yahoo(ticker, start='1995-01-01')

    today = dt.date.today()
    one_year = dt.timedelta(days=365)
    one_year_ago = today - one_year

    quandl.ApiConfig.api_key = 'khgNVC9qySoZyPshAWaw'
    data_df = quandl.get('WIKI/' + ticker, start_date=str(one_year_ago), end_date=str(today))
    data_price = data_df['Close'].values
    data_np = data_df.values
    #print(data_price)
    #print(data_price[0])


    z_data = quandl.get_table('ZACKS/FC', ticker='AAPL')
    print(z_data)

    #data_price.plot();
    #plt.show()

    #period = 50
    #train = 0.8
    #split = int(train*len(df))

if __name__ == '__main__':
    stock_predict('AAPL')
