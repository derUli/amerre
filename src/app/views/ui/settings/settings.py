""" Settings menu """
import logging

import arcade.gui

from app.constants.ui import MARGIN
from app.helpers.gui import make_button, make_vertical_ui_box_layout
from app.views.ui.settings.audio import Audio
from app.views.ui.settings.language import Language
from app.views.ui.settings.video import Video


class Settings(arcade.gui.UIManager):
    """ Settings menu """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._on_close = None
        self._on_change = None

    def setup(self, on_close, on_change) -> None:
        """ Setup settings """

        self.clear()
        self._on_close = on_close
        self._on_change = on_change

        btn_back = make_button(text=_('Back'))
        btn_back.on_click = self.on_back

        btn_video = make_button(text=_('Video'))
        btn_video.on_click = self.on_video

        btn_audio = make_button(text=_('Audio'))
        btn_audio.on_click = self.on_audio

        btn_language = make_button(text=_('Language'))
        btn_language.on_click = self.on_language

        widgets = [
            btn_back,
            btn_video,
            btn_audio,
            btn_language
        ]

        frame = self.add(arcade.gui.UIAnchorLayout())

        frame.add(
            child=make_vertical_ui_box_layout(widgets),
            anchor_x="center_x",
            anchor_y="center_y"
        )

        self.enable()

    def on_video(self, event):
        self.disable()
        menu = Video()
        menu.setup(self.on_enable, self._on_change)
        self._on_close(menu)

    def on_audio(self, event):
        self.disable()
        menu = Audio()
        menu.setup(self.on_enable, self._on_change)
        self._on_close(menu)

    def on_language(self, event):
        self.disable()
        menu = Language()
        menu.setup(self.on_enable, self._on_change)
        self._on_close(menu)

    def on_enable(self, refresh_particles=False):

        self.enable()
        self._on_close(self)

    def on_back(self, event, refresh_particles=False):
        """ On go back """

        logging.debug(event)
        if refresh_particles:
            self._on_change(refresh_particles=True)

        self.disable()
        self._on_close()
