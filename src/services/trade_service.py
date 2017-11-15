try:
    from urllib.request import Request, urlopen  # Python 3
except:
    from urllib2 import Request, urlopen  # Python 2
import logging as log
import time
import json

class TradeService(object):
    API_KEY = 'b80a447d-ef2c-4d44-978a-8309be7026de'
    WALLET_URL = 'https://hft-service-dev.lykkex.net/api/Wallets'
    ASSET_PAIR = 'AUDUSD'

    def get_balance(self):
        log.info("Retrieve current balance.")
        time_stamp = time.asctime()
        q = Request(WALLET_URL)
        q.add_header('api-key', API_KEY)
        balance = json.loads(urlopen(q).read().decode())
        log.info("Number of assets: {}".format(len(balance)))

        for x in range(0,len(balance)):
            log.info('Current wealth')
            log.info(format(balance[x]['AssetId'].encode() +': ' +str(balance[x]['Balance'])))

        return time_stamp, balance

    def get_pending_orders(self):
        log.info("Get pending orders.")
        time_stamp = time.asctime()
        q = Request('https://hft-service-dev.lykkex.net/api/Orders?status=InOrderBook')
        q.add_header('api-key', API_KEY)
        pending_orders = json.loads(urlopen(q).read().decode())
        if not pending_orders:
            log.info("No pending orders")
        return time_stamp, pending_orders


    def send_market_order(self, Asset='AUD', OrderAction='BUY', Volume='0.01'):
        log.info("Send market order - {}".format(Asset))
        url = 'https://hft-service-dev.lykkex.net/api/Orders/market'
        headers = {'api-key' : API_KEY, 'Content-Type': 'application/json'}
        data = json.dumps({"AssetPairId": ASSET_PAIR, "Asset": Asset, "OrderAction": OrderAction, "Volume": Volume}).encode("utf8")
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