# Poloniex API Wrapper according to https://poloniex.com/support/api/

import os
import json
import requests
import hmac
import hashlib
import time
import datetime
import urllib.parse


class PoloniexCoreAPI:

    """
    Core API - Basic API Wrapper-Class for public and private API-Calls
    """

    def __init__(self):
        """
        Constructor: Initialize an object with private apikey secrets etc.
        """
        self.__config = None
        if os.path.isfile('poloniex.config'):
            with open('poloniex.config', 'r') as configfile:
                self.__config = json.load(configfile)
        self.__url_public = 'https://poloniex.com/public'
        self.__url_trading = 'https://poloniex.com/tradingApi'

        # Variables for API-Call-Limit Checker
        self.__now = time.time()
        self.__count = 0

    def getconfig(self):
        return self.__config

    def checklimit(self):
        """
        Helper to not exceed API call limit. (Not used atm.)
        This function could be called everytime right before sending the request to ensure not to exceed the API limit
        :return: True if limit not exceeded, False otherwise
        """

        timeframe = 1
        max_apicalls = 6

        if (time.time() - self.__now) >= timeframe:
            self.__now = time.time()
            self.__count = 1
            return True
        else:
            self.__count += 1
            if self.__count <= max_apicalls:
                return True
            else:
                return False

    def api_query(self, command, params={}):
        """
        Public and private API methods
        :param command: Public or private command
        :param params: POST Paramter according to methods listed at https://poloniex.com/support/api/
        :return: JSON Objects
        """

        command_public = ['returnTicker',
                          'return24hVolume',
                          'returnOrderBook',
                          'returnMarketTradeHistory',
                          'returnChartData',
                          'returnCurrencies',
                          'returnLoanOrders'
                          ]

        command_private = ['returnBalances',
                           'returnCompleteBalances',
                           'returnDepositAddresses',
                           'generateNewAddress',
                           'returnDepositsWithdrawals',
                           'returnOpenOrders',
                           'returnTradeHistory',
                           'returnOrderTrades',
                           'buy',
                           'sell',
                           'cancelOrder',
                           'moveOrder',
                           'withdraw',
                           'returnFeeInfo',
                           'returnAvailableAccountBalances',
                           'returnTradableBalances',
                           'transferBalance',
                           'returnMarginAccountSummary',
                           'marginBuy',
                           'marginSell',
                           'getMarginPosition',
                           'closeMarginPosition',
                           'createLoanOffer',
                           'cancelLoanOffer',
                           'returnOpenLoanOffers',
                           'returnActiveLoans',
                           'toggleAutoRenew'
                           ]

        default_params = {
            'nonce': int(time.time() * 1000000),
            'command': command
        }
        params.update(default_params)

        # Trading / Private API Requests
        if command in command_private:
            if self.__config is None:
                print('Specify API-Key and Secret first.')
                return

            # Sign POST data for authentication
            params_encoded = urllib.parse.urlencode(params).encode('ascii')
            sign = hmac.new(self.__config['secret'].encode('ascii'), params_encoded, hashlib.sha512).hexdigest()
            headers = {
                'Key': self.__config['API key'],
                'Sign': sign
            }
            r = requests.post(self.__url_trading, data=params, headers=headers)
            return r

        # Trading / Public API Requests
        elif command in command_public:
            params.pop('nonce')
            if command == 'returnMarketTradeHistory':
                params['command'] = 'returnTradeHistory'
            r = requests.get(self.__url_public, params)
            return r

        else:
            print('API command does not exist!')


