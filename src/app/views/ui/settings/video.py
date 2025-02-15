""" Video settings """
import logging

import arcade.gui

from app.constants.ui import BUTTON_WIDTH


class Video(arcade.gui.UIManager):
    """ Settings settings """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._callback = None

    def setup(self, callback) -> None:
        """ Setup settings """

        self.clear()
        self._callback = callback

        grid = arcade.gui.UIGridLayout(column_count=2, row_count=3, horizontal_spacing=20, vertical_spacing=20)

        btn_back = arcade.gui.UIFlatButton(text=_('Back'), width=BUTTON_WIDTH)
        btn_back.on_click = self.on_back
        grid.add(btn_back, col_num=0, row_num=0)

        layout = arcade.gui.UIAnchorLayout(anchor_x='center', anchor_y='center')
        layout.add(grid)

        self.add(layout)

        self.enable()

    def on_back(self, event):
        """ On go back """

        logging.debug(event)

        self.disable()
        self._callback()
