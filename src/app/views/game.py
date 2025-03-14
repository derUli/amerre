""" Main game class """

from arcade import FACE_LEFT, FACE_RIGHT

from app.constants.input.controllers import (
    KEY_A,
    LEFTSTICK,
    AXIS_RIGHT,
    AXIS_LEFT,
    LEFT_TRIGGER,
    KEY_START
)
from app.constants.input.keyboard import KEY_LEFT, KEY_RIGHT, KEY_JUMP, KEY_SPRINT, KEY_ESCAPE, KEY_SKIP_LEVEL
from app.state.settingsstate import SettingsState
from app.utils.dev import is_frozen
from app.utils.level import Level
from app.views.view import View


class Game(View):
    """ Main game class """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._level = None
        self._move_horizontal = None
        self._jump = False
        self._sprint = False

    def setup(self, root_dir: str):
        """ Setup game"""

        self.window.set_mouse_visible(False)
        super().setup(root_dir)

        self._level = Level()
        self.window.set_mouse_visible(False)

    def setup_level(self, map_name: str):
        """ Setup level """

        self._level.setup(self._root_dir, map_name, self.window.audio_volumes)

    def on_update(self, delta_time: float):
        self._level.update(
            delta_time=delta_time
        )

    def on_fixed_update(self, delta_time: float):
        """ On level update """
        self._level.fixed_update(
            delta_time=delta_time,
            window=self.window,
            move_horizontal=self._move_horizontal,
            jump=self._jump,
            sprint=self._sprint
        )

        if self._jump:
            self._jump = False

    def on_draw(self):
        """ On draw """

        self.clear()
        self._level.draw()
        self.window.draw_after()

    def on_key_press(self, symbol: int, modifiers: int):
        """ On key press """

        if symbol in KEY_ESCAPE:
            self.on_pause()

        if symbol in KEY_LEFT:
            self._move_horizontal = FACE_LEFT

        if symbol in KEY_RIGHT:
            self._move_horizontal = FACE_RIGHT

        if symbol in KEY_JUMP:
            self._jump = True

        if symbol in KEY_SPRINT:
            self._sprint = True

        if symbol in KEY_SKIP_LEVEL and not is_frozen():
            self._level.on_level_completed()

    def on_key_release(self, _symbol: int, _modifiers: int):
        """ On key release"""

        if self._move_horizontal == FACE_LEFT and _symbol in KEY_LEFT:
            self._move_horizontal = None
        if self._move_horizontal == FACE_RIGHT and _symbol in KEY_RIGHT:
            self._move_horizontal = None

        if self._sprint and _symbol in KEY_SPRINT:
            self._sprint = False

    def on_stick_motion(self, joystick, stick, value):
        """ On stick motion """

        if stick == LEFTSTICK:
            x, y = value
            x, y = round(x), round(y)

            if x == AXIS_RIGHT:
                self._move_horizontal = FACE_RIGHT
            elif x == AXIS_LEFT:
                self._move_horizontal = FACE_LEFT
            else:
                self._move_horizontal = None

    def on_trigger_motion(self, joystick, trigger: str, value: float):
        """ On trigger motion """

        if trigger == LEFT_TRIGGER:
            self._sprint = round(value) >= 1.0

    def on_button_press(self, joystick, key) -> None:
        """ On controller button press """

        if key == KEY_A:
            self._jump = True

        if key == KEY_START:
            self.on_pause()

        if key == LEFTSTICK:
            self._sprint = True

    def on_button_release(self, joystick, key):
        """ On controller button release """

        if key == KEY_LEFT:
            self._sprint = False

    def on_pause(self) -> None:
        """ On pause game """

        from app.views.pausemenu import PauseMenu
        menu = PauseMenu(previous_view=self)
        menu.setup(root_dir=self._root_dir)
        self.window.show_view(menu)
        self._level.on_pause()

    def on_continue(self) -> None:
        """ On continue """

        state = SettingsState.load()
        self.window.audio_volumes = state.audio_volumes
        self._level.on_continue()

    def unsetup(self) -> None:
        """ Unsetup game """

        self._level.unsetup()
