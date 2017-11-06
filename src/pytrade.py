import logging as log

from services.db_service import DBService
from services.price_service import PriceService
from tradebot import TradeBot


def configure_logging():
    logging_format = '%(asctime)s %(levelname)s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    log.basicConfig(format=logging_format, datefmt=date_format, level=log.DEBUG)


if __name__ == '__main__':
    configure_logging()
    log.info("# PYTR8 #")
    price_service = PriceService()
    db_service = DBService()
    trade_bot = TradeBot(price_service, db_service)
    log.info("Start trading...")
    trade_bot.trade()
    log.info("Stop trading...")
    log.info("# PYTR8 #")