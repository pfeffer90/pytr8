import logging as log

import numpy as np
import time


class PriceService(object):
    def get_price(self):
        log.info("Retrieve price.")
        time_stamp = time.asctime()
        price = np.random.uniform(0, 100)
        log.info("Timestamp: {}".format(time_stamp))
        log.info("Price: {}".format(price))
        return time_stamp, price

    def __init__(self):
        log.info("Initialize price service.")


class DBService(object):
    def make_entry(self, time_stamp, price):
        log.info("Write time {} and price {} to database.".format(time_stamp, price))
        pass

    def get_price_list(self):
        log.info("Retrieve list of prices from database.")
        return np.random.uniform(0, 100, 100)

    def __init__(self):
        log.info("Initialize database service.")


class Trader(object):
    def trade(self, price_list):
        log.info("Trader starts to trade...")
        current_value = self.calculate_value(price_list)

        log.info("Make trading decision.")
        if current_value > self.threshold:
            log.info("Value {} is exceeding threshold {}.".format(current_value, self.threshold))
            log.info("Send buying signal")
            self.buy()
        else:
            log.info("Value {} is below threshold {}.".format(current_value, self.threshold))
            log.info("Do not send buying signal")

    def __init__(self):
        self.threshold = np.random.uniform(0, 1)
        log.info("Initialize trader with threshold {}.".format(self.threshold))

    def buy(self):
        pass

    def calculate_value(self, price_list):
        log.info("Calculate value.")
        value = np.random.uniform(0, 1)
        log.info("Value: {}".format(value))
        return value


def configure_logging():
    logging_format = '%(asctime)s %(levelname)s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    log.basicConfig(format=logging_format, datefmt=date_format, level=log.INFO)


def earn(trader, price_service, db_service):
    time_stamp, price = price_service.get_price()
    db_service.make_entry(time_stamp, price)
    price_list = db_service.get_price_list()
    trader.trade(price_list)


if __name__ == '__main__':
    configure_logging()
    log.info("# PYTR8 #")
    price_service = PriceService()
    db_service = DBService()
    trader = Trader()
    log.info("Start earning...")
    earn(trader, price_service, db_service)
    log.info("Stop earning...")
    log.info("# PYTR8 #")
