""" VHS effect """

import os
import random

import arcade

from app.containers.effect_data import EffectData
from app.effects.effect import Effect

ALPHA_MIN = 0
ALPHA_SPEED = 1
ALPHA_MAX = 18


class Vhs(Effect):
    """ VHS effect """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._camera = None
        self._vhs = None
        self._spritelist = None
        self._enabled = False

    def setup(self, data: EffectData) -> None:
        """ Setup animation """

        super().setup(data)

        self._camera = arcade.camera.Camera2D()

        self._vhs = arcade.load_animated_gif(
            os.path.join(data.root_dir, 'resources', 'animations', 'vhs.gif')
        )
        self._vhs.size = arcade.get_window().get_size()
        self._vhs.bottom = 0
        self._vhs.left = 0
        self._spritelist = arcade.sprite_list.SpriteList()
        self._spritelist.append(self._vhs)

        self._spritelist.alpha = 0

    def on_fixed_update(self, delta_time: float) -> None:
        """
        Update it
        @param delta_time: Float
        """

        if not self._enabled:
            if self._spritelist.alpha >= ALPHA_MIN:
                self._spritelist.alpha = max(
                    ALPHA_MIN,
                    self._spritelist.alpha - ALPHA_SPEED
                )
            else:
                self._spritelist.visible = False
            return

        self._spritelist.visible = True
        self._spritelist.alpha = min(
            ALPHA_MAX,
            self._spritelist.alpha + ALPHA_SPEED
        )

        self._vhs.update_animation(delta_time=delta_time)

    def draw(self) -> None:
        """ Draw it """

        self._camera.use()
        self._spritelist.draw()

    @property
    def enabled(self) -> bool:
        """ Get enabled state """

        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """ Set enabled state"""

        if value and not self._enabled:
            self._vhs.angle = random.choice([0, 180])

        self._enabled = value
