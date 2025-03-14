import arcade.gui

from app.constants.fonts import FONT_SIZE_LABEL, FONT_DEFAULT
from app.constants.ui import BUTTON_WIDTH


def make_label(text: str) -> arcade.gui.UILabel:
    return arcade.gui.UILabel(
        text=text,
        font_name=FONT_DEFAULT,
        font_size=FONT_SIZE_LABEL
    )

def make_button(text: str) -> arcade.gui.UIFlatButton:
    return arcade.gui.UIFlatButton(text=text, width=BUTTON_WIDTH)