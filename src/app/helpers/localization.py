import locale

from app.constants.gameinfo import locales_all, LOCALE_FALLBACK


def default_language():
    """ Detect default langauge """

    ls = list(locale.getlocale())
    ls = map(lambda s: s[:2].lower(), ls)
    ls = list(filter(lambda s: s in locales_all().keys(), ls))

    if not any(ls):
        return LOCALE_FALLBACK

    return ls[0]