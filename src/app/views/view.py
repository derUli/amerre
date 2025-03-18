""" View """

import arcade


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

    def setup(self, root_dir: str):
        """ Setup view """
        self._root_dir = root_dir
        self._scene = arcade.scene.Scene()

    def rumble(self, strength: int) -> None:
        for controller in self.window.controllers:
            if strength > 0:
                controller.rumble_play_strong(strength)
            else:
                controller.rumble_stop_strong()
