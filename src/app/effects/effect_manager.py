""" Effect manager """

import arcade.scene

from app.containers.effect_data import EffectData
from app.effects.bushes import Bushes
from app.effects.cloudanimation import CloudAnimation
from app.effects.filmgrain import Filmgrain
from app.effects.particles import Particles
from app.effects.tumbleweed import Tumbleweed
from app.effects.vhs import Vhs


class EffectManager:
    """ Effect manager """

    def __init__(self):
        """ Constructor """

        self._animations = []
        self._vhs = None

    def setup(
            self,
            map_config: dict,
            scene: arcade.scene.Scene,
            tilemap: arcade.TileMap,
            root_dir: str
    ):
        """ Setup effects """

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

        self._vhs = Vhs()

        animations += [
            CloudAnimation(),
            Bushes(),
            self._vhs,
            Filmgrain()
        ]
        self._animations = animations

        for animation in self._animations:
            animation.setup(data)

        self._animations = animations

    def on_update(self, delta_time: float):
        """ Update all effects """

        for animation in self._animations:
            animation.on_update(delta_time)

    def on_fixed_update(self, delta_time: float):
        """ Update all effects """
        for animation in self._animations:
            animation.on_fixed_update(delta_time)

    def draw(self) -> None:
        """ Draw all effects """

        for animation in self._animations:
            animation.draw()

    def refresh(self) -> None:
        """ Refresh all effects after changing settings """

        for animation in self._animations:
            animation.refresh()


    @property
    def vhs(self) -> Vhs:
        return self._vhs
