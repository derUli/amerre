""" The main menu """

import logging
import os
import random
import webbrowser

import arcade

from app.constants.fonts import FONT_MARKER_FELT, FONT_CONSOLA_MONO
from app.constants.gameinfo import VERSION_STRING, MAPS
from app.constants.input.controllers import KEY_START, KEY_BACK
from app.constants.input.keyboard import KEY_ESCAPE, KEY_CONFIRM
from app.constants.input.mouse import BUTTON_LEFT_CLICK
from app.effects.filmgrain import Filmgrain
from app.views.game import Game
from app.views.view import View

BACKGROUND_COLOR = (58, 158, 236, 255)
FONT_SIZE = 20
FONT_SIZE_TITLE = 80
FONT_SIZE_VERSION = 12

FADE_SPEED = 4
FADE_MAX = 255
MUSIC_FADE_SPEED = 0.005
MARGIN = 10

SCENE_LAYER_FADEIN = 'fadein'
SCENE_LAYER_ICON = 'icon'
SCENE_LAYER_PARTICLES = 'particles'
SCENE_LAYER_TEXT = 'Text'

PARTICLE_SPEED = 2

PARTICLE_COLORS = [
    (228, 255, 4, 200),
    (210, 210, 210, 200),
    (111, 186, 241, 200)
]
PARTICLES_SIZE_RANGE = 8
PARTICLES_COUNT = 500

URL_ITCH_IO = 'https://hog-games.itch.io/'


