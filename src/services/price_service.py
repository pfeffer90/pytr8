import logging as log
import time

import requests


class PriceService(object):
    ASSET_PAIR = 'AUDUSD'
    REQUEST_ORDER_BOOKS_ADDR = "https://hft-service-dev.lykkex.net/api/OrderBooks/"

    def get_price(self):
        log.info("Retrieve current price.")
        time_stamp = time.asctime()

        order_books = requests.get(PriceService.REQUEST_ORDER_BOOKS_ADDR + PriceService.ASSET_PAIR).json()
        price = self.get_asset_price(order_books)
        volume = self.get_asset_trading_volume(order_books)
        log.info("Timestamp: {}".format(time_stamp))
        log.info("Price: {}".format(price))
        return time_stamp, price, volume

    def get_asset_trading_volume(self, order_books):
        return order_books[1]['Prices'][-1]['Volume']

    def get_asset_price(self, order_books):
        price = order_books[1]['Prices'][-1]['Price']
        return price

    def __init__(self):
        log.info("Initialize price service.")