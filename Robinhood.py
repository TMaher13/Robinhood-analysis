## Script with utilities to work with Robinhood API
## Future updates will allow for buy and selling of stocks
## Thomas Maher
## 7/31/18

 import getpass
 import logging
 import warnings
 from enum import Enum

import requests
import six
from six.moves.urllib.parse import unquote
from six.moves.urllib.request import getproxies
from six.moves import input
import exceptions as RH_exception

from config import USERNAME, PASSWORD


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
