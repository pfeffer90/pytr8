import os
import sqlite3
from unittest import TestCase

from src.services.db_service import DBService


class TestDBService(TestCase):
    test_db_path = './test.db'

    def setUp(self):
        self.db_service = DBService(TestDBService.test_db_path)

    def tearDown(self):
        os.remove(TestDBService.test_db_path)

    def test_initiation_of_the_database_created_a_database_file_in_the_specified_place(self):
        self.assertTrue(os.path.exists(TestDBService.test_db_path))

    def test_initiation_of_the_database_created_a_trading_action_table(self):
        cursor = self.db_service.conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = {row['name'] for row in cursor.fetchall()}
        self.assertIn('market_orders', table_names)

    def test_initiation_of_the_database_created_a_prices_table(self):
        cursor = self.db_service.conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = {row['name'] for row in cursor.fetchall()}
        self.assertIn('prices', table_names)

    def test_db_service_allows_to_persist_buy_sell_price_pairs(self):
        time_stamp = "2000-01-01 00:00:00.000"
        buy_price = 12.5
        sell_price = 13.0
        self.db_service.make_price_entry(time_stamp, buy_price, sell_price)

        cursor = self.db_service.conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM prices;")
        persisted_prices = cursor.fetchall()

        self.assertEqual(len(persisted_prices), 1)
        persisted_price_pair = persisted_prices[0]

        self.assertEqual(persisted_price_pair["timestamp"], time_stamp)
        self.assertEqual(persisted_price_pair["buy_price"], buy_price)
        self.assertEqual(persisted_price_pair["sell_price"], sell_price)

    def test_db_service_allows_to_fetch_past_buy_sell_price_pairs_data(self):
        buy_price = 12.5
        sell_price = 13.0
        test_entries = [("2000-01-01 00:00:00.000", buy_price, sell_price),
                        ("2000-01-01 00:05:00.000", buy_price, sell_price),
                        ("2000-01-01 00:10:00.000", buy_price, sell_price)]
        for entry in test_entries:
            self.db_service.make_price_entry(*entry)

        actual_price_data = self.db_service.get_price_data()
        self.assertEqual(actual_price_data.shape, (3, 3))

        for returned_buy_price in actual_price_data["buy_price"]:
            self.assertEqual(returned_buy_price, buy_price)

        for returned_sell_price in actual_price_data["sell_price"]:
            self.assertEqual(returned_sell_price, sell_price)

    def test_db_service_allows_to_fetch_price_pairs_after_a_given_date(self):
        time_stamps = ["2000-01-01 00:00:00.000",
                       "2000-01-01 00:05:00.000",
                       "2000-01-01 00:10:00.000"]
        buy_prices = [12.5, 12.6, 12.7]
        sell_prices = [13.0, 12.9, 13.1]

        test_entries = zip(time_stamps, buy_prices, sell_prices)
        for entry in test_entries:
            self.db_service.make_price_entry(*entry)

        actual_price_data = self.db_service.get_price_data(after="2000-01-01 00:00:02.000")
        self.assertEqual(actual_price_data.shape, (2, 3))

        for expected_buy_price, actual_buy_price in zip(buy_prices[1:], actual_price_data["buy_price"]):
            self.assertEqual(expected_buy_price, actual_buy_price)

    def test_db_allows_to_persist_market_orders(self):
        time_stamp = "2000-01-01 00:00:02.000"
        action = "BUY"
        volume = 100
        final_price = 2.2

        self.db_service.make_market_order_entry(time_stamp, action, volume, final_price)

        cursor = self.db_service.conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM market_orders;")
        persisted_market_orders = cursor.fetchall()

        self.assertEqual(len(persisted_market_orders), 1)

        actual_market_order = persisted_market_orders[0]
        expected_market_order = (time_stamp, action, volume, final_price)
        for actual_entry, expected_entry in zip(actual_market_order, expected_market_order):
            self.assertEqual(actual_entry, expected_entry)
