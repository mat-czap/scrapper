import json
import os

config_location = os.environ.get("APP_MODE")


def get_config():
    with open(config_location) as config_file:
        config = json.loads(*config_file.readlines())
        return config
