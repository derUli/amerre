""" Audio utils """
import pyglet.media
from pyglet import Options, media


def audio_backends() -> list:
    """ Get supported audio backends """
    return list(Options().audio)