try:
    from urllib.request import Request, urlopen  # Python 3
except:
    from urllib2 import Request, urlopen  # Python 2
import json
import logging as log
import time


class TradeService(object):
    WALLET_URL = 'https://hft-service-dev.lykkex.net/api/Wallets'

    @staticmethod
    def get_balance(api_key):
        log.info("Retrieve current balance.")
        time_stamp = time.asctime()
        q = Request(TradeService.WALLET_URL)
        q.add_header('api-key', api_key)
        balance = json.loads(urlopen(q).read().decode())
        log.info("Number of assets: {}".format(len(balance)))

        for x in range(0, len(balance)):
            log.info(format('Current wealth ' + balance[x]['AssetId'].encode() + ': ' + str(balance[x]['Balance'])))

        return time_stamp, balance

    @staticmethod
    def get_pending_orders(api_key):
        log.info("Get pending orders.")
        time_stamp = time.asctime()
        q = Request('https://hft-service-dev.lykkex.net/api/Orders?status=InOrderBook')
        q.add_header('api-key', api_key)
        pending_orders = json.loads(urlopen(q).read().decode())
        if not pending_orders:
            log.info("No pending orders")
        return time_stamp, pending_orders

    @staticmethod
    def send_market_order(api_key, asset_pair, asset, order_action='BUY', volume='0.1'):
        log.info("Send market order - {}".format(asset))
        time_stamp = time.asctime()
        url = 'https://hft-service-dev.lykkex.net/api/Orders/market'
        headers = {'api-key': api_key, 'Content-Type': 'application/json'}
        data = json.dumps(
            {"AssetPairId": asset_pair, "Asset": asset, "OrderAction": order_action,
             "Volume": volume}).encode("utf8")
        req = Request(url, data, headers)
        f = urlopen(req)
        response = f.read()
        if not json.loads(response)['Error']:
            log.info("Trade successful at price {}".format(json.loads(response)['Result']))
        else:
            log.info("Error: Trade not successful")
        f.close()
        return time_stamp, json.loads(response)['Error']

    def __init__(self):
        log.info("Initialize trade service.")
