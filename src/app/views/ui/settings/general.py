""" General settings """

from arcade.gui.events import UIOnClickEvent, UIOnActionEvent

from app.helpers.gui import make_button, \
    make_restart_to_apply_settings_alert, make_vertical_ui_box_layout, \
    make_ui_anchor_layout
from app.helpers.localization import bool_to_on_off
from app.helpers.string import label_value
from app.views.ui.settings.settingsui import SettingsUi


class General(SettingsUi):
    """ General settings menu """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._btn_languages = {}

    def setup(self, on_close: callable, on_change: callable) -> None:
        """ Setup settings """

        super().setup(on_close, on_change)

        self._btn_languages = {}

        btn_vibration = make_button(
            text=label_value(
                _('Gamepad Vibration'), bool_to_on_off(self._state.rumble)
            ))
        btn_vibration.on_click = self.on_toggle_vibration

        btn_back = make_button(text=_('Back'))
        btn_back.on_click = self.on_back

        widgets = [
            btn_back,
            btn_vibration
        ]
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

    def refresh(self) -> None:
        """ On refresh """

        self.setup(self._on_close, self._on_change)

    def on_toggle_vibration(self, event: UIOnClickEvent) -> None:

        """ On toggle vibration """
        self._state.rumble = not self._state.rumble
        self._state.save()
        self.refresh()
