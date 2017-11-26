import logging as log
import os
import sqlite3

import pandas


class DBService(object):
    DEFAULT_PATH_TO_DB = './database/tradebot.db'

    def make_price_entry(self, time_stamp, buy_price, sell_price):
        log.info(
            "Write time {}, buy price {}, and sell price {} to database.".format(time_stamp, buy_price, sell_price))
        insert_price_pair = "insert into prices values (?, ?, ?)"
        self.conn.execute(insert_price_pair, (time_stamp, buy_price, sell_price))
        self.conn.commit()

    def get_price_data(self):
        log.info("Retrieve price data from database.")
        price_df = pandas.read_sql_query("select * from prices;", self.conn)
        return price_df

    def make_trade_entry(self, time_stamp, price, trading_signal, action, is_settled=False):
        price_buy = price[0]
        price_sell = price[1]
        insert_trade_entry = """
        insert into trading_actions (timestamp, price_buy, price_sell, trading_signal, action, is_settled)
        values ('{}' , '{}', '{}', '{}', '{}', '{}')
        """.format(time_stamp, price_buy, price_sell, trading_signal, action, 1 if is_settled else 0)
        self.conn.execute(insert_trade_entry)
        self.conn.commit()

    def get_trade_entries(self):
        get_trade_entries = 'select * from actions'
        c = self.conn.cursor()
        c.execute(get_trade_entries)
        rows = c.fetchall()
        return list(rows)

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
        create_prices_schema = """
        create table prices (
            timestamp date,
            buy_price float,
            sell_price float
        );
        """

        conn.execute(create_prices_schema)

        create_trade_action_schema = """
        create table trading_actions (
            timestamp date,
            price_buy float,
            price_sell float,
            trading_signal integer,
            action text,
            is_settled bit
        );
        """
        conn.execute(create_trade_action_schema)

        conn.commit()

    def __init__(self, path_to_database=DEFAULT_PATH_TO_DB):
        log.info("Initialize database service.")
        self.conn = self._connect_to_db(path_to_database)
