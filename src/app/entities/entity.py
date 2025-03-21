""" Entity base class """
import logging

import arcade.sprite

class Entity:
    """ Entity base class """

    def __init__(self):
        """ Constructor """

        self._sprite = None
        self._initial_position = (0, 0)
        self._root_dir = None

    def setup(self, sprite: arcade.sprite.Sprite, root_dir) -> None:
        """ Entity base class """

        self._sprite = sprite
        self._initial_position = sprite.position
        self._root_dir = root_dir

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

    def on_update(self, delta_time: float):
        """ On update """

        return

    def refresh(self):
        """ On refresh """

        return

    @property
    def alpha(self) -> int:
        """ Get alpha """

        return self._sprite.alpha

    @alpha.setter
    def alpha(self, value: int) -> None:
        """ Set alpha """

        self._sprite.alpha = value


    @property
    def angle(self) -> float:
        """ Get angle """

        return self._sprite.angle

    @angle.setter
    def angle(self, value: float) -> None:
        """ Set angle """

        self._sprite.angle = value