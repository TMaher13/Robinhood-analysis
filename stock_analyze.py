## Script for running analysis on a user-input stock.
## Extend of analysis will be updated on going forward.
## To start it will look at historical data
## Goal is to eventually build an AI model
## to predict possible movements for a stock in the future


import sys
import numpy as np
import pandas as pd
import quandl
from stocker import Stocker
import time

iex_endpoint = "https://api.iextrading.com/1.0"

def get_stock():
    ticker = input("Enter ticker symbol: ")

    return ticker


def stock_info():
    ## Get historical data on stock
    ##print("Data provided for free by IEX. \nView IEX’s Terms of Use at https://iextrading.com/api-exhibit-a/")

    ticker = get_stock()

    try:
        stock = Stocker(ticker)
    except:
        print("Ticker not found.")

    print("\n\nGeneral info on historical data of stock and movement in the past\n\n")
    time.sleep(5)
    stock.plot_stock()

    ## Object to return for predictive model
    #stock_obj =

    return stock


def stock_ml_pred(stock):
    print("Now running model to predict future stock movements\n\n")

    print("\n\nThis next plot shows the untrained predictions.\nAfter closing this graph, we will train the data.\n\n")
    time.sleep(10)
    stock.changepoint_prior_analysis(changepoint_priors=[0.001, 0.05, 0.1, 0.2])

    print("\n\nThe next plot shows the trained and tested data. \nCheck to see how well tested data went, then close the graph and continue to prediciton for next year.")
    print("Use zoom as needed to see what the model predicts.")
    print("Due to nature of quandl data, some of 'future' data is already in the past (give or take 3 months).\nUse this to test if the  predicition produces legitimate results.\n\n")
    time.sleep(15)
    stock.evaluate_prediction()


    stock.predict_future(days=365)



if __name__ == "__main__":
    print("This module gathers stock data and analyzes it for personal use. \nIt uses the quandl database, which can be found here: https://www.quandl.com/")
    print("The Stocker toolkit used can be found here: https://github.com/WillKoehrsen/Data-Analysis/tree/master/stocker")
    print("Any predictions made are not guarentees of success, and should be taken only as suggestions.\n")
    print("To run this analysis, a quandl account is needed. \nIf you do not have one, go to the quandl link above and create an account.")
    print("To get your API key, sign in to your quandl account and go to the following link: https://www.quandl.com/account/api")
    quandl_key = input("To start, enter your quandl API key:")

    ## Sets quandl API key so we can make database calls
    quandl.ApiConfig.api_key = quandl_key
    print('\n')
    stock = stock_info()

    stock_ml_pred(stock)
