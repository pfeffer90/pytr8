import logging as log
import time

import lykkex

class TradeService(object):
    WALLET_URL = 'https://hft-service-dev.lykkex.net/api/Wallets'

    @staticmethod
    def get_balance(api_key):
        log.info("Retrieve current balance.")
        time_stamp = time.asctime()
        balance = lykkex.get_balance(api_key)
        log.info("Number of assets: {}".format(len(balance)))

        for x in range(0, len(balance)):
            log.info(format('Current wealth ' + balance[x]['AssetId'].encode() + ': ' + str(balance[x]['Balance'])))

        return time_stamp, balance

    @staticmethod
    def get_pending_orders(api_key):
        log.info("Get pending orders.")
        time_stamp = time.asctime()
        pending_orders = lykkex.get_pending_orders(api_key)
        if not pending_orders:
            log.info("No pending orders")
        return time_stamp, pending_orders

    @staticmethod
    def send_market_order(api_key, asset_pair, asset, order_action='BUY', volume='0.1'):
        log.info("Send market order - {}".format(asset))
        time_stamp = time.asctime()
        response = lykkex.send_market_order(api_key, asset_pair, asset, order_action, volume)
        if not response['Error']:
            log.info("Trade successful at price {}".format(response['Result']))
        else:
            log.info("Error: Trade not successful")
        return time_stamp, response['Error']

    @staticmethod
    def send_limit_order(api_key, asset_pair, asset, price, order_action='BUY', volume='0.1'):
        log.info("Send market order - {}".format(asset))
        time_stamp = time.asctime()
        response = lykkex.send_limit_order(api_key, asset_pair, asset, price, order_action, volume)
        log.info("Limit order placed")
        order_id = str(response)
        return time_stamp, order_id

    @staticmethod
    def control_limit_order(api_key, order_id):
        log.info("Check status of limit order {}", order_id)
        time_stamp = time.asctime()
        content = lykkex.control_limit_order(api_key, order_id)
        status = content['Status']
        return time_stamp, status
        
    def __init__(self):
        log.info("Initialize trade service.")
