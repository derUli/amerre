""" Localization utils """
import locale

from app.constants.gameinfo import LOCALE_FALLBACK, \
    LOCALES_AVAILABLE


def default_language() -> str:
    """ Detect the default langauge """

    ls = list(locale.getlocale())
    ls = map(lambda s: s[:2].lower(), ls)
    ls = list(filter(lambda s: s in LOCALES_AVAILABLE, ls))

    if not any(ls):
        return LOCALE_FALLBACK

    return ls[0]