class MainMenu(View):
    """ The main menu """

    def __init__(self) -> None:
        """ Constructor """

        super().__init__()

        self._text_start = None
        self._text_title = None
        self._text_version = None

        self._scene = None
        self._icon_itch_io = None
        self._icon_exit = None
        self._last_hover = None

        self._sound_hover = None

        self._effects = []

    def setup(self, root_dir: str):
        """ Setup the start screen """

        super().setup(root_dir)

        # Background color
        arcade.set_background_color(BACKGROUND_COLOR)
        self.window.set_mouse_visible(not any(self.window.controllers))

        # Text
        self.setup_particles()
        self.setup_text()
        self.setup_icons(root_dir)

        # Play music
        self.setup_music(root_dir)
        self.setup_sounds(root_dir)

        self.on_update(0)

        self._effects = [
            Filmgrain()
        ]

        for effect in self._effects:
            effect.setup(self._scene, None, root_dir)

        return self

    def setup_text(self):
        """ Setup text """

        text = _('Press SPACE key to start')

        if any(self.window.controllers):
            text = _('Press START button to start')

        self._text_start = arcade.create_text_sprite(
            text=text,
            font_name=FONT_MARKER_FELT,
            font_size=FONT_SIZE,
            bold=True
        )
        self._scene.add_sprite(SCENE_LAYER_TEXT, self._text_start)

        self._text_title = arcade.create_text_sprite(
            text=self.window.caption,
            font_name=FONT_MARKER_FELT,
            font_size=FONT_SIZE_TITLE,
            bold=True
        )
        self._scene.add_sprite(SCENE_LAYER_TEXT, self._text_title)

        self._text_version = arcade.create_text_sprite(
            text=" ".join([_('Version'), VERSION_STRING]),
            font_name=FONT_CONSOLA_MONO,
            font_size=FONT_SIZE_VERSION,
            bold=True
        )
        self._scene.add_sprite(SCENE_LAYER_TEXT, self._text_version)

    def setup_icons(self, root_dir: str):
        """ Setup menu icons """

        self._icon_itch_io = arcade.sprite.Sprite(
            path_or_texture=os.path.join(root_dir, 'resources', 'images', 'ui', 'itch-io.jpg'),
            x=0,
            y=0
        )
        self._scene.add_sprite(SCENE_LAYER_ICON, self._icon_itch_io)

        self._icon_exit = arcade.sprite.Sprite(
            path_or_texture=os.path.join(root_dir, 'resources', 'images', 'ui', 'exit.jpg'),
            x=0,
            y=0
        )
        self._scene.add_sprite(SCENE_LAYER_ICON, self._icon_exit)

    def setup_music(self, root_dir: str):
        """ Play music """

        music = arcade.load_sound(
            os.path.join(root_dir, 'resources', 'music', 'DeepSpace.mp3'),
            streaming=True
        )
        self._music = music.play(loop=True, volume=self.window.audio_volumes.volume_music)

    def setup_sounds(self, root_dir: str):
        """ Setup sounds """

        self._sound_hover = arcade.load_sound(
            os.path.join(root_dir, 'resources', 'sounds', 'common', 'hover.mp3'),
        )

    def setup_particles(self):
        """ Setup article animation """

        try:
            self._scene[SCENE_LAYER_PARTICLES].clear()
        except KeyError:
            pass

        for i in range(0, PARTICLES_COUNT):
            sprite = arcade.sprite.SpriteCircle(
                color=random.choice(PARTICLE_COLORS),
                soft=True,
                radius=random.randint(1, PARTICLES_SIZE_RANGE)
            )
            sprite.center_x = random.randint(0, self.window.width)
            sprite.center_y = random.randint(0, self.window.height)
            self._scene.add_sprite(SCENE_LAYER_PARTICLES, sprite)

    def on_update(self, delta_time: float):
        """ On update """

        self.on_update_particles()
        self._text_start.center_x = self.window.width / 2
        self._text_start.bottom = MARGIN

        self._text_title.center_x = self.window.width / 2
        self._text_title.center_y = self.window.height / 2

        self._text_version.left = MARGIN
        self._text_version.bottom = MARGIN

        self._icon_itch_io.right = self.window.width - MARGIN
        self._icon_itch_io.bottom = MARGIN

        self._icon_exit.right = self.window.width - MARGIN
        self._icon_exit.top = self.window.height - MARGIN

        for effect in self._effects:
            effect.update(delta_time)

        # On fading in
        if self._fade_sprite is not None:

            self._fade_sprite.alpha = min(self._fade_sprite.alpha + FADE_SPEED, 255)

            if self._music:
                self._music.volume = max(self._music.volume - MUSIC_FADE_SPEED, 0)
                if self._music.volume <= 0:
                    self._music.pause()
                    self._music = None

                    view = Game()
                    view.setup(self._root_dir)
                    view.setup_level(MAPS[0])

                    self.window.show_view(view)

    def on_update_particles(self):
        """ Update particles """

        particles = self._scene[SCENE_LAYER_PARTICLES]
        for particle in particles:
            particle.center_x -= PARTICLE_SPEED

            if particle.right < 0:
                particle.center_x = self.window.width + particle.width
                particle.center_y = random.randint(0, self.window.height)

    def on_draw(self):
        """ On draw"""

        # Clear screen
        self.clear()

        # Draw scene
        self._scene.draw()

        if SCENE_LAYER_FADEIN in self._scene:
            self._scene[SCENE_LAYER_FADEIN].draw()

        for effect in self._effects:
            effect.draw()

        self.window.draw_after()

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle keyboard input """

        if symbol in KEY_ESCAPE:
            self.on_exit()

        if symbol in KEY_CONFIRM and self._fade_sprite is None:
            self.on_start_game()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        """ Handle mouse movement """

        if self._fade_sprite:
            return

        self.window.set_mouse_visible(True)

        if self._last_hover:
            if not self._last_hover.collides_with_point((x, y)):
                self._last_hover.scale = 1.0
                self._last_hover = None
            return

        sprites = [
            self._icon_itch_io,
            self._text_title,
            self._icon_exit
        ]

        for sprite in sprites:
            if sprite.collides_with_point((x, y)):

                self._sound_hover.play(volume=self.window.audio_volumes.volume_sound)

                self._last_hover = sprite
                self._last_hover.scale = 1.02
                break

    def on_mouse_press(self, x, y, button, modifiers) -> bool | None:
        """ Handle mouse press """

        if button not in BUTTON_LEFT_CLICK:
            return

        if self._last_hover == self._text_title:
            self.on_start_game()

        if self._last_hover == self._icon_itch_io:
            self.on_itch_io()

        if self._last_hover == self._icon_exit:
            self.on_exit()

    def on_button_press(self, joystick, key) -> None:
        """ On controller button press """

        if key == KEY_START:
            self.on_start_game()
        elif key == KEY_BACK:
            self.on_exit()

    def on_start_game(self) -> None:
        """ On start new game """

        self.window.set_mouse_visible(False)

        self._fade_sprite = arcade.sprite.SpriteSolidColor(
            width=self.window.width,
            height=self.window.height,
            color=BACKGROUND_COLOR
        )
        self._fade_sprite.center_x = self.window.width / 2
        self._fade_sprite.center_y = self.window.height / 2

        self._fade_sprite.alpha = 0
        self._scene.add_sprite(SCENE_LAYER_FADEIN, self._fade_sprite)

    @staticmethod
    def on_itch_io() -> None:
        """ On open itch.io """

        webbrowser.open_new_tab(URL_ITCH_IO)

    @staticmethod
    def on_exit() -> None:
        """ On exit game """

        arcade.exit()
