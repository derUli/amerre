""" Audio utils """

from pyglet import Options


def audio_backends() -> list:
    """ Get supported audio backends """
    return list(Options().audio)