class PoloniexExtendedAPI(PoloniexCoreAPI):

    """
    Extend CoreAPI queries to be more human friendly
    """

    def getticker(self, currencypair='all'):
        """
        Public API method -
        Return all currenciy pairs or one selected pair from the standard ticker as JSON

        :param currencypair: BTC_ETH, BTC_1CR ... or 'all' ('all' is default)
        :return: s.a.
        """
        try:
            if currencypair == 'all':
                return super().api_query('returnTicker').json()
            else:
                return super().api_query('returnTicker').json()[currencypair]

        except KeyError:
            print('Currency pair does not exist.')

    def getchartdata(self, currencypair, period, start, end='now', polotime=True):
        """
        Public API method -
        Returns candle stick chartdata as JSON.

        :param currencypair: i.e.: BTC_XMR
        :param period: 5m, 15m, 30m, 2h, 4h or 1d
        :param start: Date format %Y-%m-%d %H:%M:%S (example: '2017-01-13 09:17:08')
        :param end: same as param 'start' or now (now is default)
        :param polotime: Time +2h as displayed in charts window on Poloniex website = True (default), False = UTC
        :return: chartdata as JSON
        """

        # Convert a human readable date to unix timestamp format
        start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S').timestamp()

        # Get chartdata until now
        if end == 'now':
            end = 9999999999
        else:
            end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S').timestamp()

        if end < start:
            print('Endtime can not be earlier than starttime!')
            return

        # +2h timezone for poloniex
        if polotime:
            start += 7200
            end += 7200

        # human readable period times instead of seconds
        p = {'5m': 300,
             '15m': 900,
             '30m': 1800,
             '2h': 7200,
             '4h': 14400,
             '1d': 86400}

        if period in p.keys():
            period = p[period]
        else:
            print('Period format wrong or does not exist!')
            return

        # Make actual API request via CoreAPI function
        chartdata = super().api_query('returnChartData', params={'currencyPair': currencypair, 'period': period,
                                                                 'start': start, 'end': end}).json()
        return chartdata

    def getbalances(self, currency):
        """
        Private API method -
        Returns all balances in JSON format.

        :param currency: specific currency like 'DASH' or 'ETH' or 'all'
        :return: s.a.
        """
        if super().getconfig() is None:
            print('Specify API-Key and Secret first.')
            return {'error': 'Specify API-Key and Secret first.'}

        try:
            balances = super().api_query('returnCompleteBalances').json()
            if currency == 'all':
                return balances
            else:
                return balances[currency]
        except KeyError:
            print('Currency not listed.')

    def gettradehistory(self, currencypair='all', start='regdate', end='now'):
        """
        Private API method -
        Returns tradehistory as JSON

        :param currencypair: i.e.: 'BTC_XMR' or 'all' ('all' is default)
        :param start: Date format %Y-%m-%d %H:%M:%S (example: '2017-01-13 09:17:08') or 'regdate' (regdate is default)
        :param end: same as param 'start' or 'now' ('now' is default)
        :return: s.a.
        """

        config = super().getconfig()
        if config is None:
            print('Specify API-Key and Secret first.')
            return {'error': 'Specify API-Key and Secret first.'}

        if start == 'regdate':
            regdate = config.get('registration date')
            if regdate is None:
                print('No registration date specified in config file.')
                return {'error': 'No registration date specified in config file.'}
            else:
                start = datetime.datetime.strptime(config['registration date'], '%Y-%m-%d').timestamp()
        else:
            start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S').timestamp()

        if end == 'now':
            end = 9999999999
        else:
            end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S').timestamp()

        if end < start:
            print('Endtime can not be earlier than starttime!')
            return

        tradehistory = super().api_query('returnTradeHistory', params={'currencyPair': currencypair,
                                                                       'start': start, 'end': end, 'limit': 10000}).json()
        return tradehistory


    def placeorder(self, ordertype, currency, rate=0, amount=0, orderrestriction='None'):
        """

        Private API method -
        Place an order

        :param ordertype: 'buy' or 'sell'
        :param currency:
        :param rate:
        :param amount:
        :param orderrestriction:
        :return:
        """

        if ordertype != 'buy' and ordertype != 'sell':
            return {'error': 'Unknown ordertype.'}

        if rate == 0 or amount == 0 or rate * amount < 0.0001:
            return {'error': 'Total must be at least 0.0001.'}
        if rate * amount > 5:
            return {'error': 'Max. total limited to 5 BTC.'}

        currencypair = 'BTC_{}'.format(currency)
        params = {'currencyPair': currencypair, 'rate': rate, 'amount': amount}
        if orderrestriction != 'fillOrKill' and orderrestriction != 'immediateOrCancel' \
                and orderrestriction != 'postOnly' and orderrestriction != 'None':
            return {'error': 'Orderrestriction does not exist.'}
        else:
            params.update({orderrestriction: 1})
            if params.get('None'):
                params.pop('None')
        ordernumber = super().api_query(ordertype, params=params)
        return ordernumber.json()

    def cancelorder(self, ordernumber):
        """
        Private API method -
        Cancel an order

        :param ordernumber:
        :return:
        """
        return super().api_query('cancelOrder', params={'orderNumber': ordernumber}).json()

    def returnopenorders(self, currency):
        """
        Private API method -
        Return all open orders
        :param currency:
        :return:
        """
        currencypair = 'BTC_{}'.format(currency)
        return super().api_query('returnOpenOrders', params={'currencyPair': currencypair})