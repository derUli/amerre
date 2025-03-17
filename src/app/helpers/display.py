""" Screen helper """

import pyglet.display
from pyglet.display.base import Screen, ScreenMode

from app.constants.settings import SETTINGS_SIZE_MINIUM


def screen_resolutions() -> list:
    """ Get all screen resolutions """

    m = filter(lambda mode: is_16_9_ratio(mode.width, mode.height), modes())
    m = filter(
        lambda mode: (mode.width, mode.height) >= SETTINGS_SIZE_MINIUM, m)

    if not any(m):
        return [SETTINGS_SIZE_MINIUM]

    return sorted(list(set(map(lambda mode: (mode.width, mode.height), m))))


def fullscreen_resolution() -> tuple:
    """ Get the fullscreen resolution """

    return default_mode().width, default_mode().height


def window_resolution() -> list:
    """ Get the window resolution """

    resolutions = list(filter(
        lambda mode: mode < fullscreen_resolution(), screen_resolutions()
    ))

    if not any(resolutions):
        return SETTINGS_SIZE_MINIUM

    return resolutions[-1]


def gcd(a, b):
    """
    The GCD (greatest common divisor) is the highest number that evenly divides both
    width and height.
    """

    return a if b == 0 else gcd(b, a % b)


def calculate_aspect(width: int, height: int) -> tuple[int, int]:
    """ Calculate aspect ratio of a screen resolution """

    r = gcd(width, height)
    x = int(width / r)
    y = int(height / r)

    return x, y


def is_16_9_ratio(width: int, height: int) -> bool:
    """ Check if a screen resolution is 16:9 """

    return calculate_aspect(width, height) == (16, 9)


def default_screen() -> Screen:
    """ Get default screen """

    return pyglet.display.get_display().get_default_screen()


def default_mode() -> ScreenMode:
    """ Get default mode """

    return default_screen().get_mode()


def modes() -> list:
    """ Get all screen modes """

    return default_screen().get_modes()


def default_rate() -> int:
    """ Get default refresh rate """

    return default_mode().rate
