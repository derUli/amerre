""" Audio utils """

from pyglet import Options


def audio_drivers() -> list:
    """ Get supported audio backends """

    return list(Options().audio)
