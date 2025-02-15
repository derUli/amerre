""" Video settings """
import logging

import arcade.gui

from app.constants.ui import BUTTON_WIDTH
from app.state.settingsstate import SettingsState


class Video(arcade.gui.UIManager):
    """ Settings settings """

    def __init__(self):
        """ Constructor """

        super().__init__()
        self._state = None
        self._callback = None

    def setup(self, callback) -> None:
        """ Setup settings """

        self.disable()
        self.clear()
        self._callback = callback
        self._state = SettingsState.load()

        grid = arcade.gui.UIGridLayout(column_count=2, row_count=1, vertical_spacing=20)

        btn_back = arcade.gui.UIFlatButton(text=_('Back'), width=BUTTON_WIDTH)
        btn_back.on_click = self.on_back
        grid.add(btn_back, col_num=0, row_num=0)

        fps_text = _('Off')
        if arcade.timings_enabled():
            fps_text = _('On')

        btn_toggle_fps = arcade.gui.UIFlatButton(
            text=': '.join([_('Show FPS'), fps_text]),
            width=BUTTON_WIDTH
        )
        btn_toggle_fps.on_click = self.on_toggle_fps
        grid.add(btn_toggle_fps, col_num=1, row_num=0)

        widgets = [
            btn_back,
            btn_toggle_fps
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=20, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.enable()

    def on_back(self, event):
        """ On go back """

        logging.debug(event)

        self.disable()
        self._callback()


    def on_toggle_fps(self, event):

        logging.debug(event)

        if arcade.timings_enabled():
            arcade.disable_timings()
        else:
            arcade.enable_timings()

        self._state.show_fps = arcade.timings_enabled()
        self._state.save()

        self.setup(self._callback)
