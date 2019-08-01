## Script for seeing price action indicators for a stock
import os, sys
import pandas as pd
import numpy as np
import pandas_datareader.data as web
from datetime import datetime
import json
from tabulate import tabulate

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt


def get_1_day(timestamp, data):
    try:
        return data.loc[timestamp]
    except:
        print("No data found for this day")


def get_1_year(timestamp, data):
    print("1 year support not defined.")


def what_kind_of_data(data):
    """
        Ask the user what kind of data they want. Supported options are:

            - Single day data
    """
    request = input("What kind of data are you looking for?\n" +
          "\t- For single-day data, submit \"1day\"" +
          "\n\t- For 1 year data, submit \"1year\"" +
          "\nEnter request: ")

    if(request == '1day'):
        day = input("Enter day to get data for (YYYY-MM-DD): ")
        print("Data for " + day + ":\n", get_1_day(day, data))
    else:
        print("Incorrect data entry. Exiting.")
    #elif(request == '1year')


if __name__ == "__main__":
    if not os.path.exists("stored_key.txt"):
        print("To start, get an API key from Alpha Vantage at https://www.alphavantage.co/support/#api-key")

        with open("stored_key.txt", "w+") as f:
            API_key = input("Enter your Alpha Vantage API key: ")
            f.write(API_key)
        print("API key stored in stored_key.txt file.\n" +
              "To update your API key just change the contents of the file.\n")

    with open("stored_key.txt", "r") as file:
        key = file.read()


    ticker = input("Enter the ticker for the desired company: ")

    ts = TimeSeries(key=key, output_format='pandas')

    # Returns data as json objects
    data, metadata = ts.get_daily_adjusted(symbol=ticker, outputsize='full')

    #data.columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume', 'div_amount', 'split_coef']
    data = data.iloc[::-1]
    #print(data.head())
    #print("Days of data collected: ", len(data.index))
    what_kind_of_data(data)


    #print(data.loc['1998-01-02'])
    #data['adj_close'].plot()
    #plt.show()
