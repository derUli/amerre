""" Savegame state """
import logging
import os

import jsonpickle

from app.constants.gameinfo import MAPS, DEFAULT_ENCODING
from app.helpers.paths import savegame_path

VERSION = 1


class SavegameState:
    def __init__(self):
        self._version = VERSION
        self._current_level = 0

    @staticmethod
    def exists() -> bool:
        """ Check if there is an existing savegame """

        return os.path.exists(savegame_path())

    @property
    def lastmodified(self) -> float:
        """ Last modification time """

        return os.path.getmtime(savegame_path())

    @property
    def current_level(self):
        try:
            return MAPS[self._current_level]
        except IndexError:
            return None

    def next_level(self):
        if not self.current_level:
            return False

        self._current_level += 1

    @staticmethod
    def load():
        """ Loads the settings state """

        try:
            return SavegameState._load()
        except ValueError as e:
            logging.error(e)
        except OSError as e:
            logging.error(e)
        except AttributeError as e:
            logging.error(e)

        return SavegameState()

    @staticmethod
    def _load():
        """
        Actually loads the settings state

        @return: SettingsState
        """

        with open(savegame_path(), 'r', encoding=DEFAULT_ENCODING) as f:
            state = jsonpickle.decode(f.read())

            # jsonpickle don't calls __init__()
            # So when loading a state attributes added since then are missing
            # I added a version number
            # If the state version from the code is newer than the stored version
            # discard the old settings state and return a new one
            if SavegameState().version != state.version:
                return SavegameState()

            return state

    def save(self) -> None:
        """ Save settings as json file """

        directory = os.path.dirname(savegame_path())
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(savegame_path(), 'w', encoding=DEFAULT_ENCODING) as f:
            f.write(jsonpickle.encode(self, unpicklable=True))


    @property
    def version(self) -> int:
        """ State version"""

        return self._version

    @staticmethod
    def delete():
        """ Delete savegame """
        if SavegameState.exists():
            os.unlink(savegame_path())