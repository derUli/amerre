""" Particles """
import logging
import random

import arcade.sprite

from app.constants.layers import LAYER_PARTICLES
from app.containers.effect_data import EffectData
from app.effects.effect import Effect
from app.state.settingsstate import SettingsState

PARTICLES_COUNT = 300
PARTICLES_RADIUS = 6
PARTICLES_Y_MIN = 600
PARTICLES_Y_MAX = 800
PARTICLE_SPEED = 15

PARTICLES_COLOR = (255, 255, 255)


class Particles(Effect):
    """ Effect """

    def setup(self, data: EffectData) -> None:
        """ Setup animation """

        super().setup(data)

        state = SettingsState.load()
        particles_count = int(PARTICLES_COUNT * state.particles)

        self.make_particles(particles_count)

    def on_update(self, delta_time: float) -> None:
        """
        Update it
        @param delta_time: float
        """

        for sprite in self._data.scene[LAYER_PARTICLES]:
            sprite.center_x -= PARTICLE_SPEED * delta_time
            if sprite.right < 0:
                sprite.center_x = (self._data.tilemap.width *
                                   self._data.tilemap.tile_width)
                sprite.center_y = random.randint(
                    PARTICLES_Y_MIN,
                    PARTICLES_Y_MAX
                )

    def draw(self) -> None:
        """ Draw effect """

        return

    def make_particles(self, particles_count: int) -> None:
        """
        Make particles
        """
        width = self._data.tilemap.width * self._data.tilemap.tile_width

        for i in range(0, particles_count):
            logging.debug(f"Make particle {i}")
            r, g, b = PARTICLES_COLOR
            a = random.randint(80, 180)
            color = r, g, b, a

            sprite = arcade.sprite.SpriteCircle(
                radius=random.randint(1, PARTICLES_RADIUS),
                color=color,
                soft=True
            )

            sprite.center_x = random.randint(1, width)
            sprite.center_y = random.randint(PARTICLES_Y_MIN, PARTICLES_Y_MAX)

            self._data.scene.add_sprite(LAYER_PARTICLES, sprite)

    def refresh(self):

        modifier = SettingsState.load().particles

        new_count = int(PARTICLES_COUNT * modifier)
        old_count = len(self._data.scene[LAYER_PARTICLES])
        if new_count == old_count:
            return

        if new_count > old_count:
            self.make_particles(new_count - old_count)
            return

        if new_count < old_count:
            diff = new_count - old_count

            sprites = self._data.scene[LAYER_PARTICLES][diff:]

            for sprite in sprites:
                self._data.scene[LAYER_PARTICLES].remove(sprite)
