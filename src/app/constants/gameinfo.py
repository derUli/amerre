""" Version number """

VERSION = (0, 0, 1)
VERSION_STRING = '.'.join(map(str, VERSION))

DIRECTORY_GAME_NAME_WIN = 'Amerre'
DIRECTORY_GAME_NAME_LINUX = '.amerre'

MAPS = [
    'map01',
    # 'map02'
]

LOCALE_FALLBACK = 'en'
LOCALE_GERMAN = 'de'
LOCALE_ENGLISH = 'en'
LOCALES_AVAILABLE = [
    LOCALE_GERMAN,
    LOCALE_ENGLISH
]


def locales_translated() -> dict:
    """ All locales """

    return {
        LOCALE_GERMAN: _('German'),
        LOCALE_ENGLISH: _('English')
    }


BASE_WIDTH = 2560
BASE_HEIGHT = 1440
