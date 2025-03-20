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


def bool_to_on_off(value: bool) -> str:
    """ boolean to translated string """
    
    if value:
        return _('On')

    return _('Off')
