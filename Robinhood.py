## Script with utilities to work with Robinhood API
## Future updates will allow for buy and selling of stocks
## Thomas Maher
## 7/31/18

import getpass
import logging
import warnings
from enum import Enum

import os
import requests
import six
from six.moves.urllib.parse import unquote
from six.moves.urllib.request import getproxies
from six.moves import input
import time
import subprocess

from config import USERNAME, PASSWORD

## To allow for escape sequence to clear screen between implementation loops
import colorama
colorama.init()


## Build robinhood class
class Robinhood:
    ## Wrapper for fetching and parsing Robinhood endpoints
    rh_endpoints = {
        "login": "https://api.robinhood.com/oauth2/token/",
        "logout": "https://api.robinhood.com/api-token-logout/",
        "investment_profile": "https://api.robinhood.com/user/investment_profile/",
        "accounts": "https://api.robinhood.com/accounts/",
        "ach_iav_auth": "https://api.robinhood.com/ach/iav/auth/",
        "ach_relationships": "https://api.robinhood.com/ach/relationships/",
        "ach_transfers": "https://api.robinhood.com/ach/transfers/",
        "applications": "https://api.robinhood.com/applications/",
        "dividends": "https://api.robinhood.com/dividends/",
        "edocuments": "https://api.robinhood.com/documents/",
        "instruments": "https://api.robinhood.com/instruments/",
        "instruments_popularity": "https://api.robinhood.com/instruments/popularity/",
        "margin_upgrades": "https://api.robinhood.com/margin/upgrades/",
        "markets": "https://api.robinhood.com/markets/",
        "notifications": "https://api.robinhood.com/notifications/",
        "options_positions": "https://api.robinhood.com/options/positions/",
        "orders": "https://api.robinhood.com/orders/",
        "password_reset": "https://api.robinhood.com/password_reset/request/",
        "portfolios": "https://api.robinhood.com/portfolios/",
        "positions": "https://api.robinhood.com/positions/",
        "quotes": "https://api.robinhood.com/quotes/",
        "historicals": "https://api.robinhood.com/quotes/historicals/",
        "document_requests": "https://api.robinhood.com/upload/document_requests/",
        "user": "https://api.robinhood.com/user/",
        "watchlists": "https://api.robinhood.com/watchlists/",
        "news": "https://api.robinhood.com/midlands/news/",
        "ratings": "https://api.robinhood.com/midlands/ratings/",
        "fundamentals": "https://api.robinhood.com/fundamentals/",
        "options": "https://api.robinhood.com/options/",
        "marketdata": "https://api.robinhood.com/marketdata/"
    }

    ## Initialize account info
    session = None
    username = None
    password = None
    headers = None
    auth_token = None

    logger = logging.getLogger('Robinhood')
    logger.addHandler(logging.NullHandler())

    ## Constructor
    def __init__(self):
        self.session = requests.session()
        self.session.proxies = getproxies()

        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en;q=1",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Robinhood-API-Version": "1.0.0",
            "Connection": "keep-alive",
            "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)",
            "Origin": "https://robinhood.com"
        }
        self.session.headers = self.headers

    def login_request(self):
        username = input("Enter your username: ")
        password = getpass.getpass()
        return self.login(username=username, password=password)

    def login(self, username, password, mfa_code=None):
        self.username = username
        self.password = password

        ## Authentication set to expire after 1 hour, may change later depending on preference
        payload = {
            'password': self.password,
            'username': self.username,
            'scope': 'internal',
            'grant_type': 'password',
            'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
            'expires_in': 3600
        }

        if mfa_code:
            payload['mfa_code'] = mfa_code


        try:
            res = self.session.post(
                self.endpoints['login'],
                data=payload
            )
            res.raise_for_status()
            data = res.json()
        except requests.exceptions.HTTPError:

            raise RH_exception.LoginFailed()


        if 'mfa_required' in data.keys():           #pragma: no cover
            raise RH_exception.TwoFactorRequired()  #requires a second call to enable 2FA

        if 'access_token' in data.keys():
            self.auth_token = data['access_token']
            self.headers['Authorization'] = 'Bearer ' + self.auth_token
            return True

        return False

    def logout(self):

        try:
            request = self.session.ppost(self.endpoints['logout'])
            request.raise_for_status()
            data = resolve
            return data
        except:
            print("\nAlready logged out.")

    def show_portfolio(self):
        ## Show portfolio
        while True:
            print('\x1b[2J\x1b[H') # Escape sequence to clear screen
            print("Welcome to your portfolio page!")

            leave = input("Exit back to home page? (y/n) ")
            if leave == 'y' or leave == 'Y': time.sleep(1); break
            else: continue

    def show_stock(self):
        ## Show a specific stock
        print('Stock')

        while True:

            stay = input("Look at another stock? (y/n) ")
            if stay == 'y' or stay == 'Y': continue
            else: time.sleep(1); break

    def buy_stock(self):
        ## Buy stock
        #print('Buy')
        print('\x1b[2J\x1b[H') # Escape sequence to clear screen
        print("Welcome to the page where you can buy stock!\n")
        ticker = input("Enter the ticker for the stock you would like to buy: ")

        transaction = Transaction.BUY
        stock_instrument = self.get_instrument(ticker)
        if not stock_instrument['url']:
            print("Stock cannot be found.")
            print("Leaving transaction page.")
            time.sleep(1)
            return

        while True:


            stay = input("Buy another stock? (y/n) ")
            if stay == 'y' or stay == 'Y': continue
            else: time.sleep(1); break

    def sell_stock(self):
        ## Sell stock
        print('Sell')

        while True:


            stay = input("Sell another stock? (y/n) ")
            if stay == 'y' or stay == 'Y': continue
            else: time.sleep(1); break


if __name__ == '__main__':
    ## Initialize trader
    trader = Robinhood()
    #bashCommand = str(printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -)
    while True:
        #os.system('cls' if os.name == 'nt' else 'clear')
        print('\x1b[2J\x1b[H') # Escape sequence to clear screen

        #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #output, error = process.communicate()
        print("=" * 105)
        print("Welcome to my command line Robinhood Trader! Try it out and give any feedback you have to my github page!\n")
        print("There are 5 things you can do:")
        print("\t1) To look at your stock portfolio, type 'portfolio'")
        print("\t2) To look at a specific stock, type 'stock'")
        print("\t3) To buy stocks, type 'buy'")
        print("\t4) To sell stocks, type 'sell'")
        print("\t5) To end your session, type 'end'\n")

        command = str(input("What do you want to do? "))

        if command == 'portfolio' or command =='Portfolio':
            trader.show_portfolio()
        elif command == 'stock' or command == 'Stock':
            trader.show_stock()
        elif command == 'buy' or command == 'Buy':
            trader.buy_stock()
        elif command == 'sell' or command == 'Sell':
            trader.sell_stock()
        elif command == 'end' or command == 'End':
            trader.logout()
            print("Thanks for using my project!")
            time.sleep(3)
            print('\x1b[2J\x1b[H') # Escape sequence to clear screen
            break
        else:
            print("\nDid not enter a correct command.\nEnding session.")
            time.sleep(3)
            print('\x1b[2J\x1b[H') # Escape sequence to clear screen
            break
