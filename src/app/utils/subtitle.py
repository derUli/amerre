import logging
import os

import arcade
from arcade import SpriteList

from app.constants.fonts import FONT_CONSOLA_MONO

MARGIN = 10
FONT_SIZE = 20

TEXT_COLOR = arcade.csscolor.WHITE

class Subtitle:
    def __init__(self):
        self._texts = []
        self._rendered_texts = []
        self._current_text = None

    def load(self, source, filename: str) -> None:

        self.clear()

        if not source:
            return

        filename_parts = os.path.splitext(filename)
        text_file = f"{filename_parts[0]}.txt"

        self._texts = []

        with open(text_file, 'r', encoding='UTF-8') as file:
            while line := file.readline():
                self._texts.append(line.rstrip())

        self._rendered_texts = []

        for text in self._texts:

            parts = text.split(' ', maxsplit=1)

            sprite = arcade.create_text_sprite(
                text=parts[1],
                font_name=FONT_CONSOLA_MONO,
                font_size=FONT_SIZE,
                bold=True,
                color=TEXT_COLOR
            )

            sprite.center_x = arcade.get_window().width / 2
            sprite.bottom = MARGIN

            sprite_list = SpriteList(lazy=True)
            sprite_list.append(sprite)

            try:
                time = float(parts[0])
                logging.error(f"Can not parse subtitle timestamp {time}")
            except ValueError:
                continue

            self._rendered_texts.append({
                'time': time,
                'text': text,
                'sprite_list': sprite_list
            })

        self._current_text = self._rendered_texts[0]

    def update(self, player):

        for text in self._rendered_texts:
            if player.time >= text['time']:
                self._current_text = text

    def clear(self):
        self._texts = []
        self._rendered_texts = []
        self._current_text = None

    def draw(self):
        if not self._current_text:
            return

        self._current_text['sprite_list'].draw()