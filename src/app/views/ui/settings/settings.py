""" Settings menu """
import logging

import arcade.gui

from app.constants.ui import BUTTON_WIDTH
from app.views.ui.settings.video import Video


class Settings(arcade.gui.UIManager):
    """ Settings menu """

    def __init__(self):
        """ Constructor """
        super().__init__()

        self._callback = None

    def setup(self, callback) -> None:
        """ Setup settings """
        self.clear()
        self._callback = callback

        btn_back = arcade.gui.UIFlatButton(text=_('Back'), width=BUTTON_WIDTH)
        btn_back.on_click = self.on_back

        btn_video = arcade.gui.UIFlatButton(text=_('Video'), width=BUTTON_WIDTH)
        btn_video.on_click = self.on_video

        widgets = [
            btn_back,
            btn_video
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=20, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.enable()

    def on_video(self, event):
        self.disable()
        menu = Video()
        menu.setup(self.on_enable)
        self._callback(menu)

    def on_enable(self):
        self.enable()
        self._callback(self)

    def on_back(self, event):
        """ On go back """

        logging.debug(event)

        self.disable()
        self._callback()

