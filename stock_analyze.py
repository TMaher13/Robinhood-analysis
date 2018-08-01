## Script for running analysis on a user-input stock.
## Extend of analysis will be updated on going forward.
## To start it will look at historical data
## Goal is to eventually build an AI model
## to predict possible movements for a stock in the future

## Data is gathered from the IEX API

import sys

iex_endpoint = "https://api.iextrading.com/1.0"

def get_stock():
    ticker = input("Enter ticker symbol: ")

    return ticker


def stock_info(ticker):
    ## Get historical data on stock
    print("Data provided for free by IEX. \nView IEX’s Terms of Use at https://iextrading.com/api-exhibit-a/")



if __name__ == "__main__":
