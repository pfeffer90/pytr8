from unittest import TestCase

import pandas

from pytr8.tradebot.tradebot import momentum_strategy, TradeBot


class TestMomentumStrategy(TestCase):
    def test_momentum_strategy_raises_an_error_if_price_data_has_less_than_two_data_points(self):
        one_price_data = {"timestamp": ["2000-01-01 00:00:00.000"],
                          "buy_price": [12.2],
                          "sell_price": [12.5]}
        price_data = pandas.DataFrame(data=one_price_data)
        self.assertRaises(RuntimeError, momentum_strategy, price_data)

    def test_momentum_strategy_detects_price_raising(self):
        two_price_data_raising = {"timestamp": ["2000-01-01 00:00:00.000", "2000-01-01 00:00:05.000"],
                          "buy_price": [12.2, 12.3],
                          "sell_price": [12.5, 12.5]}
        price_data = pandas.DataFrame(data=two_price_data_raising)
        actual_trading_signal = momentum_strategy(price_data)

        expected_trading_signal = TradeBot.BUYING_SIGNAL
        self.assertEqual(actual_trading_signal, expected_trading_signal)

    def test_momentum_strategy_detects_price_falling(self):
        two_price_data_falling = {"timestamp": ["2000-01-01 00:00:00.000", "2000-01-01 00:00:05.000"],
                          "buy_price": [12.2, 12.1],
                          "sell_price": [12.5, 12.5]}
        price_data = pandas.DataFrame(data=two_price_data_falling)
        actual_trading_signal = momentum_strategy(price_data)

        expected_trading_signal = TradeBot.SELLING_SIGNAL
        self.assertEqual(actual_trading_signal, expected_trading_signal)
