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

## enum for vuy and sell orders
class Transaction(Enum):
    """enum for buy/sell orders"""
    BUY = 'buy'
    SELL = 'sell'

## Build Robinhood class
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

    instruments_cache = {}

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
                self.rh_endpoints['login'],
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




    def get_instrument(self, symbol):
        if not symbol in self.instruments_cache:
            instruments = trader.instruments(symbol)
            for instrument in instruments:
                self.add_instrument(instrument['url'], instrument['symbol'])

        url = ''
        if symbol in self.instruments_cache:
            url = self.instruments_cache[symbol]

        return { 'symbol': symbol, 'url': url }



    def show_stock(self):
        ## Show a specific stock
        print('Stock')

        while True:

            stay = input("Look at another stock? (y/n) ")
            if stay == 'y' or stay == 'Y': continue
            else: time.sleep(1); break



    ## Method used for buying stocks.
    ## Ask for ticker, show current price, and ask how many stocks they would like to buy
    ## Built so that user must enter twice that they would like to buy to ensure transaction
    def buy_stock(self):
        ## Buy stock
        #print('Buy')
        print('\x1b[2J\x1b[H') # Escape sequence to clear screen
        print("Welcome to the page where you can buy stock!\n")

        while True:
            ticker = input("Enter the ticker for the stock you would like to buy: ")

            transaction = Transaction.BUY
            ## For now only doing market buys. May implement limit buys later
            order = 'market'

            stock_instrument = self.get_instrument(ticker)
            if not stock_instrument['url']:
                print("Stock cannot be found or cannot be bought.")
                print("Leaving transaction page.")
                time.sleep(1)
                return

            transaction = Transaction(transaction)
            price = self.quote_data(instrument['symbol'])['bid_price']

            print("Current price is $" + str(price))
            cont_trans = input("Continue with transaction at this price? (y/n) ")
            if cont_trans != 'y' or cont_trans != 'Y':
                if cont_trans == 'n' or cont_trans == 'N':
                    print("\nLeaving transaction page.")
                    time.sleep(1)
                    return
                else:
                    print("\nInvalid character entered")
                    print("Leaving transaction page")
                    time.sleep(1)
                    return

            num_shares = input("How many shares would you like to purchase? (whole number only) ")
            if not num_shares.isdigit():
                print("\nInvalid character entered")
                print("Leaving transaction page")
                time.sleep(1)
                return
            num_shares = int(num_shares)

            payload = {
                'account': self.get_account()['url'],
                'instrument': unquote(instrument['url']),
                'price': float(price),
                'quantity': num_shares,
                'side': transaction.name.lower(),
                'symbol': instrument['symbol'],
                'time_in_force': time_in_force.lower(),
                'trigger': 'immediate',
                'type': order.lower()
            }

            trade = self.session.post(self.rh_endpoints['orders'],
                                        data=payload)
            if not (trade.status_code == 200 or trade.status_code == 201):
                print("Error executing order")
                try:
                    data = trade.json()
                    if 'detail' in data:
                        print(data['detail'])
                except:
                    pass
            else:
                print("\nDone\n\n")

            stay = input("Buy another stock? (y/n) ")
            if stay == 'y' or stay == 'Y': continue
            else: time.sleep(1); return



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
        print("Welcome to my command line Robinhood Trader! Try it out and give any feedback you have to my github page!\n\n")
        if not trader.login_request():
            print("Incorrect username or password entered. Ending session.")
            time.sleep(3)
            break
        print('\x1b[2J\x1b[H') # Escape sequence to clear screen

        print("Welcome to my command line Robinhood Trader! Try it out and give any feedback you have to my github page!\n\n")
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
