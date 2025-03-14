""" Settings menu """
import logging

import arcade.gui
from arcade.gui import UIFlatButton

from app.constants.fonts import FONT_DEFAULT
from app.constants.ui import BUTTON_WIDTH
from app.views.ui.settings.audio import Audio
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

        btn_back = arcade.gui.UIFlatButton(text=_('Back'), width=BUTTON_WIDTH)
        btn_back.on_click = self.on_back

        btn_video = arcade.gui.UIFlatButton(text=_('Video'), width=BUTTON_WIDTH)
        btn_video.on_click = self.on_video

        btn_audio = arcade.gui.UIFlatButton(text=_('Audio'), width=BUTTON_WIDTH)
        btn_audio.on_click = self.on_audio

        widgets = [
            btn_back,
            btn_video,
            btn_audio
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=20, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.add(arcade.gui.UIAnchorLayout())

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

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
