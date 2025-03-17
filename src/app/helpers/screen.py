""" Screen helper """

import pyglet.display

from app.constants.settings import SETTINGS_SIZE_MINIUM


def screen_resolutions() -> list:
    """ Get all screen resolutions """

    modes = pyglet.display.get_display().get_default_screen().get_modes()

    modes = filter(lambda mode: is_16_9_ratio(mode.width, mode.height), modes)
    return sorted(list(set(map(lambda mode: (mode.width, mode.height), modes))))


def fullscreen_resolution() -> list:
    """ Get the fullscreen resolution """

    resolutions = list(reversed(screen_resolutions()))

    if not any(resolutions):
        return SETTINGS_SIZE_MINIUM

    return resolutions[0]


def window_resolution() -> list:
    """ Get the window resolution """

    resolutions = screen_resolutions()

    if len(resolutions) < 2:
        resolutions = [SETTINGS_SIZE_MINIUM] + resolutions

    return resolutions[0]


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
