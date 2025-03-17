""" To be continued screen """

import arcade

from app.constants.fonts import FONT_DEFAULT
from app.constants.input.controllers import KEY_START
from app.constants.input.keyboard import KEY_CONFIRM
from app.containers.effect_data import EffectData
from app.effects.filmgrain import Filmgrain
from app.views.view import View

FONT_SIZE = 60
FADE_SPEED = 4
FADE_MAX = 255
SCENE_LAYER_TEXT = 'Text'
SCENE_LAYER_FADE = 'Fade'
BACKGROUND_COLOR = (58, 158, 236, 255)


class ToBeContinued(View):
    """ To be continued screen """

    def __init__(self):
        """ To be continued screen """

        super().__init__()

        self._text_completed = None
        self._fade_sprite = None
        self.window = None
        self._fade_sprite = None
        self.background_color = arcade.csscolor.WHITE

        self._effects = []

    def setup(self, root_dir: str):
        """ Setup logo screen """

        self.window = arcade.get_window()

        super().setup(root_dir)
        self.window.set_mouse_visible(False)

        self._text_completed = arcade.create_text_sprite(
            text=_('To be continued'),
            font_name=FONT_DEFAULT,
            font_size=FONT_SIZE,
            color=arcade.csscolor.BLACK,
            bold=True,
        )

        self._scene.add_sprite(SCENE_LAYER_TEXT, self._text_completed)
        self._scene[SCENE_LAYER_TEXT].visible = False

        self._effects = [
            Filmgrain()
        ]

        data = EffectData(root_dir=root_dir)
        for effect in self._effects:
            effect.setup(data=data)

        return self

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle keyboard input """

        if symbol in KEY_CONFIRM:
            self.on_main_menu()

    def on_update(self, delta_time: float):
        w, h = self.window.get_size()
        self._text_completed.center_x = w / 2
        self._text_completed.center_y = h / 2
        self._scene[SCENE_LAYER_TEXT].visible = True

        for effect in self._effects:
            effect.update(delta_time)

        if SCENE_LAYER_FADE in self._scene:
            self._fade_sprite.visible = True
            self._fade_sprite.center_x = w / 2
            self._fade_sprite.center_y = h / 2

            if self._fade_sprite.alpha >= FADE_MAX:
                from app.views.mainmenu import MainMenu
                self.window.show_view(MainMenu().setup(self._root_dir))

            self._fade_sprite.alpha = min(self._fade_sprite.alpha + FADE_SPEED,
                                          FADE_MAX)

    def on_draw(self):
        """ On draw """

        self.clear()
        self._scene.draw()

        for effect in self._effects:
            effect.draw()

    def on_button_press(self, joystick, key) -> None:
        """ On controller button press """

        if key == KEY_START:
            self.on_main_menu()

    def on_main_menu(self) -> None:
        """ On go to main menu """

        if self._fade_sprite:
            return

        self._fade_sprite = arcade.sprite.SpriteSolidColor(
            width=self.window.width,
            height=self.window.height,
            color=BACKGROUND_COLOR
        )
        self._fade_sprite.visible = False
        self._fade_sprite.alpha = 0

        self._scene.add_sprite(SCENE_LAYER_FADE, self._fade_sprite)
