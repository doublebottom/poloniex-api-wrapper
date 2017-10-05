# poloniex-api-wrapper
A Python 3 wrapper for the trading API of poloniex.com 

https://www.poloniex.com
https://poloniex.com/support/api/

Use it on your own risk!

## Install

#### Python Version
Python >= 3.5 recommended.

Install Miniconda from https://conda.io/miniconda.html.
1. Open a terminal an create a virtual environment
  
       conda create -n poloniex python=3
2. Activate environment

       source activate poloniex
3. Install requests

       pip install requests
4. Clone or download this repo

## Configuration 

Go to the Poloniex website and create an API-Key.
Replace 'API key', 'secret' and 'registration date' with your own codes. The config file contains example keys only they are only for demonstartion on how the config should look like. The registration date is needed if you want to use a few methods from the PoloniexExtended API (i.e. to get your full trade history).

If you are only interested in the public methods delete or rename the 'poloniex.config' file.

## Usage

The easiest way to get an idea on how this wrapper works is probably to open 'main.py' uncomment step by step some of the examples and run it.

In generall there are just two classes. The PoloniexCoreAPI class and the PoloniexExtendedAPI class. You can do all the queries with the CoreAPI itself, but for some more human friendly usage I created a derivated class (ExtendedAPI) with some methods on top of the core class. 

To use both the CoreAPI and the ExtendedAPI just create an object of the ExtendedAPI class and fire up the request like so:

     polo = PoloniexExtendedAPI()
     orderbook = polo.api_query('returnOrderBook', params={'currencyPair': 'BTC_BLK', 'depth': '10'}).json()

Put in every API-method and corresponding key-value pair from the Poloniex API documentation (s.a.) 
Syntax is just: var = polo.api_query('API-Method', params={'key1': 'value1', 'key2': 'value2', ...}).json()

The Extended API methods makes it easier to deal with i.e. date formats. Have a look at the description in the docstrings in 'poloniex.py'.
        

  
