try:
    from urllib.request import Request, urlopen  # Python 3
except:
    from urllib2 import Request, urlopen  # Python 2
import json
import logging as log
import time


class TradeService(object):
    API_KEY = 'b80a447d-ef2c-4d44-978a-8309be7026de'
    WALLET_URL = 'https://hft-service-dev.lykkex.net/api/Wallets'
    ASSET_PAIR = 'AUDUSD'
    ASSET = 'AUD'

    def get_balance(self):
        log.info("Retrieve current balance.")
        time_stamp = time.asctime()
        q = Request(TradeService.WALLET_URL)
        q.add_header('api-key', TradeService.API_KEY)
        balance = json.loads(urlopen(q).read().decode())
        log.info("Number of assets: {}".format(len(balance)))

        for x in range(0, len(balance)):
            log.info(format('Current wealth ' + balance[x]['AssetId'].encode() + ': ' + str(balance[x]['Balance'])))

        return time_stamp, balance

    def get_pending_orders(self):
        log.info("Get pending orders.")
        time_stamp = time.asctime()
        q = Request('https://hft-service-dev.lykkex.net/api/Orders?status=InOrderBook')
        q.add_header('api-key', TradeService.API_KEY)
        pending_orders = json.loads(urlopen(q).read().decode())
        if not pending_orders:
            log.info("No pending orders")
        return time_stamp, pending_orders

    def send_market_order(self, OrderAction='BUY', Volume='0.1'):
        log.info("Send market order - {}".format(TradeService.ASSET))
        time_stamp = time.asctime()
        url = 'https://hft-service-dev.lykkex.net/api/Orders/market'
        headers = {'api-key': TradeService.API_KEY, 'Content-Type': 'application/json'}
        data = json.dumps(
            {"AssetPairId": TradeService.ASSET_PAIR, "Asset": TradeService.ASSET, "OrderAction": OrderAction,
             "Volume": Volume}).encode("utf8")
        req = Request(url, data, headers)
        f = urlopen(req)
        response = f.read()
        if not json.loads(response)['Error']:
            log.info("Trade succesfull at price {}".format(json.loads(response)['Result']))
        else:
            log.info("Error: Trade not succesfull")
        f.close()
        return time_stamp, json.loads(response)['Error']

    def __init__(self):
        log.info("Initialize trade service.")
