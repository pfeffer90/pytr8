import argparse
import json
import logging as log
import os
import sys
import requests

from services.config_service import ConfigService
from tradebot import TradeBot


def configure_logging():
    logging_format = '%(asctime)s %(levelname)s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    log.basicConfig(format=logging_format, datefmt=date_format, level=log.DEBUG)


def initialize_parser():
    parser = argparse.ArgumentParser(description='Start the trading bot.')
    parser.add_argument('-f', '--configuration_file_path', required=True)

    return parser


def get_trading_configuration(args):
    parser = initialize_parser()
    parsed_arguments = parser.parse_args(args)
    path_to_config_file = os.path.abspath(parsed_arguments.configuration_file_path)
    if not os.path.exists(path_to_config_file):
        raise RuntimeError('Could not find the specified configuration file {}.'.format(path_to_config_file))
    return ConfigService(path_to_config_file)


if __name__ == '__main__':
    trading_configuration = get_trading_configuration(sys.argv[1:])
    configure_logging()
    log.info("# PYTR8 #")
    log.info("")
    log.info("Configuration file: {}".format(trading_configuration.path_to_config_file))
    log.info("Configuration: {}".format(json.dumps(trading_configuration.config, indent=2)))
    log.info("")

    log.info("Check status...")
    api_running = requests.get("https://hft-service-dev.lykkex.net/api/IsAlive").json()
    if api_running['IssueIndicators']:
        log.error('API is not ready - interrupt trading')
    if not api_running['IssueIndicators']:
        log.error('API is running')
        trade_bot = TradeBot(trading_configuration)
        
        log.info("Start trading...")
        
        trade_bot.trade()
        
        log.info("Stop trading...")
        log.info("# PYTR8 #")
