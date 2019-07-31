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
    data, metadata = ts.get_daily(symbol=ticker, outputsize='full')

    data.columns = ['open', 'high', 'low', 'close', 'volume']
    data = data.iloc[::-1]
    print(data.head())

    data['close'].plot()
    plt.show()
