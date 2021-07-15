from os import path
from pathlib import Path
import json


def get_json_config() -> dict:
    with open(file=path.join(Path(__file__).parent, '../.config.json'), mode='r') as config:
        local_config = json.load(config)['config']
    return local_config


class Config:
    def __init__(self):
        self.db = _DBConfig()
        self.default = _DefaultVars()


class _DBConfig:
    def __init__(self):
        self.__dict__ = get_json_config()['db']
        

class _DefaultVars:
    def __init__(self):
        self.__dict__ = get_json_config()['default_values']

