import logging as log
import time

from services.db_service import DBService
from services.price_service import PriceService


class Trader(object):
    def trade(self, price_list):
        log.info("Trader starts to trade...")
        current_value = self.calculate_trading_signal(price_list)

        log.info("Make trading decision.")
        if current_value >= self.threshold:
            log.info("Value {} is exceeding threshold {}.".format(current_value, self.threshold))
            log.info("Send buying signal")
            self.buy()
        else:
            log.info("Value {} is below threshold {}.".format(current_value, self.threshold))
            log.info("Do not send buying signal")

    def __init__(self):
        self.threshold = 1
        log.info("Initialize trader with threshold {}.".format(self.threshold))

    def buy(self):
        pass

    def calculate_trading_signal(self, price_list):
        log.info("Calculate trading signal.")
        value = 1 if price_list[-1] > price_list.mean() else 0
        log.info("Value: {}".format(value))
        return value


def configure_logging():
    logging_format = '%(asctime)s %(levelname)s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    log.basicConfig(format=logging_format, datefmt=date_format, level=log.INFO)


def earn(trader, price_service, db_service):
    TRADING_INTERVAL = 5
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
    log.info("Start earning...")
    earn(trader, price_service, db_service)
    log.info("Stop earning...")
    log.info("# PYTR8 #")
