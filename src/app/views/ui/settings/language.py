""" Video settings """
import os

import arcade.gui
from arcade.gui.events import UIOnClickEvent, UIOnActionEvent

from app.constants.gameinfo import locales_translated
from app.helpers.gui import make_button, \
    make_restart_to_apply_settings_alert
from app.state.settingsstate import SettingsState


class Language(arcade.gui.UIManager):
    """ Settings settings """

    def __init__(self):
        """ Constructor """

        super().__init__()
        self._state = None
        self._on_close = None
        self._on_change = None
        self._btn_languages = {}

    def setup(self, on_close, on_change) -> None:
        """ Setup settings """

        self.disable()
        self.clear()
        self._btn_languages = {}
        self._on_close = on_close
        self._on_change = on_change
        self._state = SettingsState.load()

        locales = locales_translated()

        btn_back = make_button(text=_('Back'))
        btn_back.on_click = self.on_back

        widgets = [
            btn_back
        ]

        for l in locales:
            btn = make_button(locales[l])
            self._btn_languages[l] = btn
            btn.on_click = self.on_change_language
            widgets += [btn]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=20, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.add(arcade.gui.UIAnchorLayout())

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.enable()

    def on_change_language(self, event: UIOnClickEvent):
        old_lang = os.environ['LANG']
        new_lang = old_lang

        for key in self._btn_languages:
            if event.source == self._btn_languages[key]:
                new_lang = key
                break

        self._state.language = new_lang
        self._state.save()

        if old_lang == new_lang:
            self.on_back(event)
            return

        self.add(
            make_restart_to_apply_settings_alert(on_action=self.on_back)
        )

    def on_back(self, event: UIOnClickEvent | UIOnActionEvent):
        self.disable()
        self.clear()
        self._on_close()
