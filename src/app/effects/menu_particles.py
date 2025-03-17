""" Menu background particles """

import random

import arcade

from app.containers.effect_data import EffectData
from app.effects.effect import Effect
from app.state.settingsstate import SettingsState

PARTICLES_SIZE_RANGE = 8
PARTICLE_SPEED = 100
PARTICLES_COUNT = 500

PARTICLE_COLORS = [
    (228, 255, 4, 200),
    (210, 210, 210, 200),
    (111, 186, 241, 200)
]

SCENE_LAYER_PARTICLES = 'particles'


class MenuParticles(Effect):
    """ Menu background particles """

    def setup(self, data: EffectData) -> None:
        """ Setup effect """

        self._data = data

        try:
            self._data.scene[SCENE_LAYER_PARTICLES].clear()
        except KeyError:
            pass

        state = SettingsState.load()
        particles_count = int(PARTICLES_COUNT * state.particles)

        self.make(particles_count)

    def on_update(self, delta_time: float) -> None:
        """ On update """
        w, h = arcade.get_window().get_size()

        particles = self._data.scene[SCENE_LAYER_PARTICLES]
        for particle in particles:
            particle.center_x -= PARTICLE_SPEED * delta_time

            if particle.right < 0:
                particle.center_x = w + particle.width
                particle.center_y = random.randint(0, h)

    def refresh(self) -> None:
        """ On refresh """

        modifier = SettingsState.load().particles
        new_count = int(PARTICLES_COUNT * modifier)
        old_count = len(self._data.scene[SCENE_LAYER_PARTICLES])
        if new_count == old_count:
            return

        if new_count > old_count:
            self.make(new_count - old_count)
            return

        if new_count < old_count:
            diff = new_count - old_count

            sprites = self._data.scene[SCENE_LAYER_PARTICLES][diff:]

            for sprite in sprites:
                self._data.scene[SCENE_LAYER_PARTICLES].remove(sprite)

    def make(self, particles_count: int) -> None:
        """ Make particles """

        for i in range(0, particles_count):
            sprite = arcade.sprite.SpriteCircle(
                color=random.choice(PARTICLE_COLORS),
                soft=True,
                radius=random.randint(1, PARTICLES_SIZE_RANGE)
            )

            w, h = arcade.get_window().get_size()

            sprite.center_x = random.randint(0, w)
            sprite.center_y = random.randint(0, h)

            self._data.scene.add_sprite(SCENE_LAYER_PARTICLES, sprite)
