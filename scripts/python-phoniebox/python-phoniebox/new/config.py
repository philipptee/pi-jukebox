import configparser
from collections import namedtuple

class ConfigError(Exception):
    def __init__(self, message):
        self.message = message

Config = namedtuple('Config', 'min_volume_percent max_volume_percent')

def Loadconfig(path):
    parser = configparser.ConfigParser()
    config = parser.read(path)
    if "DEFAULT" not in config.keys():
        raise ConfigError(
            "Missing [DEFAULT] header section in config file: %s" % path)
    default = config["DEFAULT"]
    return Config(
        default.get(MIN_VOLUME_PERCENT, 0),
        default.get(MAX_VOLUME_PERCENT, 100)
    )