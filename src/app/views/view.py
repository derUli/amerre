""" View """

import arcade

from app.constants.settings import FIXED_RATE
from app.state.settingsstate import SettingsState


class View(arcade.View):
    """ View """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._root_dir = None
        self._scene = None
        self._effects = []
        self._fade_sprite = None
        self._phase = None
        self._music = None
        self._state = None

    def setup(self, root_dir: str):
        """ Setup view """
        self._root_dir = root_dir
        self._scene = arcade.scene.Scene()
        self._state = SettingsState.load()

    def rumble(self, strength: int) -> None:
        """ Rumble controller """

        strength = strength * int (self._state.rumble)

        for controller in self.window.controllers:
            if strength > 0:
                controller.rumble_play_strong(strength, 1 / FIXED_RATE)
            else:
                controller.rumble_stop_strong()
