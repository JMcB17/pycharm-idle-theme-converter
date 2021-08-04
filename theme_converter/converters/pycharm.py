from bs4 import BeautifulSoup


def add_idle_key_attribute(idle_key: str, pycharm_option: BeautifulSoup, idle_theme: dict):
    idle_theme[f'{idle_key}-foreground'] = pycharm_option.find(name='FOREGROUND')
    idle_theme[f'{idle_key}-background'] = pycharm_option.find(name='BACKGROUND')


def convert(theme: BeautifulSoup, defaults: BeautifulSoup, mapping: dict) -> dict:
    """Convert an IntelliJ IDEA .icls theme to a dict for configparser."""
    idle_theme = {}

    parent_theme_name = theme.scheme.parent_scheme
    parent_theme = defaults.find(parent_theme_name)

    for idle_key, pycharm_key in mapping['attributes'].values():
        if isinstance(pycharm_key, list):
            pass
        else:
            theme_get = theme.find(pycharm_key)
            if theme_get:
                add_idle_key_attribute(idle_key, theme_get, idle_theme)
            else:
                add_idle_key_attribute(idle_key, parent_theme.find(pycharm_key), idle_theme)

    return idle_theme
