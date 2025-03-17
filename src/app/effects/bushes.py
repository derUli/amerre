""" Bush effect """

import arcade

from app.constants.layers import LAYER_BUSH, LAYER_PLAYER
from app.constants.ui import FADE_SPEED
from app.effects.effect import Effect

ALPHA_MAX = 255
ALPHA_MIN = 255 * 0.4

MIN_DISTANCE = 64


class Bushes(Effect):
    """ Bushes effect """

    def on_fixed_update(self, delta_time: float) -> None:
        """
        Update it
        @param delta_time: Float
        """

        try:
            sprites = self._data.scene[LAYER_BUSH]
        except arcade.scene.SceneKeyError:
            return

        collides = False
        player = self._data.scene[LAYER_PLAYER][0]

        for sprite in sprites:
            if arcade.get_distance_between_sprites(sprite,
                                                   player) < MIN_DISTANCE:
                collides = True
                break

        for sprite in sprites:
            if collides:
                sprite.alpha = max(ALPHA_MIN, sprite.alpha - FADE_SPEED)
            else:
                sprite.alpha = min(ALPHA_MAX, sprite.alpha + FADE_SPEED)
