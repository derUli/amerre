""" FPSCounter """

import logging
import time

import arcade

from app.constants.fonts import FONT_MONOTYPE
from app.state.settingsstate import SettingsState

FONT_SIZE_FPS = 14
FONT_COLOR_FPS = arcade.csscolor.WHITE
MAX_FPS_COUNT = 5000
MARGIN = 10
UPDATE_INTERVAL = 1


class FPSCounter:
    """ FPSCounter """

    def __init__(self):
        """ Constructor """
        self._fps_text = {}
        self._window = None
        self._current_fps = None
        self._fps_camera = None
        self._last_update = 0
        self._default_draw_rate = None

    def setup(self, window: arcade.Window):
        """ Setup FPSCounter """

        self._default_draw_rate = SettingsState.load().draw_rate
        self._fps_text = {}
        self._window = window
        self._fps_camera = arcade.camera.Camera2D()
        return self

    def update(self) -> None:
        """ Update fps counter """

        if not arcade.timings_enabled():
            self._current_fps = None
            return

        if time.time() < self._last_update + 1:
            return

        fps = round(arcade.get_fps())

        if fps == 0 and self._current_fps is None:
            fps = self._default_draw_rate

        # if current_fps is unchanged return here
        if str(fps) == self._current_fps:
            return

        self._current_fps = str(fps)

        fps_text = arcade.Text(
            self._current_fps,
            font_name=FONT_MONOTYPE,
            font_size=FONT_SIZE_FPS,
            color=FONT_COLOR_FPS,
            x=0,
            y=0
        )

        fps_text.x = MARGIN
        fps_text.y = self._window.height - MARGIN - fps_text.content_height / 2

        self._fps_text[self._current_fps] = fps_text

        fps_text_len = len(self._fps_text)
        if fps_text_len >= MAX_FPS_COUNT:
            keys = list(self._fps_text.keys())[-MAX_FPS_COUNT:]

            new_dict = {}

            for key in keys:
                new_dict[key] = self._fps_text[key]

            self._fps_text = new_dict
            logging.info('More than MAX_FPS_COUNT')

        self._last_update = time.time()

    def draw(self) -> None:
        """ Draw fps counter text """

        self._fps_camera.use()
        if self._current_fps and self._current_fps in self._fps_text:
            self._fps_text[self._current_fps].draw()
