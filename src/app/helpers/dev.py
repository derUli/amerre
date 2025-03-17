""" Dev utils """

import sys
import pyglet

from app.state.settingsstate import SettingsState


def configure_pyglet():
    """ Pyglet must be configured before arcade is imported """

    state = SettingsState.load()
    pyglet.options.debug_gl = state.debug

def is_frozen() -> bool:
    """ Check is the app is frozen """

    return hasattr(sys, 'frozen')
