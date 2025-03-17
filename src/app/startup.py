""" Game startup """

import argparse
import gettext
import logging
import os
import sys

import arcade
import pyglet

from app.constants.gameinfo import VERSION_STRING
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

    def setup_locale(self, lang: str) -> None:
        """ setup locale """

        locale_path = os.path.join(self._root_dir, 'resources', 'locales')

        os.environ['LANG'] = lang
        logging.info(label_value('Language', os.environ['LANG']))
        gettext.install('messages', locale_path)

    @staticmethod
    def log_version_info():
        """ Log version info"""

        logging.info(label_value('Amerre version', VERSION_STRING))
        logging.info(label_value('Python version', sys.version))
        logging.info(label_value('Arcade version', arcade.version.VERSION))
        logging.info(label_value('Pyglet version', pyglet.version))
        logging.info(
            label_value('GIL', getattr(sys, '_is_gil_enabled', 'Unknown'))
        )

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

        state = SettingsState.load()

        self.setup_locale(state.language)

        # Create settings state on first launch
        if not state.exists():
            state.save()

        samples = state.antialiasing
        antialiasing = samples > 0

        # Update rate
        width, height = state.screen_resolution

        if not state.fullscreen and args.window_size:
            size = args.window_size.lower()
            window_size = size.split('x')
            try:
                window_size = list(map(int, window_size))
            except ValueError as e:
                logging.error(e)
                return

            width, height = window_size[0], window_size[1]

        window = GameWindow(
            fullscreen=state.fullscreen,
            visible=True,
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

        log_hardware_info()

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
            '--intro',
            action='store_true',
            default=False,
            help='Show intro'
        )


        parser.add_argument(
            '--window-size',
            action='store',
            default=None,
            help='Set the window size'
        )

        parser.add_argument(
            '--no-intro',
            action='store_true',
            default=False,
            help='Don\'t show intro'
        )

        return parser.parse_args()
