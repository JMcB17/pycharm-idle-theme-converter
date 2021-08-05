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
            tag_search = theme.find('option', attrs={'name': key})
            if tag_search:
                return tag_search


def convert(theme: BeautifulSoup, defaults: BeautifulSoup, mapping: dict) -> dict:
    """Convert an IntelliJ IDEA .icls theme to a dict for configparser."""
    idle_theme = {}

    # todo: handle failure here
    parent_theme_name = theme.scheme['parent_scheme']
    parent_theme = defaults.find('scheme', attrs={'name': parent_theme_name})

    for idle_key, pycharm_key in mapping['colors'].items():
        pycharm_color_tag = _find_key_with_fallbacks([theme, parent_theme], pycharm_key)
        idle_theme[idle_key] = pycharm_color_tag['value']

    for idle_key_partial, pycharm_key in mapping['attributes'].items():
        pycharm_attribute_tag = _find_key_with_fallbacks([theme, parent_theme], pycharm_key)

        # todo: need fallback on these too
        # todo: remove debug fallback
        foreground_option = pycharm_attribute_tag.find('option', attrs={'name': 'FOREGROUND'}) or {'value': ''}
        foreground_color = foreground_option['value']
        idle_theme[f'{idle_key_partial}-foreground'] = foreground_color

        background_option = pycharm_attribute_tag.find('option', attrs={'name': 'BACKGROUND'}) or {'value': ''}
        background_color = background_option['value']
        idle_theme[f'{idle_key_partial}-background'] = background_color

    # todo: add hashes to color codes, idle themes have them but not pycharm themes

    return idle_theme
