# pylint: disable=W0223

""" The Game window """

import logging
import os
import time

import arcade
import pyglet
from arcade.gui import UIFlatButton
from app.constants.fonts import FONT_DEFAULT, FONT_SIZE_BUTTON
from app.constants.input.keyboard import KEY_SCREENSHOT
from app.state.settingsstate import SettingsState
from app.utils.audiovolumes import AudioVolumes
from app.utils.fpscounter import FPSCounter
from app.helpers.paths import screenshot_path
from app.helpers.string import label_value
from app.views.logo import Logo
from app.views.mainmenu import MainMenu


class GameWindow(arcade.Window):
    """
    Main application class
    """

    def __init__(
            self,
            width: int = 1280,
            height: int = 720,
            fullscreen: bool = True,
            visible: bool = True,
            style: str | None = None,
            vsync: bool = True,
            draw_rate: float = 1 / 60,
            update_rate=1 / 60,
            center_window=False,
            antialiasing: bool = True,
            samples: int = 4,
            fixed_rate: float = 1 / 60

    ):
        """ Constructor """
        self._root_dir = None
        self._screen = None
        self._controller_manager = None
        self._controllers = []
        self._fps_counter = None
        self._audio_volumes = None

        # Call the parent class and set up the window
        super().__init__(
            width=width,
            height=height,
            title=_('Welcome to Amerre'),
            fullscreen=fullscreen,
            visible=visible,
            style=style,
            vsync=vsync,
            resizable=False,
            draw_rate=draw_rate,
            update_rate=update_rate,
            center_window=center_window,
            antialiasing=antialiasing,
            samples=samples,
            gc_mode='auto',
            fixed_rate=fixed_rate
        )

    def setup(
            self,
            root_dir: str,
            audio_volumes: AudioVolumes,
            show_intro: bool = True
    ):
        """ Set up the main window here"""

        self._root_dir = root_dir
        self._audio_volumes = audio_volumes

        icon = pyglet.image.load(
            os.path.join(root_dir, 'resources', 'images', 'ui', 'icon.ico')
        )
        self.set_icon(icon)
        self.setup_fonts()
        self.setup_controllers()

        if show_intro:
            view = Logo
        else:
            view = MainMenu

        self._fps_counter = FPSCounter().setup(self)

        state = SettingsState.load()

        if state.show_fps:
            arcade.enable_timings()

        self.show_view(view().setup(root_dir))

        self.setup_style()

    def setup_style(self):
        for style in UIFlatButton.DEFAULT_STYLE.values():
            style.font_name = FONT_DEFAULT
            style.font_size = FONT_SIZE_BUTTON

    @property
    def size(self):
        """ Window size """

        return self.width, self.height

    def setup_controllers(self):
        """ Setup controllers """

        self._controller_manager = pyglet.input.ControllerManager()
        controllers = self._controller_manager.get_controllers()
        for controller in controllers:
            logging.info(label_value('Controller connected', controller))

            controller.open()
            controller.push_handlers(self)

            self._controllers.append(controller)

        @self._controller_manager.event
        def on_connect(controller) -> None:
            """ On controller connect """

            logging.info(label_value('Controller connected', controller))

            controller.open()
            controller.push_handlers(self)

            self._controllers.append(controller)

        @self._controller_manager.event
        def on_disconnect(controller):
            """ On controller disconnect """

            logging.info(label_value('Controller disconnected', controller))
            controller.pop_handlers()
            controller.close()
            self._controllers.remove(controller)

    def setup_fonts(self):
        """ Load fonts """

        fonts = [
            'MarkerFelt.ttf',
            'consolamonobook.ttf'
        ]

        for font in fonts:
            arcade.load_font(
                os.path.join(
                    self._root_dir,
                    'resources',
                    'fonts',
                    font
                )
            )

    def on_button_press(self, joystick, key) -> None:
        """ On controller button pressed """

        if hasattr(self.current_view, 'on_button_press'):
            self.current_view.on_button_press(joystick, key)
        else:
            logging.debug(
                label_value(
                    self.current_view.__class__.__qualname__,
                    'on_button_press not implemented'
                )
            )

    def on_button_release(self, joystick, key) -> None:
        """ On controller button released """

        if hasattr(self.current_view, 'on_button_release'):
            self.current_view.on_button_release(joystick, key)
        else:
            logging.debug(
                label_value(
                    self.current_view.__class__.__qualname__,
                    'on_button_release not implemented'
                )
            )

    def on_stick_motion(self, joystick, stick, value):
        """ On stick motion """

        if hasattr(self.current_view, 'on_stick_motion'):
            self.current_view.on_stick_motion(joystick, stick, value)
        else:
            logging.debug(
                label_value(
                    self.current_view.__class__.__qualname__,
                    'on_stick_motion not implemented'
                )
            )

    def on_trigger_motion(self, joystick, stick, value):
        """ On stick motion """

        if hasattr(self.current_view, 'on_trigger_motion'):
            self.current_view.on_trigger_motion(joystick, stick, value)
        else:
            logging.debug(
                label_value(
                    self.current_view.__class__.__qualname__,
                    'on_trigger_motion not implemented'
                )
            )

    @property
    def controllers(self):
        """ Get controllers """

        return self._controllers

    def on_key_press(self, symbol: int, modifiers: int):
        """ On keyboard key presssed """

        if symbol in KEY_SCREENSHOT:
            self.on_screenshot()

    def on_screenshot(self):
        """ Save a screenshot """

        if not os.path.exists(screenshot_path()):
            os.makedirs(screenshot_path())

        filename = os.path.join(screenshot_path(), time.strftime("%Y%m%d-%H%M%S") + '.jpg')

        start = time.time()
        image = arcade.get_image().convert('RGB')
        image.save(filename, subsampling=0, quality=100)
        end = time.time() - start

        logging.info(f"Screenshot saved as {filename} in {end} seconds")

        sound = arcade.load_sound(
            os.path.join(self._root_dir, 'resources', 'sounds', 'common', 'screenshot.mp3')
        )
        sound.play(volume=self._audio_volumes.volume_sound_normalized)

        return filename

    def on_update(self, delta_time: float):
        """ On update """

        if self._fps_counter:
            self._fps_counter.update()

    def draw_after(self):
        """ Draw after view """

        if self._fps_counter:
            self._fps_counter.draw()

    @property
    def audio_volumes(self) -> AudioVolumes:
        """ Get audio volumes """

        return self._audio_volumes

    @audio_volumes.setter
    def audio_volumes(self, val: AudioVolumes) -> None:
        self._audio_volumes = val

    @property
    def root_dir(self):
        """ Root directory """
        return self._root_dir
