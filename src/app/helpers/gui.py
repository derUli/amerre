""" Gui helper """

import arcade.gui
from arcade.gui import UIMessageBox

from app.constants.fonts import FONT_SIZE_LABEL, FONT_DEFAULT
from app.constants.ui import BUTTON_WIDTH, MODAL_WIDTH, MODAL_HEIGHT


def make_label(text: str) -> arcade.gui.UILabel:
    """ Make a label """

    return arcade.gui.UILabel(
        text=text,
        font_name=FONT_DEFAULT,
        font_size=FONT_SIZE_LABEL
    )


def make_button(text: str) -> arcade.gui.UIFlatButton:
    """ Make a button """

    return arcade.gui.UIFlatButton(text=text, width=BUTTON_WIDTH)


def make_slider(
        value: float = 0,
        min_value: float = 0,
        max_value: float = 100,
) -> arcade.gui.UISlider:
    """ Make a slider """

    return arcade.gui.UISlider(
        value=value,
        min_value=min_value,
        max_value=max_value,
        width=BUTTON_WIDTH
    )


def make_alert(message_text: str) -> UIMessageBox:
    """ Make an alert """

    return arcade.gui.UIMessageBox(
        message_text=message_text,
        buttons=(_('OK'),),
        width=MODAL_WIDTH,
        height=MODAL_HEIGHT
    )

def make_restart_to_apply_settings_alert(
        on_action: callable
) -> UIMessageBox:
    """ Make an alert after changing settings """

    alert = make_alert(_('A restart is required to apply some settings.'))
    alert.on_action = on_action
    return alert