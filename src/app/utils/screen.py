import pyglet.display

from app.constants.settings import SETTINGS_SIZE_MINIUM


def screen_resolutions() -> list:
    modes = pyglet.display.get_display().get_default_screen().get_modes()

    modes = filter(lambda mode: is_16_9_ratio(mode), modes)
    return sorted(list(set(map(lambda mode: (mode.width, mode.height), modes))))


def fullscreen_resolution() -> list:
    resolutions = list(reversed(screen_resolutions()))

    if not any(resolutions):
        return SETTINGS_SIZE_MINIUM

    return resolutions[0]


def window_resolution() -> list:
    resolutions = list(reversed(screen_resolutions()))

    if len(resolutions) < 2:
        return SETTINGS_SIZE_MINIUM

    return resolutions[1]


def is_16_9_ratio(mode) -> bool:
    return calculate_aspect(mode.width, mode.height) == "16:9"


def calculate_aspect(width: int, height: int) -> str:
    def gcd(a, b):
        """The GCD (greatest common divisor) is the highest number that evenly divides both width and height."""
        return a if b == 0 else gcd(b, a % b)

    r = gcd(width, height)
    x = int(width / r)
    y = int(height / r)

    return f"{x}:{y}"
