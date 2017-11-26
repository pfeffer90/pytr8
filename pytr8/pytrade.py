import argparse
import json
import logging as log
import os
import sys
from logging import handlers as log_handlers

import lykkex

from services.config_service import ConfigService
from tradebot.tradebot import TradeBot


class PytradeError(Exception):
    def __init__(self, msg):
        self.msg = msg


def get_trading_configuration(config_file_path):
    path_to_config_file = os.path.abspath(config_file_path)
    if not os.path.exists(path_to_config_file):
        raise PytradeError('Could not find the specified configuration file {}.'.format(path_to_config_file))
    return ConfigService(path_to_config_file)


def configure_logging(logging_level_string, logging_dir):
    if logging_level_string == "DEBUG":
        logging_level = log.DEBUG
    elif logging_level_string == "INFO":
        logging_level = log.INFO
    else:
        raise PytradeError("Unknown specified logging level {}.".format(logging_level_string))

    logging_path = os.path.abspath(logging_dir)
    if not os.path.exists(logging_path):
        os.makedirs(logging_path)
    path_to_logging_file = os.path.join(logging_path, 'tradebot.log')

    logging_format = '%(asctime)s %(levelname)s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    log.basicConfig(format=logging_format, datefmt=date_format, level=logging_level)
    log_file_size_in_mb = 2
    fh = log_handlers.RotatingFileHandler(path_to_logging_file,
                                          maxBytes=(log_file_size_in_mb * 1024 * 1024),backupCount=7)
    _logger = log.getLogger()
    _logger.addHandler(fh)


def initialize_parser():
    parser = argparse.ArgumentParser(description='Start the trading bot.')
    parser.add_argument('-f', '--configuration_file_path', required=True)
    parser.add_argument('-l', '--log_level', default="INFO", choices=["DEBUG", "INFO"])
    parser.add_argument('-d', '--log_directory', default="./log")

    return parser


def parse_args(argv):
    parser = initialize_parser()
    parsed_arguments = parser.parse_args(argv)
    return parsed_arguments


def main(argv):
    if argv is None:
        argv = sys.argv[1:]
    parsed_arguments = parse_args(argv)
    configure_logging(parsed_arguments.log_level, parsed_arguments.log_directory)
    try:
        trading_configuration = get_trading_configuration(parsed_arguments.configuration_file_path)
        log.info("# PYTR8 #")
        log.info("")
        log.info("Configuration file: {}".format(trading_configuration.path_to_config_file))
        log.info("Configuration: {}".format(json.dumps(trading_configuration.config, indent=2)))
        log.info("")

        log.info("Check Lykkex API status...")
        api_status = lykkex.is_alive()
        if api_status['IssueIndicators']:
            raise PytradeError('Lykkex API seems not ready. Reported issues:\n {}'.format(api_status))

        log.info('Lykkex API is running')
        trade_bot = TradeBot(trading_configuration)

        log.info("Start trading...")

        trade_bot.trade()

        log.info("Stop trading...")
        log.info("# PYTR8 #")
    except PytradeError, err:
        log.error(err.msg)
        log.error("Shutting down PYTR8")
        return 1


if __name__ == '__main__':
    sys.exit(main(None))
