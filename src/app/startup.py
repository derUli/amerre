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
from app.constants.settings import (
    SETTINGS_DEFAULT_FULLSCREEN,
    SETTINGS_DEFAULT_VSYNC,
    SETTINGS_DEFAULT_SIZE,
    SETTINGS_ANTIALIASING_CHOICES,
    SETTINGS_DEFAULT_ANTIALIASING, SETTINGS_DEFAULT_DRAW_RATE, SETTINGS_DEFAULT_UPDATE_RATE,
    SETTINGS_DEFAULT_VOLUME_MUSIC, SETTINGS_DEFAULT_VOLUME_SOUND, SETTINGS_DEFAULT_VOLUME_MASTER,
    SETTINGS_DEFAULT_VOLUME_SPEECH, SETTINGS_WINDOW_STYLE_CHOICES, SETTINGS_DEFAULT_WINDOW_STYLE
)
from app.gamewindow import GameWindow
from app.utils.audiovolumes import AudioVolumes
from app.utils.log import configure_logger, log_hardware_info
from app.utils.string import label_value

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
        configure_logger()

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

        fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        vsync = SETTINGS_DEFAULT_VSYNC

        args = self.get_args()
        logging.info(args)

        if args.fullscreen:
            fullscreen = True
        elif args.window:
            fullscreen = False

        if args.vsync:
            vsync = True
        elif args.no_vsync:
            vsync = False

        show_intro = True

        if args.intro:
            show_intro = True
        elif args.no_intro:
            show_intro = False

        size = args.size
        size = size.lower()
        width, height = size.split('x')
        width, height = int(width), int(height)

        try:
            width, height = int(width), int(height)
        except ValueError:
            logging.error('size has invalid format')
            return

        if width == 0 or height == 0:
            logging.error('Width and height must be greater than 0')
            return

        lang = list(locale.getlocale())

        if args.language:
            lang = [args.language]

        if not any(lang):
            lang = [DEFAULT_LOCALE]

        self.setup_locale(lang)

        samples = args.antialiasing
        antialiasing = samples > 0

        # Draw rate
        draw_rate = 1 / 99999

        if args.draw_rate > 0:
            draw_rate = 1 / args.draw_rate
        elif vsync:
            draw_rate = 1 / pyglet.display.get_display().get_default_screen().get_mode().rate

        # Update rate

        update_rate = 1 / 62

        if args.update_rate > 0:
            update_rate = 1 / args.update_rate

        if str(args.window_style).lower() == 'none':
            args.window_style = None

        window = GameWindow(
            fullscreen=fullscreen,
            visible=False,
            style=args.window_style,
            vsync=vsync,
            width=width,
            height=height,
            antialiasing=antialiasing,
            samples=samples,
            center_window=args.center_window,
            draw_rate=draw_rate,
            update_rate=update_rate,
            fixed_rate=update_rate
        )

        # Set window location based on arguments
        x, y = window.get_location()

        if args.x is not None:
            x = args.x

        if args.y is not None:
            y = args.y

        window.set_location(x, y)
        window.set_visible(True)

        self.log_version_info()
        log_hardware_info(window)

        volume_music = args.volume_music
        volume_sound = args.volume_sound
        volume_speech = args.volume_speech
        volume_master = args.volume_master

        window.setup(
            self._root_dir,
            show_intro=show_intro,
            show_fps=args.show_fps,
            audio_volumes=AudioVolumes(
                volume_music=volume_music,
                volume_sound=volume_sound,
                volume_master=volume_master,
                volume_speech=volume_speech
            )
        )
        arcade.run()

    @staticmethod
    def get_args() -> argparse.Namespace:
        """ Get args """

        parser = argparse.ArgumentParser()

        parser.add_argument(
            '--fullscreen',
            action='store_true',
            default=False,
            help='Run in fullscreen mode'
        )

        parser.add_argument(
            '--window',
            action='store_true',
            default=False,
            help='Run in windowed mode'
        )

        parser.add_argument(
            '--center-window',
            action='store_true',
            default=False,
            help='Center window on screen'
        )

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
            '--vsync',
            action='store_true',
            default=False,
            help='Enable VSync'
        )

        parser.add_argument(
            '--no-vsync',
            action='store_true',
            default=False,
            help='Disable VSync'
        )

        parser.add_argument(
            '--window-style',
            action='store',
            type=str,
            help='The window style',
            choices=SETTINGS_WINDOW_STYLE_CHOICES,
            default=SETTINGS_DEFAULT_WINDOW_STYLE
        )

        parser.add_argument(
            '--size',
            action='store',
            default=SETTINGS_DEFAULT_SIZE,
            help='Size of window'
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
            '--draw-rate',
            action='store',
            type=int,
            help='The draw rate',
            default=SETTINGS_DEFAULT_DRAW_RATE
        )

        parser.add_argument(
            '--update-rate',
            action='store',
            type=int,
            help='The update rate',
            default=SETTINGS_DEFAULT_UPDATE_RATE
        )

        parser.add_argument(
            '--antialiasing',
            action='store',
            type=int,
            help='The antialiasing level',
            choices=SETTINGS_ANTIALIASING_CHOICES,
            default=SETTINGS_DEFAULT_ANTIALIASING
        )

        parser.add_argument(
            '--show-fps',
            action='store_true',
            default=False,
            help='Show FPS'
        )

        parser.add_argument(
            '--volume-music',
            action='store',
            type=int,
            help='The music volume',
            default=SETTINGS_DEFAULT_VOLUME_MUSIC
        )

        parser.add_argument(
            '--volume-speech',
            action='store',
            type=int,
            help='The music volume',
            default=SETTINGS_DEFAULT_VOLUME_SPEECH
        )

        parser.add_argument(
            '--volume-sound',
            action='store',
            type=int,
            help='The sound volume',
            default=SETTINGS_DEFAULT_VOLUME_SOUND
        )

        parser.add_argument(
            '--volume-master',
            action='store',
            type=int,
            help='The master volume',
            default=SETTINGS_DEFAULT_VOLUME_MASTER
        )

        parser.add_argument(
            '--language',
            help='The language',
            type=str
        )

        return parser.parse_args()
