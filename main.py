from poloniex import PoloniexExtendedAPI
import json

def pp(print_me_pretty):
    """
    Pretty Print JSON return.

    :param print_me_pretty: Input the return-value of the API queries to just pretty print the JSON return
    :return:
    """
    json_pretty = json.dumps(print_me_pretty, sort_keys=True, indent=2, separators=(',', ': '))
    return json_pretty


def main():
    # Create wrapper object
    polo = PoloniexExtendedAPI()

    # How to call from core API
    # -------------------------

    vol = polo.api_query('return24hVolume').json()
    print(pp(vol))

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
