import collections
import logging as log
import os
import sqlite3

import numpy as np


class DBService(object):
    TIME_STAMP_FIELD = 'time_stamp'
    PRICE_FIELD = 'price'
    DB_FILENAME = './database/tradebot.db'

    def make_price_entry(self, time_stamp, price):
        log.info("Write time {} and price {} to database.".format(time_stamp, price))
        self.fake_db_for_price_list.append(price)
        pass

    def get_price_list(self):
        log.info("Retrieve list of prices from database.")
        return np.array(self.fake_db_for_price_list)

    def make_trade_entry(self, time_stamp, price, trading_signal, action):
        insert_trade_entry = """
        insert into actions (timestamp, price, trading_signal, action, is_settled)
        values ('{}' , '{}', '{}', '{}', '0')
        """.format(time_stamp, price, trading_signal, action)
        print insert_trade_entry
        self.conn.execute(insert_trade_entry)
        self.conn.commit()

    def close_connection_to_db(self):
        self.conn.close()

    def _connect_to_db(self):
        absolute_path_to_db = os.path.abspath(DBService.DB_FILENAME)
        db_is_new = not os.path.exists(absolute_path_to_db)
        conn = sqlite3.connect(absolute_path_to_db)
        if db_is_new:
            log.info('No database available. Create {}.'.format(absolute_path_to_db))
            self._make_schemas(conn)
        else:
            log.info('Found database at {}.'.format(absolute_path_to_db))
        return conn

    def _make_schemas(self, conn):
        create_trade_action_schema = """
        create table actions (
            timestamp date,
            price float,
            trading_signal integer,
            action text,
            is_settled bit
        );
        """
        conn.execute(create_trade_action_schema)

    def __init__(self):
        log.info("Initialize database service.")
        maximum_price_list_length = 10 ** 6
        self.fake_db_for_price_list = collections.deque(maxlen=maximum_price_list_length)
        self.conn = self._connect_to_db()
