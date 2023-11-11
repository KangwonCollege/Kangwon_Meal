import os.path

from configparser import ConfigParser
from utils.directory import directory


def get_config(config_name: str = "token") -> ConfigParser:
    path = os.path.join(directory, "config", config_name + ".ini")
    config = ConfigParser()
    config.read(path)
    
    return config
