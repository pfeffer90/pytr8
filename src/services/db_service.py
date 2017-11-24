import collections
import logging as log
import os
import sqlite3

import numpy as np


class DBService(object):
    TIME_STAMP_FIELD = 'time_stamp'
    PRICE_FIELD = 'price'
    DEFAULT_PATH_TO_DB = './database/tradebot.db'

    def make_price_entry(self, time_stamp, price_buy, price_sell):
        log.info("Write time {}, buy price {}, and sell price {} to database.".format(time_stamp, price_buy, price_sell))
        self.fake_db_for_price_list.append([price_buy, price_sell])
        pass

    def get_price_list(self):
        log.info("Retrieve list of prices from database.")
        return np.array(self.fake_db_for_price_list)

    def make_trade_entry(self, time_stamp, price, trading_signal, action, is_settled=False):
        price_buy = price[0]
        price_sell = price[1]
        insert_trade_entry = """
        insert into actions (timestamp, price_buy, price_sell, trading_signal, action, is_settled)
        values ('{}' , '{}', '{}', '{}', '{}', '{}')
        """.format(time_stamp, price_buy, price_sell, trading_signal, action, 1 if is_settled else 0)
        print insert_trade_entry
        self.conn.execute(insert_trade_entry)
        self.conn.commit()

    def close_connection_to_db(self):
        self.conn.close()

    def _connect_to_db(self, path_to_database):
        absolute_path_to_db = os.path.abspath(path_to_database)
        db_is_new = not os.path.exists(absolute_path_to_db)

        path_to_database_dir, database_filename = os.path.split(absolute_path_to_db)
        if not os.path.exists(path_to_database_dir):
            os.makedirs(path_to_database_dir)

        conn = sqlite3.connect(absolute_path_to_db)
        if db_is_new:
            log.info('New database, initialize database schemas.')
            self._make_schemas(conn)

        log.info('Using database at {}.'.format(absolute_path_to_db))

        return conn

    def _make_schemas(self, conn):
        create_trade_action_schema = """
        create table actions (
            timestamp date,
            price_buy float,
            price_sell float,
            trading_signal integer,
            action text,
            is_settled bit
        );
        """
        conn.execute(create_trade_action_schema)

    def __init__(self, path_to_database=DEFAULT_PATH_TO_DB):
        log.info("Initialize database service.")
        maximum_price_list_length = 10 ** 6
        self.fake_db_for_price_list = collections.deque(maxlen=maximum_price_list_length)
        self.conn = self._connect_to_db(path_to_database)
