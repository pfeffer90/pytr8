import collections
import logging as log
import numpy as np

class DBService(object):
    TIME_STAMP_FIELD = 'time_stamp'
    PRICE_FIELD = 'price'

    def make_entry(self, time_stamp, price):
        log.info("Write time {} and price {} to database.".format(time_stamp, price))
        self.fake_db.append(price)
        pass

    def get_price_list(self):
        log.info("Retrieve list of prices from database.")
        return np.array(self.fake_db)

    def __init__(self):
        limit_of_price = 10 ** 6
        self.fake_db = collections.deque(maxlen=limit_of_price)

        log.info("Initialize database service.")
