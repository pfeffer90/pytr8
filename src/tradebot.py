import logging as log
import time


class TradeBot(object):
    BUYING_SIGNAL = 1

    def calculate_trading_signal(self, price_list):
        log.info("Calculate trading signal.")
        current_price = price_list[-1]
        price_list_mean = price_list.mean()
        log.info("Current price: {}, mean price: {}".format(current_price, price_list_mean))
        trading_signal = TradeBot.BUYING_SIGNAL if current_price > price_list_mean else 0
        log.info("Trading signal: {}".format(trading_signal))
        return trading_signal

    def buy(self):
        pass

    def act(self, price_list):
        log.info("Tradebot makes trading decision...")
        trading_signal = self.calculate_trading_signal(price_list)

        if trading_signal == TradeBot.BUYING_SIGNAL:
            log.info("Send buying signal")
            self.buy()
        else:
            log.info("Do not send buying signal")

    def trade(self):
        TRADING_INTERVAL = 0.01  # seconds
        continue_trading = True
        while continue_trading:
            try:
                log.info("")
                time_stamp, price, volume = self.price_service.get_price()
                self.db_service.make_price_entry(time_stamp, price)
                price_list = self.db_service.get_price_list()
                n = len(price_list)
                log.info("Total length of price list: {}".format(n))
                self.act(price_list)
                log.info("Pause for {} seconds".format(TRADING_INTERVAL))
                time.sleep(TRADING_INTERVAL)
            except KeyboardInterrupt:
                log.info("Trading interrupted by user. Quitting")
                continue_trading = False

    def __init__(self, price_service, db_service):
        log.info("Initialize trader... ")
        self.price_service = price_service
        self.db_service = db_service
