""" Settings UI base """

import arcade.gui

from app.state.settingsstate import SettingsState


class SettingsUi(arcade.gui.UIManager):
    """ Settings UI base """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._state = None
        self._old_state = None
        self._on_close = None
        self._on_change = None
        self._in_game = False

    def setup(self, on_close: callable, on_change: callable) -> None:
        """ Setup settings UI"""

        self._on_close = on_close
        self._on_change = on_change

        self._state = SettingsState.load()

        if not self._old_state:
            self._old_state = SettingsState.load()

        self.disable()
        self.clear()

    @property
    def in_game(self) -> bool:
        return self._in_game

    @in_game.setter
    def in_game(self, value: bool) -> None:
        self._in_game = value
