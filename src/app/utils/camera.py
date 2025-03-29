""" Player camera """

import arcade
from arcade import Rect, Window
from arcade.camera import Camera2D
from arcade.camera.data_types import DEFAULT_NEAR_ORTHO, DEFAULT_FAR
from arcade.gl import Framebuffer
from arcade.types import Point2

from app.state.settingsstate import SettingsState

# Max offset
OFFSET_MAX = 300
OFFSET_SPEED = 300


class Camera(Camera2D):
    """ Player camera """

    def __init__(
            self,
            viewport: Rect | None = None,
            position: Point2 | None = None,
            up: tuple[float, float] = (0.0, 1.0),
            zoom: float = 1.0,
            projection: Rect | None = None,
            near: float = DEFAULT_NEAR_ORTHO,
            far: float = DEFAULT_FAR,
            *,
            scissor: Rect | None = None,
            render_target: Framebuffer | None = None,
            window: Window | None = None,
    ):
        """ Constructor """

        super().__init__(
            viewport,
            position,
            up,
            zoom,
            projection,
            near,
            far,
            scissor=scissor,
            render_target=render_target,
            window=window
        )

        self._state = None
        self._offset_x = 0
        self._offset_y = 0
        self._player = None
        self._camera_speed = 1.0
        self._camera_movement = (0, 0)

    def setup(self, player: arcade.sprite.Sprite) -> None:
        """ Set up the camera """

        self._state = SettingsState().load()
        self._player = player

    @property
    def camera_movement(self) -> tuple:
        """ Get camera movement """

        return self._camera_movement

    @camera_movement.setter
    def camera_movement(self, value: tuple) -> None:
        """ Set camera movement """

        self._camera_movement = value

    def change_offset(self, delta_time: float):
        x, y = self._camera_movement

        no_movement = x == 0 and y == 0

        if no_movement:
            if self._offset_x > 0:
                x = -1
            if self._offset_x < 0:
                x = 1
            if self._offset_y > 0:
                y = -1
            if self._offset_y < 0:
                y = 1

        speed = OFFSET_SPEED * delta_time

        self._offset_x += x * speed
        self._offset_y += y * speed

        self._offset_x = min(self._offset_x, OFFSET_MAX)
        self._offset_x = max(self._offset_x, -OFFSET_MAX)

        self._offset_y = min(self._offset_y, OFFSET_MAX)
        self._offset_y = max(self._offset_y, -OFFSET_MAX)

        if not no_movement:
            return

        if x == 1 and self._offset_x > 0:
            self._offset_x = 0

        if y == 1 and self._offset_y > 0:
            self._offset_y = 0

    def on_update(self, delta_time: float) -> None:
        """ On update """

        self.change_offset(delta_time)

        x, y = self._player.position
        x += self._offset_x
        y += self._offset_y


        x = max(x, self._state.base_width / 2)
        y = max(y, self._state.base_height / 2)

        self.position = arcade.math.lerp_2d(
            self.position, (x, y), self._camera_speed
        )
