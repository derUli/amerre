""" Subtitle """

import logging
import os

import arcade
from arcade import SpriteList

from app.constants.fonts import FONT_DEFAULT
from app.constants.ui import MARGIN
from app.state.settingsstate import SettingsState

TEXT_COLOR = arcade.csscolor.WHITE


class Subtitle:
    """ Subtitle """

    def __init__(self):
        """ Constructor """
        self._texts = []
        self._rendered_texts = []
        self._current_text = None

    def load(self, filename: str) -> None:
        """ Load subtitle file """

        self.clear()

        filename_parts = os.path.splitext(filename)
        text_file = f"{filename_parts[0]}.txt"

        self._texts = []

        state = SettingsState.load()

        if not state.subtitle_enabled:
            return

        if state.subtitle_size == 0:
            return

        with open(text_file, 'r', encoding='UTF-8') as file:
            while line := file.readline():
                self._texts.append(line.rstrip())

        self._rendered_texts = []

        w = arcade.get_window().width

        for text in self._texts:

            parts = text.split(' ', maxsplit=1)

            font_size = state.subtitle_size

            sprite = arcade.create_text_sprite(
                text=parts[1],
                font_name=FONT_DEFAULT,
                font_size=font_size,
                color=TEXT_COLOR
            )

            if sprite.width > w:
                logging.warning(
                    f"Subtitle sprite width {sprite.width} is too large; {text}")

            sprite.center_x = w / 2
            sprite.bottom = MARGIN

            sprite_list = SpriteList(lazy=True)
            sprite_list.append(sprite)

            try:
                time = float(parts[0])
            except ValueError:
                logging.error(f"Can not parse subtitle timestamp {parts[0]}")
                continue

            self._rendered_texts.append({
                'time': time,
                'text': text,
                'sprite_list': sprite_list
            })

        self._current_text = self._rendered_texts[0]

    def on_update(self, player) -> None:
        """ Update subtitle """

        for text in self._rendered_texts:
            if player.time >= text['time']:
                self._current_text = text

    def clear(self) -> None:
        """ Clear """

        self._texts = []
        self._rendered_texts = []
        self._current_text = None

    def draw(self) -> None:
        """ Draw """

        if not self._current_text:
            return

        self._current_text['sprite_list'].draw()
