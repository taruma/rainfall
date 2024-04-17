"""This module is used to load the configuration file and make it available to the application."""

from box import Box

_CONFIG_PATH = "app_config.yml"
appConfig = Box.from_yaml(filename=_CONFIG_PATH)
