""" Move clouds """
import random

import arcade

from app.constants.layers import LAYER_CLOUD
from app.effects.effect import Effect
from app.state.settingsstate import SettingsState

MOVE_SPEED = 10
MOVE_ANGLE = 5

LAYER_NAME = 'Tumbleweed'

class Tumbleweed(Effect):
    """ Move clouds """

    def update(self, delta_time: float):
        """ Update animation"""

        sprites = self._scene[LAYER_NAME]

        if not 'initialized' in self._options:
            for sprite in sprites:
                sprite.visible = False
                self._options['initialized'] = False
            return


        for sprite in sprites:
            if sprite.visible:
                sprite.left -= MOVE_SPEED
                sprite.angle -= MOVE_ANGLE

                if sprite.right <= 0:
                    sprite.visible = False


        not_visible = list(filter(lambda s: not s.visible, sprites))

        if not any(not_visible):
            return

        if random.randint(1, 200) == 10:
            sprite = random.choice(list(not_visible))
            sprite.visible = True
            sprite.left = self._tilemap.width * self._tilemap.tile_width