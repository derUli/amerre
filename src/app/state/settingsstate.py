""" Settings state """

import logging
import os

import jsonpickle

from app.constants.gameinfo import DEFAULT_ENCODING, BASE_HEIGHT, BASE_WIDTH
from app.constants.settings import (
    SETTINGS_DEFAULT_SHOW_FPS, \
    SETTINGS_DEFAULT_VSYNC, \
    SETTINGS_DEFAULT_FULLSCREEN,
    SETTINGS_DEFAULT_VOLUME_MUSIC, \
    SETTINGS_DEFAULT_VOLUME_SOUND,
    SETTINGS_DEFAULT_VOLUME_MASTER, \
    SETTINGS_DEFAULT_VOLUME_SPEECH, \
    SETTINGS_DEFAULT_SUBTITLE_SIZE,
    SETTINGS_DEFAULT_SUBTITLE_ENABLED, \
    SETTINGS_DEFAULT_ANTIALIASING, \
    SETTINGS_DEFAULT_PARTICLES,
    SETTINGS_DEFAULT_DRAW_RATE, \
    SETTINGS_DEFAULT_DEBUG, SETTINGS_DEFAULT_AUDIO_DRIVER,
    SETTINGS_DEFAULT_RUMBLE
)
from app.helpers.display import fullscreen_resolution, window_resolution, \
    default_rate
from app.helpers.localization import default_language
from app.helpers.paths import settings_path
from app.utils.audiovolumes import AudioVolumes

VERSION = 3


class SettingsState:
    """ Game settings """

    def __init__(self):
        """ Constructor """

        self._version = VERSION

        # Video
        self._vsync = SETTINGS_DEFAULT_VSYNC
        self._show_fps = SETTINGS_DEFAULT_SHOW_FPS
        self._fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self._antialiasing = SETTINGS_DEFAULT_ANTIALIASING
        self._particles = SETTINGS_DEFAULT_PARTICLES
        self._draw_rate = SETTINGS_DEFAULT_DRAW_RATE
        self._base_width = BASE_WIDTH
        self._base_height = BASE_HEIGHT

        # Audio
        self._audio_driver = SETTINGS_DEFAULT_AUDIO_DRIVER
        self._audio_volumes = AudioVolumes(
            volume_music=SETTINGS_DEFAULT_VOLUME_MUSIC,
            volume_sound=SETTINGS_DEFAULT_VOLUME_SOUND,
            volume_master=SETTINGS_DEFAULT_VOLUME_MASTER,
            volume_speech=SETTINGS_DEFAULT_VOLUME_SPEECH
        )

        # Subtitles
        self._subtitle_enabled = SETTINGS_DEFAULT_SUBTITLE_ENABLED
        self._subtitle_size = SETTINGS_DEFAULT_SUBTITLE_SIZE

        # General
        self._language = default_language()
        self._rumble = SETTINGS_DEFAULT_RUMBLE

        # Other
        self._debug = SETTINGS_DEFAULT_DEBUG

    @staticmethod
    def exists() -> bool:
        """ Check if there is an existing settings file for the launcher """

        return os.path.exists(settings_path())

    @staticmethod
    def load():
        """ Loads the settings state """

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

        with open(settings_path(), 'r', encoding=DEFAULT_ENCODING) as f:
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

        with open(settings_path(), 'w', encoding=DEFAULT_ENCODING) as f:
            f.write(jsonpickle.encode(self, unpicklable=True))

    @property
    def show_fps(self) -> bool:
        """ Show FPS """

        return self._show_fps

    @show_fps.setter
    def show_fps(self, value: bool) -> None:
        """ Show FPS """

        self._show_fps = value

    @property
    def vsync(self) -> bool:
        """ V-Sync """

        return self._vsync

    @vsync.setter
    def vsync(self, value: bool) -> None:
        """ V-Sync """

        self._vsync = value

    @property
    def fullscreen(self) -> bool:
        """ Fullscreen """

        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value: bool) -> None:
        """ Fullscreen """

        self._fullscreen = value

    @property
    def screen_resolution(self):
        """ Get the screen resolution for the screen mode """

        if self.fullscreen:
            return fullscreen_resolution()

        return window_resolution()

    @property
    def audio_volumes(self) -> AudioVolumes:
        """ Audio volumes """

        return self._audio_volumes

    @audio_volumes.setter
    def audio_volumes(self, value: AudioVolumes) -> None:
        """ Audio volumes """

        self.audio_volumes = value

    @property
    def subtitle_enabled(self) -> bool:
        """ Subtitles enabled """

        return self._subtitle_enabled

    @subtitle_enabled.setter
    def subtitle_enabled(self, value: bool) -> None:
        """ Subtitles enabled """

        self._subtitle_enabled = value

    @property
    def subtitle_size(self) -> int:
        """ Subtitle size """

        return self._subtitle_size

    @subtitle_size.setter
    def subtitle_size(self, value: int) -> None:
        """ Subtitle size """

        self._subtitle_size = value

    @property
    def antialiasing(self) -> int:
        """ Get antialiasing """

        return self._antialiasing

    @antialiasing.setter
    def antialiasing(self, value: int) -> None:
        """ Set antialiasing """
        self._antialiasing = value

    @property
    def particles(self) -> float:
        """ Particle count modifier """

        return self._particles

    @particles.setter
    def particles(self, value: float) -> None:
        """ Particle count modifier """

        self._particles = value

    @property
    def draw_rate(self) -> int:
        """ Get the draw_rate """
        return self._draw_rate

    @draw_rate.setter
    def draw_rate(self, value: int) -> None:
        """ Set the draw_rate """
        self._draw_rate = value

    @property
    def actual_draw_rate(self) -> int:
        """ Actual draw rate depending on vsync """

        # If V-Sync is enabled and the draw_rate higher than the monitor
        # refresh rate return monitor refresh rate
        if self.vsync and self.draw_rate > default_rate():
            return default_rate()

        return self.draw_rate

    @property
    def debug(self) -> bool:
        """ Is debug mode enabled """

        return self._debug

    @property
    def audio_driver(self) -> str:
        """ Get audio driver """

        return self._audio_driver

    @audio_driver.setter
    def audio_driver(self, value: str) -> None:
        """ Set audio driver """

        self._audio_driver = value

    @property
    def version(self) -> int:
        """ State version"""

        return self._version

    @property
    def language(self) -> str:
        """ Get language """

        return self._language

    @language.setter
    def language(self, value: str) -> None:
        """ Set language """

        self._language = value

    @property
    def rumble(self) -> bool:
        """ Get rumble """

        return self._rumble

    @rumble.setter
    def rumble(self, value: bool) -> None:
        """ Set rumble """

        self._rumble = value

    @property
    def base_width(self) ->int:
        """ Get base width """

        return self._base_width

    @base_width.setter
    def base_width(self, value: int) -> None:
        """ Set base width """

        self._base_width = value

    @property
    def base_height(self) ->int:
        """ Get base height """

        return self._base_height

    @base_height.setter
    def base_height(self, value: int) -> None:
        """ Set base height """

        self._base_height = value