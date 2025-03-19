import arcade.gui


class SettingsUi(arcade.gui.UIManager):
    def __init__(self):
        super().__init__()

        self._state = None
        self._old_state = None
        self._on_close = None
        self._on_change = None
