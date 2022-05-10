from box import Box

_CONFIG_PATH = "app_config.yml"
appConfig = Box.from_yaml(filename=_CONFIG_PATH)
appConfig.DASH_THEME.THEME = "COSMO"
