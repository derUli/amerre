import locale

from app.constants.gameinfo import LOCALES_ALL, LOCALE_FALLBACK


def default_language():
    """ Detect default langauge """

    ls = list(locale.getlocale())
    ls = map(lambda s: s[:2].lower(), ls)
    ls = list(filter(lambda s: s in LOCALES_ALL, ls))

    if not any(ls):
        return LOCALE_FALLBACK

    return ls[0]