""" Logo splash screen"""
import os

import arcade
import pyglet
from arcade import View

from app.views.startscreen import StartScreen

SCENE_LAYER_LOGO = 'Logo'
SCENE_LAYER_FADE = 'Fade'

PHASE_FADE_IN = 1
PHASE_WAIT = 2
PHASE_FADE_OUT = 3
PHASE_NEXT = 4

FADE_SPEED = 2

LOGO_LENGTH = 3


class Logo(View):
    """ Logo splash screen"""

    def __init__(self):
        """ Constructor """

        super().__init__()
        self._root_dir = None
        self._scene = None
        self._fade_sprite = None
        self._phase = None

    def setup(self, root_dir: str):
        """ Setup logo screen """

        arcade.set_background_color(arcade.color.WHITE)
        self._root_dir = root_dir
        logo_file = os.path.join(self._root_dir, 'resources', 'images', 'ui', 'hog-games.png')
        logo = arcade.sprite.Sprite(path_or_texture=logo_file, x=0, y=0)

        self._scene = arcade.scene.Scene()
        self._scene.add_sprite(SCENE_LAYER_LOGO, logo)

        self._phase = None
        self._fade_sprite = arcade.sprite.SpriteSolidColor(
            width=self.window.width,
            height=self.window.height,
            color=arcade.color.BLACK
        )
        self._fade_sprite.center_x = self.window.width / 2
        self._fade_sprite.center_y = self.window.height / 2

        self._fade_sprite.alpha = 255
        self._scene.add_sprite(SCENE_LAYER_FADE, self._fade_sprite)

        self._phase = PHASE_FADE_IN

    def on_update(self, delta_time: float):
        """ On update """
        if self._phase == PHASE_NEXT:
            view = StartScreen()
            view.setup(root_dir=self._root_dir)
            self.window.show_view(view)

        if self._phase == PHASE_FADE_IN:
            self._fade_sprite.alpha = max(self._fade_sprite.alpha - FADE_SPEED, 0)

            if self._fade_sprite.alpha <= 0:
                # TODO: play sound
                self._phase = PHASE_WAIT

                pyglet.clock.schedule_interval(self.fade_to_startscreen, LOGO_LENGTH)

        if self._phase == PHASE_FADE_OUT:
            self._fade_sprite.alpha = min(self._fade_sprite.alpha + FADE_SPEED, 255)
            if self._fade_sprite.alpha >= 255:
                self._phase = PHASE_NEXT

        self._scene[SCENE_LAYER_LOGO][0].center_x = self.window.width / 2
        self._scene[SCENE_LAYER_LOGO][0].center_y = self.window.height / 2

    def on_draw(self):
        """ On draw """
        self.clear()
        self._scene.draw()

    def fade_to_startscreen(self, dt: float):
        """ Show StartScreen """
        self._phase = PHASE_FADE_OUT