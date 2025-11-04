from system_tests.config import config
from enum import Enum


class DashboardUrl(Enum):
    PEOPLE = "/people"
    PLANETS = "/planets"


def url(base_path, path, **path_params):
    return base_path + path.format(**path_params)


def url(path, **path_params):
    return url(config.settings.api_host, path, **path_params)


def url(path):
    return config.settings.api_host + path


def url(path: Enum):
    return config.settings.api_host + path.value
