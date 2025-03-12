""" Move clouds """

from app.constants.layers import LAYER_CLOUD
from app.effects.effect import Effect

CLOUD_SPEED = 0.25


class CloudAnimation(Effect):
    """ Move clouds """

    def setup(self, scene, tilemap, root_dir: str, options: dict = None):
        """ Setup animation """
        super().setup(scene, tilemap, root_dir, options)
        self._options['direction'] = 1

    def update(self, delta_time: float):
        """ Update animation"""

        clouds = self._scene[LAYER_CLOUD]

        width = self._tilemap.width * self._tilemap.tile_width

        change_direction = False
        for cloud in clouds:
            cloud.center_x -= self._options['cloudSpeed'] * self._options['direction']

            if self._options['direction'] == 1 and cloud.right <= 0:
                if self._options['cloudMode'] == 'texture':
                    change_direction = True
                else:
                    cloud.right = width - abs(cloud.right)

            if self._options['direction'] == -1 and cloud.right >= width - cloud.width:
                if self._options['cloudMode'] == 'texture':
                    change_direction = True

        if change_direction:
            self._options['direction'] *= -1
