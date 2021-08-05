from typing import Union, List
from bs4 import BeautifulSoup, Tag


def _find_key_with_fallbacks(themes: Union[Tag, List[Tag]], keys: Union[str, List[str]]) -> Tag:
    """Find the first result from a number of themes and a number of keys, searching keys first then themes."""
    if not isinstance(themes, list):
        themes = [themes]
    if not isinstance(keys, list):
        keys = [keys]

    # todo: handle failure here
    for theme in themes:
        for key in keys:
            tag_search = theme.find(key)
            if tag_search:
                return tag_search


def convert(theme: BeautifulSoup, defaults: BeautifulSoup, mapping: dict) -> dict:
    """Convert an IntelliJ IDEA .icls theme to a dict for configparser."""
    idle_theme = {}

    # todo: handle failure here
    parent_theme_name = theme.scheme['parent_scheme']
    parent_theme = defaults.find('scheme', attrs={'name': parent_theme_name})

    for idle_key, pycharm_key in mapping['colors'].values():
        pycharm_color_tag = _find_key_with_fallbacks([theme, parent_theme], pycharm_key)
        idle_theme[idle_key] = pycharm_color_tag.value

    for idle_key_partial, pycharm_key in mapping['attributes'].values():
        pycharm_attribute_tag = _find_key_with_fallbacks([theme, parent_theme], pycharm_key)
        idle_theme[f'{idle_key_partial}-foreground'] = pycharm_attribute_tag.find(name='FOREGROUND')
        idle_theme[f'{idle_key_partial}-background'] = pycharm_attribute_tag.find(name='BACKGROUND')

    return idle_theme
