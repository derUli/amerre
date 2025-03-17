""" Logo splash screen """

import os
import random

import arcade
import pyglet

from app.constants.ui import FADE_SPEED, FADE_MAX
from app.containers.effect_data import EffectData
from app.effects.filmgrain import Filmgrain
from app.views.mainmenu import MainMenu
from app.views.view import View

SCENE_LAYER_LOGO = 'Logo'
SCENE_LAYER_FADE = 'Fade'

PHASE_FADE_IN = 1
PHASE_WAIT = 2
PHASE_FADE_OUT = 3
PHASE_NEXT = 4

LOGO_LENGTH = 3


class Logo(View):
    """ Logo splash screen"""

    def __init__(self):
        """ Constructor """

        super().__init__()
        self._phase = None

    def setup(self, root_dir: str):
        """ Setup logo screen """

        super().setup(root_dir)

        self._effects = [
            Filmgrain()
        ]

        data = EffectData(
            root_dir=root_dir,
            scene=self._scene
        )

        for effect in self._effects:
            effect.setup(data)

        super().setup(root_dir)
        self.window.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.WHITE)

        logo_file = os.path.join(self._root_dir, 'resources', 'images', 'ui',
                                 'hog-games.png')
        logo = arcade.sprite.Sprite(
            path_or_texture=logo_file,
            center_x=0,
            center_y=0
        )

        self._scene.add_sprite(SCENE_LAYER_LOGO, logo)

        self._fade_sprite = arcade.sprite.SpriteSolidColor(
            width=self.window.width,
            height=self.window.height + 2,
            color=arcade.color.BLACK
        )
        self._fade_sprite.center_x = self.window.width / 2
        self._fade_sprite.center_y = self.window.height / 2

        self._fade_sprite.alpha = 255
        self._scene.add_sprite(SCENE_LAYER_FADE, self._fade_sprite)

        self._phase = PHASE_FADE_IN

        return

    def on_update(self, delta_time: float):

        if self._phase == PHASE_NEXT:
            self.window.show_view(MainMenu().setup(root_dir=self._root_dir))

        self._scene[SCENE_LAYER_LOGO][0].center_x = self.window.width / 2
        self._scene[SCENE_LAYER_LOGO][0].center_y = self.window.height / 2

        for effect in self._effects:
            effect.on_update(delta_time)

    def on_fixed_update(self, delta_time: float):
        """ On update """

        if self._phase == PHASE_FADE_IN:
            self._fade_sprite.alpha = max(self._fade_sprite.alpha - FADE_SPEED,
                                          0)

            if self._fade_sprite.alpha <= 0:
                sound_number = random.randint(1, 5)
                file = os.path.join(
                    self._root_dir,
                    'resources',
                    'sounds',
                    'grunt',
                    f'{sound_number:03d}.mp3'
                )
                sound = arcade.load_sound(file, streaming=True)
                sound.play(
                    volume=self.window.audio_volumes.volume_sound_normalized)

                self._phase = PHASE_WAIT

                pyglet.clock.schedule_interval(self.fade_to_main_menu,
                                               LOGO_LENGTH)

        if self._phase == PHASE_FADE_OUT:
            self._fade_sprite.alpha = min(
                self._fade_sprite.alpha + FADE_SPEED,
                FADE_MAX
            )
            if self._fade_sprite.alpha >= FADE_MAX:
                self._phase = PHASE_NEXT

    def on_draw(self):
        """ On draw """

        self.clear()
        self._scene.draw()

        for effect in self._effects:
            effect.draw()

        self.window.draw_after()

    def fade_to_main_menu(self, dt: float):
        """ Show StartScreen """
        self._phase = PHASE_FADE_OUT
