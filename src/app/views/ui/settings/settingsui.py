import arcade.gui

from app.state.settingsstate import SettingsState


class SettingsUi(arcade.gui.UIManager):
    def __init__(self):
        super().__init__()

        self._state = None
        self._old_state = None
        self._on_close = None
        self._on_change = None

    def setup(self, on_close: callable, on_change: callable) -> None:
        self._on_close = on_close
        self._on_change = on_change

        self._state = SettingsState.load()

        if not self._old_state:
            self._old_state = SettingsState.load()

        self.disable()
        self.clear()
