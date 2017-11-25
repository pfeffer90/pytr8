import json


class ConfigService(object):
    API_KEY = 'API_KEY'
    ASSET = 'ASSET'
    ASSET_PAIR = 'ASSET_PAIR'
    TRADING_FREQUENCY = 'TRADING_FREQUENCY'
    PATH_TO_DATABASE = 'PATH_TO_DATABASE'

    def get_api_key(self):
        return self.config[ConfigService.API_KEY]

    def get_asset(self):
        return self.config[ConfigService.ASSET]

    def get_asset_pair(self):
        return self.config[ConfigService.ASSET_PAIR]

    def get_trading_frequency(self):
        return self.config[ConfigService.TRADING_FREQUENCY]

    def get_path_to_database(self):
        return self.config[ConfigService.PATH_TO_DATABASE]

    def __init__(self, path_to_config_file):
        self.path_to_config_file = path_to_config_file
        with open(self.path_to_config_file) as config_file:
            self.config = json.load(config_file)
