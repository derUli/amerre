""" Eagles clouds """
import os
import random

from app.constants.layers import LAYER_EAGLE
from app.containers.effect_data import EffectData
from app.effects.effect import Effect
from app.helpers.sprite import load_animated_gif

FACE_LEFT = 0
FACE_RIGHT = 1

MOVE_SPEED = 100


class Eagle:
    def __init__(self, sprite):
        self._sprite = sprite
        self.animations = []
        self._face = FACE_LEFT
        self.move_x = 0

    def setup(self, data: EffectData):
        """ Set up the eagle animations """

        path = os.path.join(
            data.root_dir,
            'resources',
            'images',
            'sprites',
            'eagle',
            'flying',
            'animation.gif'
        )
        position = self._sprite.position

        self.animations = [
            load_animated_gif(path),
            load_animated_gif(path, flip_horizontally=True)
        ]

        for animation in self.animations:
            animation.position = position

            animation.scale = 0.5
            animation.visible = False
            data.scene.add_sprite(LAYER_EAGLE, animation)

        # Remove  initial sprite
        self._sprite.remove_from_sprite_lists()

        self._face = random.choice([FACE_LEFT, FACE_RIGHT])
        self._sprite = self.animations[self._face]

    @property
    def center_x(self) -> float:
        return self.animations[0].center_x

    @center_x.setter
    def center_x(self, value: float) -> None:
        for animation in self.animations:
            animation.center_x = value

    @property
    def face(self) -> int:
        return self._face

    @face.setter
    def face(self, value: int) -> None:
        self._face = value

        for animation in self.animations:
            animation.visible = False

        self.animations[self._face].visible = True


class Eagles(Effect):
    """ Eagles clouds """

    def setup(self, data: EffectData) -> None:
        """ Setup animation """

        super().setup(data)

        try:
            eagles = data.scene[LAYER_EAGLE]
        except KeyError:
            eagles = []

        eagles = list(map(Eagle, eagles))
        list(map(lambda eagle: eagle.setup(data), eagles))

        self._data.options['eagles'] = eagles

    def on_update(self, delta_time: float):
        """ Update animation"""

        for eagle in self._data.options['eagles']:

            if eagle.move_x <= 0:
                if eagle.face == FACE_RIGHT:
                    eagle.face = FACE_LEFT
                else:
                    eagle.face = FACE_RIGHT

                eagle.move_x = random.randint(1000, 5000)

                if eagle.center_x < 0:
                    eagle.face = FACE_RIGHT
                if eagle.center_x > self._data.tilemap.width * self._data.tilemap.tile_width:
                    eagle.face = FACE_LEFT

                break

            if eagle.face == FACE_RIGHT:
                move = MOVE_SPEED * delta_time
                eagle.move_x -= move
                eagle.center_x += move

            if eagle.face == FACE_LEFT:
                move = MOVE_SPEED * delta_time
                eagle.move_x -= move
                eagle.center_x -= move
