""" Video settings """

from arcade.gui.events import UIOnClickEvent, UIOnActionEvent

from app.constants.gameinfo import locales_translated
from app.helpers.gui import make_button, \
    make_restart_to_apply_settings_alert, make_vertical_ui_box_layout, \
    make_ui_anchor_layout
from app.views.ui.settings.settingsui import SettingsUi


class Language(SettingsUi):
    """ Settings settings """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._btn_languages = {}

    def setup(self, on_close: callable, on_change: callable) -> None:
        """ Setup settings """

        super().setup(on_close, on_change)

        self._btn_languages = {}

        locales = locales_translated()

        btn_back = make_button(text=_('Back'))
        btn_back.on_click = self.on_back

        widgets = [
            btn_back
        ]

        for value, text in locales.items():
            btn = make_button(text)
            btn.disabled = self._state.language == value

            self._btn_languages[value] = btn
            btn.on_click = self.on_change_language
            widgets += [btn]

        # Initialise a BoxLayout in which widgets can be arranged.
        self.add(make_ui_anchor_layout([make_vertical_ui_box_layout(widgets)]))

        self.enable()

    def on_change_language(self, event: UIOnClickEvent):
        """ On change language """

        new_lang = self._state.language

        for value, button in self._btn_languages.items():
            if event.source == button:
                new_lang = value
                break

        self._state.language = new_lang
        self._state.save()

        self.add(
            make_restart_to_apply_settings_alert(on_action=self.on_back)
        )

    def on_back(self, event: UIOnClickEvent | UIOnActionEvent):
        """ On back """
        self.disable()
        self.clear()
        self._on_close()
