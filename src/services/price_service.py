import logging as log
import time
import datetime
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
        time_ob = self.get_time(order_books)
        time_delta = (datetime.datetime.strptime(time_stamp, '%a %b %d %H:%M:%S %Y')-time_ob).total_seconds()

        log.info("Timestamp: {}".format(time_stamp))
        log.info("Price: {}".format(price))
        log.info("System latency: {} secs".format(time_delta))
        return time_stamp, price, volume

    def get_asset_trading_volume(self, order_books):
        return order_books[1]['Prices'][-1]['Volume']

    def get_time(self,order_books):
        time_stamp_ob = order_books[1]['Timestamp']
        val = datetime.datetime.strptime(time_stamp_ob, '%Y-%m-%dT%H:%M:%S.%f')  
        return val       
        
    def get_asset_price(self, order_books):
        try:
            price = order_books[1]['Prices'][-1]['Price']
        except IndexError as e:
            log.error("Could not extract price from order books.")
            log.error("{}".format(order_books))
            raise RuntimeError(e.message)
        return price

    def __init__(self):
        log.info("Initialize price service.")