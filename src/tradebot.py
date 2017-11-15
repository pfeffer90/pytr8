import logging as log
import time


class TradeBot(object):
    BUYING_SIGNAL = 1

    def calculate_trading_signal(self, price_list):
        log.info("Calculate trading signal.")
        current_price = price_list[-1]
        price_list_mean = price_list.mean()
        log.info("Current price: {}, mean price: {}".format(current_price, price_list_mean))
        accuracy = 10**(-4)
        trading_signal = TradeBot.BUYING_SIGNAL if (current_price - price_list_mean) > accuracy else 0
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
        self.db_service.make_trade_entry(time_stamp, price, trading_signal, action)
        log.info("Persist trading action")
        self.trade_service.send_market_order()

        pass

    def trade(self):
        TRADING_INTERVAL = 10  # seconds
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
        time_stamp, price, volume = self.price_service.get_price()
        self.db_service.make_price_entry(time_stamp, price)
        self.trade_service.get_balance()
        self.trade_service.get_pending_orders()

    def __init__(self, price_service, db_service, trade_service):
        log.info("Initialize trader... ")
        self.price_service = price_service
        self.db_service = db_service
        self.trade_service = trade_service
