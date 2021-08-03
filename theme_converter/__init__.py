import configparser
from pathlib import Path

import requests
from bs4 import BeautifulSoup


DEFAULTCOLORSCHEMESMANAGER_XML_URL = 'https://raw.githubusercontent.com/JetBrains/intellij-community/master' \
                                     '/platform/platform-resources/src/DefaultColorSchemesManager.xml'


def download_defaults(defaults_url: str = DEFAULTCOLORSCHEMESMANAGER_XML_URL) -> BeautifulSoup:
    """Get the default colour schemes xml from the IntelliJ Community GitHub repo and put it in a soup."""
    response = requests.get(defaults_url)
    soup = BeautifulSoup(response.raw)
    return soup


def save_idle_theme(theme_name: str, theme: dict, config_highlight_path: Path):
    """Save the IDLE theme to the config-highlight.cfg file with name theme_name."""
    config_highlight = configparser.ConfigParser()
    config_highlight.read(config_highlight_path, encoding='utf-8')

    # todo: pay attention to overwrites
    config_highlight[theme_name] = theme
    with open(config_highlight_path, 'w', encoding='utf-8') as config_highlight_file:
        config_highlight.write(config_highlight_file, space_around_delimiters=False)


def main():
    pass
