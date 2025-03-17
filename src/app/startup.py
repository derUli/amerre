""" Game startup """

import argparse
import gettext
import locale
import logging
import os
import sys

import arcade
import pyglet

from app.constants.gameinfo import VERSION_STRING, DEFAULT_LOCALE
from app.constants.settings import (UPDATE_RATE, FIXED_RATE)
from app.gamewindow import GameWindow
from app.helpers.string import label_value
from app.state.settingsstate import SettingsState
from app.utils.log import log_hardware_info

try:
    import sounddevice
except OSError:
    sounddevice = None
except ImportError:
    sounddevice = None


class Startup:
    """ Game startup """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self.args = None
        self._root_dir = None
        self.args = None

    def setup(self, root_dir: str):
        """ Setup game startup """

        self._root_dir = root_dir

        return self

    def setup_locale(self, lang) -> None:
        """ setup locale """

        locale_path = os.path.join(self._root_dir, 'resources', 'locales')
        os.environ['LANG'] = lang[0]
        logging.info(label_value('Language', lang[0]))
        gettext.install('messages', locale_path)

    @staticmethod
    def log_version_info():
        """ Log version info"""

        logging.info(label_value('Amerre version', VERSION_STRING))
        logging.info(label_value('Python version', sys.version))
        logging.info(label_value('Arcade version', arcade.version.VERSION))
        logging.info(label_value('Pyglet version', pyglet.version))
        try:
            gil = sys._is_gil_enabled()
        except AttributeError:
            gil = None

        logging.info(label_value('GIL', gil))

    def start(self) -> None:
        """ Start game """

        args = self.get_args()
        logging.info(args)
        self.log_version_info()

        show_intro = True

        if args.intro:
            show_intro = True
        elif args.no_intro:
            show_intro = False

        lang = list(locale.getlocale())

        if args.language:
            lang = [args.language]

        if not any(lang):
            lang = [DEFAULT_LOCALE]

        self.setup_locale(lang)

        state = SettingsState.load()

        # Create settings state on first launch
        if not state.exists():
            state.save()

        samples = state.antialiasing
        antialiasing = samples > 0

        # Update rate
        width, height = state.screen_resolution

        window = GameWindow(
            fullscreen=state.fullscreen,
            visible=False,
            vsync=state.vsync,
            width=width,
            height=height,
            antialiasing=antialiasing,
            samples=samples,
            center_window=True,
            draw_rate=1.0 / state.actual_draw_rate,
            update_rate=1.0 / UPDATE_RATE,
            fixed_rate=1.0 / FIXED_RATE
        )

        # Set window location based on arguments
        x, y = window.get_location()

        if args.x is not None:
            x = args.x

        if args.y is not None:
            y = args.y

        window.set_location(x, y)
        window.set_visible(True)

        log_hardware_info(window)

        window.setup(
            self._root_dir,
            show_intro=show_intro,
            audio_volumes=state.audio_volumes
        )
        arcade.run()

    @staticmethod
    def get_args() -> argparse.Namespace:
        """ Get args """

        parser = argparse.ArgumentParser()

        parser.add_argument(
            '-x',
            action='store',
            type=int,
            required=False,
            help='The X position of the window'
        )

        parser.add_argument(
            '-y',
            action='store',
            type=int,
            required=False,
            help='The X position of the window'
        )

        parser.add_argument(
            '--intro',
            action='store_true',
            default=False,
            help='Show intro'
        )

        parser.add_argument(
            '--no-intro',
            action='store_true',
            default=False,
            help='Don\'t show intro'
        )

        parser.add_argument(
            '--language',
            help='The language',
            type=str
        )

        return parser.parse_args()
