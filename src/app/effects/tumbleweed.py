""" Move clouds """
import random

from app.containers.effect_data import EffectData
from app.effects.effect import Effect
from app.state.settingsstate import SettingsState

MOVE_SPEED = 1000
MOVE_ANGLE = 500

LAYER_NAME = 'Tumbleweed'

RANDOMIZE_DELTA = 1


class Tumbleweed(Effect):
    """ Move clouds """

    def setup(self, data: EffectData) -> None:
        super().setup(data)

        self._data.options['delta'] = 0
        self._data.options['particles'] = SettingsState.load().particles

    def on_update(self, delta_time: float):
        """ Update animation"""

        self._data.options['delta'] += delta_time

        sprites = self._data.scene[LAYER_NAME]

        if not 'initialized' in self._data.options:
            for sprite in sprites:
                sprite.visible = False
                self._data.options['initialized'] = False
            return

        for sprite in sprites:
            if sprite.visible:
                sprite.left -= (MOVE_SPEED * delta_time)
                sprite.angle -= (MOVE_ANGLE * delta_time)

                if sprite.right <= 0:
                    sprite.visible = False

        not_visible = list(filter(lambda s: not s.visible, sprites))

        if not any(not_visible):
            return

        if self._data.options['delta'] < RANDOMIZE_DELTA:
            return

        self._data.options['delta'] = 0

        visible = list(filter(lambda s: s.visible, sprites))
        max_count = max(2, int(len(sprites) * self._data.options['particles']))

        if len(visible) >= max_count:
            return

        if random.randint(1, 10) == 1:
            sprite = random.choice(list(not_visible))
            sprite.visible = True
            sprite.left = self._data.tilemap.width * self._data.tilemap.tile_width

    def refresh(self) -> None:
        self._data.options['particles'] = SettingsState.load().particles

        sprites = self._data.scene[LAYER_NAME]

        visible = list(filter(lambda s: s.visible, sprites))
        max_count = max(2, int(len(sprites) * self._data.options['particles']))

        if len(visible) < max_count:
            return

        remove_count = len(visible) - max_count

        for sprite in visible[remove_count:]:
            sprite.visible = False
