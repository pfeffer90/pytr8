import logging as log
import time

import numpy

from services.db_service import DBService
from services.price_service import PriceService
from services.trade_service import TradeService


def momentum_strategy(price_list):
    log.info("Using a momentum strategy.")
    current_price = price_list[-1]
    price_list_mean = price_list.mean()
    log.info("Current price: {}, mean price: {}".format(current_price, price_list_mean))
    #        accuracy = 10**(-4)
    #        trading_signal = TradeBot.BUYING_SIGNAL if (current_price - price_list_mean) > accuracy else 0
    trading_signal = TradeBot.BUYING_SIGNAL if numpy.random.uniform(low=0.0, high=1.0, size=None) > 0.5 else 0
    return trading_signal


class TradeBot(object):
    BUYING_SIGNAL = 1

    def calculate_trading_signal(self, price_list):
        log.info("Calculate trading signal.")
        trading_signal = momentum_strategy(price_list)
        log.info("Trading signal: {}".format(trading_signal))
        return trading_signal

    def act(self):
        log.info("Prepare and execute trading actions...")

        price_list = self.db_service.get_price_list()
        log.debug("Total length of price list: {}".format(len(price_list)))

        trading_signal = self.calculate_trading_signal(price_list)

        if trading_signal == TradeBot.BUYING_SIGNAL:
            self.buy()
        else:
            log.info("Do not send buying signal")

    def buy(self):
        log.info("Send buying signal")
        time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        price = self.db_service.get_price_list()[-1]
        trading_signal = TradeBot.BUYING_SIGNAL
        action = 'BUY'
        self.trade_service.send_market_order(self.api_key, self.asset_pair, self.asset)
        log.info("Persist trading action")
        self.db_service.make_trade_entry(time_stamp, price, trading_signal, action, True)

    def trade(self):
        TRADING_INTERVAL = 1  # seconds
        continue_trading = True
        while continue_trading:
            try:
                log.info("")
                self.inform()
                self.act()
                log.info("Pause for {} seconds".format(TRADING_INTERVAL))
                time.sleep(TRADING_INTERVAL)
            except KeyboardInterrupt:
                log.info("Trading interrupted by user. Quitting")
                continue_trading = False

    def inform(self):
        time_stamp, price, volume = self.price_service.get_price(self.asset_pair)
        self.db_service.make_price_entry(time_stamp, price)
        self.trade_service.get_balance(self.api_key)
        self.trade_service.get_pending_orders(self.api_key)

    def __init__(self, configuration):
        log.info("Initialize trader... ")
        self.api_key = configuration.get_api_key()
        self.asset = configuration.get_asset()
        self.asset_pair = configuration.get_asset_pair()
        self.trading_frequency = configuration.get_trading_frequency()

        self.price_service = PriceService()
        self.trade_service = TradeService()
        self.db_service = DBService(configuration.get_path_to_database())
