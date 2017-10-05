from poloniex import PoloniexExtendedAPI
from helper import *


def main():
    # Create wrapper object
    polo = PoloniexExtendedAPI()

    # How to call from core API
    # -------------------------

    # vol = polo.api_query('return24hVolume').json()
    # print(pp(vol))

    # orderbook = polo.api_query('returnOrderBook', params={'currencyPair': 'BTC_BLK', 'depth': '10'}).json()
    # print(pp(orderbook))

    # How to call from Extended API
    # -----------------------------

    # ticker = polo.getticker('ETH_GNT')
    # print(pp(ticker))

    # ticker = polo.getticker('all')
    # print(pp(ticker))

    # ohlc_data = polo.getchartdata('BTC_ETH', '1d', '2017-01-01 00:00:00', polotime=True)
    # print(pp(ohlc_data))

    # tradehistory = polo.gettradehistory(currencypair='BTC_XMR', start='regdate', end='now')
    # print(pp(tradehistory))

    # balances = polo.getbalances('ETH')
    # print(pp(balances))

    # Trading
    # -------

    # ordernumber = polo.placeorder('sell', 'ETH', rate=0.113, amount=0.00000625, orderrestriction='postOnly')
    # print(ordernumber)

    # openorders = polo.returnopenorders('DASH')
    # print(openorders)

    # cancel = polo.cancelorder(order)


if __name__ == '__main__':
    main()
