import arcade.scene

from app.containers.effect_data import EffectData
from app.effects.bushes import Bushes
from app.effects.cloudanimation import CloudAnimation
from app.effects.filmgrain import Filmgrain
from app.effects.particles import Particles
from app.effects.tumbleweed import Tumbleweed


class EffectManager:

    def __init__(self):
        self._animations = []

    def setup(
            self,
            map_config: dict,
            scene: arcade.scene.Scene,
            tilemap: arcade.TileMap,
            root_dir: str
    ):

        data = EffectData(
            scene,
            tilemap,
            root_dir,
            map_config
        )

        animations = []

        if 'particles' in map_config and map_config['particles']:
            animations += [Particles()]

        if 'tumbleweed' in map_config and map_config['tumbleweed']:
            animations += [Tumbleweed()]

        animations += [
            CloudAnimation(),
            Bushes(),
            Filmgrain()
        ]
        self._animations = animations

        for animation in self._animations:
            animation.setup(data)

        self._animations = animations

    def update(self, delta_time: float):
        for animation in self._animations:
            animation.update(delta_time)

    def draw(self):
        for animation in self._animations:
            animation.draw()

    def refresh(self):
        for animation in self._animations:
            animation.refresh()
