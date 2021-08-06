from typing import Union, List

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag  # type hints


# todo: fix mapping for error, the pycharm key it's mapped to doesn't have fg or bg but does have effect


DEFAULTCOLORSCHEMESMANAGER_XML_URL = 'https://raw.githubusercontent.com/JetBrains/intellij-community/master' \
                                     '/platform/platform-resources/src/DefaultColorSchemesManager.xml'
ATTR_MAPPING = {'-foreground': 'FOREGROUND', '-background': 'BACKGROUND'}


def _download_defaults(defaults_url: str = DEFAULTCOLORSCHEMESMANAGER_XML_URL) -> BeautifulSoup:
    """Get the default colour schemes xml from the IntelliJ Community GitHub repo and put it in a soup."""
    response = requests.get(defaults_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def _find_key_with_fallbacks(themes: Union[Tag, List[Tag]], keys: Union[str, List[str]]) -> List[Tag]:
    """Find the first result from a number of themes and a number of keys, searching keys first then themes."""
    if not isinstance(themes, list):
        themes = [themes]
    if not isinstance(keys, list):
        keys = [keys]
    # always fall back to Default Text
    keys.append('TEXT')

    hits = []
    for theme in themes:
        for key in keys:
            tag_search = theme.find('option', attrs={'name': key})
            if tag_search is not None:
                hits.append(tag_search)

    return hits


def convert(theme: BeautifulSoup, mapping: dict) -> dict:
    """Convert an IntelliJ IDEA .icls theme to a dict for configparser."""
    idle_theme = {}

    # todo: make this cached
    defaults = _download_defaults()

    theme_name = theme.scheme['name']
    # todo: handle failure here
    parent_theme_name = theme.scheme['parent_scheme']
    parent_theme = defaults.find('scheme', attrs={'name': parent_theme_name})

    for idle_key, pycharm_key in mapping['colors'].items():
        pycharm_color_tags = _find_key_with_fallbacks([theme, parent_theme], pycharm_key)
        # this is needed exclusively because SELECTION_FOREGROUND has a value field but it's empty
        # pycharm's theme system is not very cool
        for color_tag in pycharm_color_tags:
            try:
                if color_tag['value']:
                    idle_theme[idle_key] = color_tag['value']
                    break
            except KeyError:
                for idle_suffix, pycharm_attr in ATTR_MAPPING.items():
                    if idle_key.endswith(idle_suffix):
                        idle_theme[idle_key] = color_tag.find('option', attrs={'name': pycharm_attr})['value']

    for idle_key_partial, pycharm_key in mapping['attributes'].items():
        pycharm_attribute_tags = _find_key_with_fallbacks([theme, parent_theme], pycharm_key)

        for idle_suffix, pycharm_attr in ATTR_MAPPING.items():
            for attribute_tag in pycharm_attribute_tags:
                tag_search = attribute_tag.find('option', attrs={'name': pycharm_attr})
                if tag_search is not None:
                    idle_theme[idle_key_partial + idle_suffix] = tag_search['value']
                    break

    # convert colour codes from pycharm format to idle format
    for key, value in idle_theme.items():
        idle_theme[key] = '#' + value.upper()

    return {theme_name: idle_theme}
