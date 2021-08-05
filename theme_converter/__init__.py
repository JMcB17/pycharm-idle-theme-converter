import argparse
import configparser
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import theme_converter.converters.pycharm


DEFAULTCOLORSCHEMESMANAGER_XML_URL = 'https://raw.githubusercontent.com/JetBrains/intellij-community/master' \
                                     '/platform/platform-resources/src/DefaultColorSchemesManager.xml'
MAPPINGS_DIRECTORY = Path('mappings/')
IDLERC_DIRECTORY = Path.home() / '.idlerc'
CONFIG_MAIN_CFG = IDLERC_DIRECTORY / 'config-highlight.cfg'


def get_parser() -> argparse.ArgumentParser:
    """Get the parser for the main function."""
    parser = argparse.ArgumentParser()

    parser.add_argument('icls_file', type=Path)

    return parser


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
        config_highlight.write(config_highlight_file)


def main():
    parser = get_parser()
    args = parser.parse_args()

    icls_file = args.icls_file
    icls_contents = icls_file.read_text()
    icls_soup = BeautifulSoup(icls_contents)
    mapping_path = MAPPINGS_DIRECTORY / 'pycharm.json'
    with open(mapping_path, encoding='utf-8') as mapping_file:
        pycharm_mapping = json.load(mapping_file)
    pycharm_default_themes = download_defaults()

    new_theme = theme_converter.converters.pycharm.convert(icls_soup, pycharm_default_themes, pycharm_mapping)
    save_idle_theme('test', new_theme, CONFIG_MAIN_CFG)
