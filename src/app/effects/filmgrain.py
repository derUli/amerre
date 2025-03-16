""" Filmgrain effect """

import os

import arcade

from app.containers.effect_data import EffectData
from app.effects.effect import Effect

ALPHA = 19


class Filmgrain(Effect):
    """ Filmgrain effect """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self.camera = None
        self.grain = None
        self.spritelist = None

    def setup(self, data: EffectData) -> None:
        """ Setup animation """

        super().setup(data)

        self.camera = arcade.camera.Camera2D()

        self.grain = arcade.load_animated_gif(
            os.path.join(data.root_dir, 'resources', 'animations', 'grain.gif')
        )
        self.grain.size = arcade.get_window().get_size()
        self.grain.bottom = 0
        self.grain.left = 0
        self.spritelist = arcade.sprite_list.SpriteList()
        self.spritelist.append(self.grain)

        self.spritelist.alpha = ALPHA

    def update(self, delta_time: float) -> None:
        """
        Update it
        @param delta_time: Float
        """

        self.grain.update_animation(delta_time=delta_time)

    def draw(self) -> None:
        """ Draw it """

        self.camera.use()
        self.spritelist.draw()
