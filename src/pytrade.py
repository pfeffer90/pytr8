import logging as log
import time

from services.db_service import DBService
from services.price_service import PriceService


class Trader(object):
    BUYING_SIGNAL = 1

    def calculate_trading_signal(self, price_list):
        log.info("Calculate trading signal.")
        current_price = price_list[-1]
        price_list_mean = price_list.mean()
        log.info("Current price: {}, mean price: {}".format(current_price, price_list_mean))
        trading_signal = Trader.BUYING_SIGNAL if current_price > price_list_mean else 0
        log.info("Trading signal: {}".format(trading_signal))
        return trading_signal

    def buy(self):
        pass

    def trade(self, price_list):
        log.info("Trader starts to trade...")
        trading_signal = self.calculate_trading_signal(price_list)

        log.info("Make trading decision.")
        if trading_signal == Trader.BUYING_SIGNAL:
            log.info("Send buying signal")
            self.buy()
        else:
            log.info("Do not send buying signal")

    def __init__(self):
        log.info("Initialize trader... ")


def configure_logging():
    logging_format = '%(asctime)s %(levelname)s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    log.basicConfig(format=logging_format, datefmt=date_format, level=log.INFO)


def earn(trader, price_service, db_service):
    TRADING_INTERVAL = 5 #seconds
    continue_trading = True
    while continue_trading:
        try:
            log.info("")
            time_stamp, price, volume = price_service.get_price()
            db_service.make_entry(time_stamp, price)
            price_list = db_service.get_price_list()
            trader.trade(price_list)
            log.info("Pause for {} seconds".format(TRADING_INTERVAL))
            time.sleep(TRADING_INTERVAL)
        except KeyboardInterrupt:
            log.info("Trading interrupted by user. Quitting")
            continue_trading = False


if __name__ == '__main__':
    configure_logging()
    log.info("# PYTR8 #")
    price_service = PriceService()
    db_service = DBService()
    trader = Trader()
    log.info("Start trading...")
    earn(trader, price_service, db_service)
    log.info("Stop trading...")
    log.info("# PYTR8 #")
