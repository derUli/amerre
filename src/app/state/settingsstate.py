import logging
import os

import arcade
import jsonpickle

from app.constants.settings import SETTINGS_DEFAULT_SHOW_FPS
from app.utils.paths import settings_path

VERSION = 1

class SettingsState:
    """ Game settings """

    def __init__(self):
        """ Constructor """
        self._version = VERSION
        self._show_fps = SETTINGS_DEFAULT_SHOW_FPS

    @staticmethod
    def exists() -> bool:
        """
        Check if there is an existing settings file for the launcher

        @return: bool
        """
        return os.path.exists(settings_path())

    @staticmethod
    def load():
        """
        Loads the settings state

        @return: SettingsState
        """
        try:
            return SettingsState._load()
        except ValueError as e:
            logging.error(e)
        except OSError as e:
            logging.error(e)
        except AttributeError as e:
            logging.error(e)

        return SettingsState()

    @staticmethod
    def _load():
        """
        Actually loads the settings state

        @return: SettingsState
        """
        with open(settings_path(), 'r') as f:
            state = jsonpickle.decode(f.read())

            # jsonpickle don't calls __init__()
            # So when loading a state attributes added since then are missing
            # I added a version number
            # If the state version from the code is newer than the stored version
            # discard the old settings state and return a new one

            if SettingsState().version != state.version:
                return SettingsState()

            return state

    def save(self) -> None:
        """ Save settings as json file """

        directory = os.path.dirname(settings_path())
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(settings_path(), 'w') as f:
            f.write(jsonpickle.encode(self, unpicklable=True))

    @property
    def version(self) -> int:
        return self._version

    @property
    def show_fps(self) -> bool:
        return self._show_fps

    @show_fps.setter
    def show_fps(self, value: bool) -> None:
        self._show_fps = value