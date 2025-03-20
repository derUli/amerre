""" Entity base class """

import arcade.sprite

class Entity:
    """ Entity base class """

    def __init__(self):
        """ Constructor """

        self._sprite = None
        self._initial_position = (0, 0)

    def setup(self, sprite: arcade.sprite.Sprite) -> None:
        """ Entity base class """

        self._sprite = sprite
        self._initial_position = sprite.position

    @property
    def sprite(self) -> arcade.sprite.Sprite:
        """ Get the sprite """

        return self._sprite

    @property
    def initial_position(self) -> tuple:
        """ Get the initial position"""

        return self._initial_position

    @property
    def position(self) -> tuple:
        """ Get the position"""

        return self._sprite.position

    @position.setter
    def position(self, pos: tuple) -> None:
        """ Set the position """

        self._sprite.position = pos

    def reset_initial_position(self) -> None:
        """ Reset the initial position """

        self.position = self._initial_position

    def on_update(self):
        """ On update """

        pass