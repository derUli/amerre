""" Dev utils """
import logging
import sys
import pyglet

from app.helpers.string import label_value
from app.state.settingsstate import SettingsState


def configure_pyglet():
    """ Pyglet must be configured before arcade is imported """

    state = SettingsState.load()
    logging.info(label_value('Debug', state.debug))
    pyglet.options.debug_gl = state.debug
    print(pyglet.options.audio)

def is_frozen() -> bool:
    """ Check is the app is frozen """

    return hasattr(sys, 'frozen')
