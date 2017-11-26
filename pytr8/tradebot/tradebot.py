import logging as log
import time

import numpy

from pytr8.services.db_service import DBService
from pytr8.services.lykkex_service import LykkexService

def momentum_strategy(price_list):
    log.info("Using a momentum strategy.")
    midquotes = price_list[['buy_price','sell_price']].mean(axis=1)
    momentum = numpy.nanmean(numpy.log(midquotes) - numpy.log(midquotes.shift(1)))

    
    accuracy = 10 ** (-4)
    if numpy.abs(momentum) < accuracy:
        momentum = 0
        
    log.info("Momentum: {}".format(momentum))
    trading_signal = numpy.sign(momentum)
    return trading_signal


def random_strategy(_):
    log.info("Using a random strategy.")
    trading_signal = numpy.random.randint(3, size=None) - 1

    return trading_signal

def no_strategy(_):
    log.info("No strategy. Just wait and see")
    trading_signal = 0

    return trading_signal

class TradeBot(object):
    BUYING_SIGNAL = 1
    SELLING_SIGNAL = -BUYING_SIGNAL

    def calculate_trading_signal(self,):
        log.info("Calculate trading signal.")
        price_data = self.db_service.get_price_data()
        trading_signal = momentum_strategy(price_data)
        log.info("Trading signal: {}".format(trading_signal))
        return trading_signal

    def act(self):
        log.info("Prepare and execute trading actions...")

        trading_signal = self.calculate_trading_signal()

        if trading_signal == TradeBot.BUYING_SIGNAL:
            self.buy()
        if trading_signal == TradeBot.SELLING_SIGNAL:
            self.sell()
        else:
            log.info("Do not send market orders")

    def buy(self):
        log.info("Send buying signal")

        action = "BUY"
        volume = 0.1

        timestamp, final_price = self.lykkex_service.send_market_order(self.api_key,
                                                                       self.asset_pair,
                                                                       self.asset,
                                                                       action,
                                                                       volume)
        log.info("Persist trading action")
        self.db_service.make_market_order_entry(timestamp, action, volume, final_price)

    def sell(self):
        log.info("Send selling signal")
        action = "SELL"
        volume = 0.1

        timestamp, final_price = self.lykkex_service.send_market_order(self.api_key,
                                                                       self.asset_pair,
                                                                       self.asset,
                                                                       action,
                                                                       volume)
        log.info("Persist trading action")
        self.db_service.make_market_order_entry(timestamp, action, volume, final_price)

    def trade(self):
        trading_interval = 1. / self.trading_frequency  # seconds
        continue_trading = True
        while continue_trading:
            try:
                log.info("")
                self.inform()

                stop_trading = self.evaluate()
                if not stop_trading:
                    self.act()
                log.info("Pause for {} seconds".format(trading_interval))
                time.sleep(trading_interval)
            except KeyboardInterrupt:
                log.info("Trading interrupted by user. Quitting")
                continue_trading = False

    def inform(self):
        log.info('Start inform')
        time_stamp, price_buy, volume_buy = self.lykkex_service.get_price(self.asset_pair, 'BUY')
        log.info('Start inform')
        time_stamp, price_sell, volume_sell = self.lykkex_service.get_price(self.asset_pair, 'SELL')

        self.db_service.make_price_entry(time_stamp, price_buy, price_sell)

    def evaluate(self):
        log.info("Start risk management")

        # Check if funds are sufficient
        balance = self.lykkex_service.get_balance(self.api_key)[1]
        all_available = 1
        for x in range(0, len(balance)):
            if balance[x]['Balance'] < 0.01:
                all_available = 0

        # Check if orders are pending
        no_pending_orders = not self.lykkex_service.get_pending_orders(self.api_key)[1]
        if all_available and no_pending_orders:
            stop_trading = 0
        else:
            stop_trading = 1

        log.info("Trading stop: {}".format(stop_trading))
        return stop_trading

    def __init__(self, configuration):
        log.info("Initialize trader... ")
        self.api_key = configuration.get_api_key()
        self.asset = configuration.get_asset()
        self.asset_pair = configuration.get_asset_pair()
        self.trading_frequency = configuration.get_trading_frequency()

        self.lykkex_service = LykkexService()
        self.db_service = DBService(configuration.get_path_to_database())
