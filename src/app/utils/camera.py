from arcade import Rect, Window
from arcade.camera import Camera2D
from arcade.camera.data_types import DEFAULT_NEAR_ORTHO, DEFAULT_FAR
from arcade.gl import Framebuffer
from arcade.types import Point2

# Max offset
MAX_OFFSET_X = 100
MAX_OFFSET_Y = 100
OFFSET_SPEED = 1

class Camera(Camera2D):
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

        self._offset_x = 0
        self._offset_y = 0

    def offset_move_right(self):
        self._offset_x = min(MAX_OFFSET_X, self._offset_x)