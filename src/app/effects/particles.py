""" Particles """
import random

import arcade.sprite

from app.constants.layers import LAYER_PARTICLES
from app.effects.effect import Effect

PARTICLES_COUNT = 300
PARTICLES_RADIUS = 6
PARTICLES_Y_MIN = 370
PARTICLES_Y_MAX = 800
PARTICLE_SPEED = 0.2

PARTICLES_COLOR = (255, 255, 255)


class Particles(Effect):
    """ Effect """

    def setup(self, scene, tilemap, root_dir: str):
        """ Setup animation """
        super().setup(scene, tilemap, root_dir)

        width = tilemap.width * tilemap.tile_width
        for i in range(0, PARTICLES_COUNT):
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

            # sprite.change_y -= random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)

            scene.add_sprite(LAYER_PARTICLES, sprite)

    def update(self, delta_time: float) -> None:
        """
        Update it
        @param delta_time: float
        """

        for sprite in self._scene[LAYER_PARTICLES]:
            sprite.center_x -= PARTICLE_SPEED
            if sprite.right < 0:
                sprite.center_x = self._tilemap.width * self._tilemap.tile_width
                sprite.center_y = random.randint(PARTICLES_Y_MIN, PARTICLES_Y_MAX)

    def draw(self) -> None:
        """ Draw effect """

        return
