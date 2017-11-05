import logging as log

import numpy as np


class DBService(object):
    def make_entry(self, time_stamp, price):
        log.info("Write time {} and price {} to database.".format(time_stamp, price))
        pass

    def get_price_list(self):
        log.info("Retrieve list of prices from database.")
        return np.random.uniform(0, 100, 100)

    def __init__(self):
        log.info("Initialize database service.")