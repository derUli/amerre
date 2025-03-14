""" Moving clouds """

from app.constants.layers import LAYER_CLOUD
from app.containers.effect_data import EffectData
from app.effects.effect import Effect


class CloudAnimation(Effect):
    """ Moving clouds """

    def setup(self, data: EffectData) -> None:
        """ Setup animation """

        super().setup(data)
        self._data.options['direction'] = 1

    def update(self, delta_time: float):
        """ Update animation"""

        clouds = self._data.scene[LAYER_CLOUD]

        width = self._data.tilemap.width * self._data.tilemap.tile_width

        change_direction = False
        for cloud in clouds:
            cloud.center_x -= self._data.options['cloudSpeed'] * self._data.options['direction'] * delta_time

            if self._data.options['direction'] == 1 and cloud.right <= 0:
                if self._data.options['cloudMode'] == 'texture':
                    change_direction = True
                else:
                    cloud.right = width - abs(cloud.right)

            if self._data.options['direction'] == -1 and cloud.right >= width - cloud.width:
                if self._data.options['cloudMode'] == 'texture':
                    change_direction = True

        if change_direction:
            self._data.options['direction'] *= -1
