""" Filmgrain effect """

import os

import arcade

from app.containers.effect_data import EffectData
from app.effects.effect import Effect

ALPHA = 20


class Filmgrain(Effect):
    """ Filmgrain effect """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._camera = None
        self._grain = None
        self._spritelist = None

    def setup(self, data: EffectData) -> None:
        """ Setup animation """

        super().setup(data)

        self._camera = arcade.camera.Camera2D()

        self._grain = arcade.load_animated_gif(
            os.path.join(data.root_dir, 'resources', 'animations', 'grain.gif')
        )
        self._grain.size = arcade.get_window().get_size()
        self._grain.bottom = 0
        self._grain.left = 0
        self._spritelist = arcade.sprite_list.SpriteList()
        self._spritelist.append(self._grain)

        self._spritelist.alpha = ALPHA

    def on_update(self, delta_time: float) -> None:
        """
        Update it
        @param delta_time: Float
        """

        self._grain.update_animation(delta_time=delta_time)

    def draw(self) -> None:
        """ Draw it """

        self._camera.use()
        self._spritelist.draw()
