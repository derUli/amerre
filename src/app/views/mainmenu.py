""" The main menu """

import os
import webbrowser

import arcade
import arcade.gui

from app.constants.fonts import FONT_DEFAULT
from app.constants.gameinfo import VERSION_STRING, MAPS_FIRST
from app.constants.input.controllers import KEY_START, KEY_BACK
from app.constants.input.keyboard import KEY_ESCAPE, KEY_CONFIRM
from app.constants.input.mouse import BUTTON_LEFT_CLICK
from app.constants.ui import MARGIN, FADE_SPEED, FADE_MAX
from app.containers.effect_data import EffectData
from app.effects.filmgrain import Filmgrain
from app.effects.menu_particles import MenuParticles
from app.state.savegamestate import SavegameState
from app.state.settingsstate import SettingsState
from app.views.game import Game
from app.views.tobecontinued import ToBeContinued
from app.views.ui.settings.settings import Settings
from app.views.view import View

BACKGROUND_COLOR = (58, 158, 236, 255)
FONT_SIZE = 15
FONT_SIZE_TITLE = 50

MUSIC_FADE_SPEED = 0.005

SCENE_LAYER_FADEIN = 'fadein'
SCENE_LAYER_ICON = 'icon'
SCENE_LAYER_TEXT = 'Text'

URL_ITCH_IO = 'https://hog-games.itch.io/'


class MainMenu(View):
    """ The main menu """

    def __init__(self) -> None:
        """ Constructor """

        super().__init__()

        self._text_start = None
        self._text_title = None
        self._text_version = None
        self._text_load = None

        self._scene2 = None
        self._manager = None
        self._icon_itch_io = None
        self._icon_settings = None
        self._icon_exit = None
        self._last_hover = None

        self._sound_hover = None
        self._effects = []

    def setup(self, root_dir: str):
        """ Setup the start screen """

        super().setup(root_dir)

        self._scene2 = arcade.scene.Scene()

        # Background color
        arcade.set_background_color(BACKGROUND_COLOR)
        self.window.set_mouse_visible(not any(self.window.controllers))

        # Play music
        self.setup_music(root_dir)
        self.setup_sounds(root_dir)

        self._effects = [
            MenuParticles(),
            Filmgrain()
        ]

        data = EffectData(
            root_dir=root_dir,
            scene=self._scene
        )

        for effect in self._effects:
            effect.setup(data)

        # Text
        self.setup_text()
        self.setup_icons(root_dir)

        self.on_update(0)
        return self

    def setup_text(self):
        """ Setup text """
        if SCENE_LAYER_TEXT in self._scene:
            self._scene[SCENE_LAYER_TEXT].clear()

        text = _('Press SPACE key to start')

        if any(self.window.controllers):
            text = _('Press START button to start')

        self._text_start = arcade.create_text_sprite(
            text=text,
            font_name=FONT_DEFAULT,
            font_size=FONT_SIZE,
            bold=True
        )
        self._scene.add_sprite(SCENE_LAYER_TEXT, self._text_start)

        self._text_title = arcade.create_text_sprite(
            text=self.window.caption,
            font_name=FONT_DEFAULT,
            font_size=FONT_SIZE_TITLE,
            bold=True
        )
        self._scene.add_sprite(SCENE_LAYER_TEXT, self._text_title)

        color = arcade.csscolor.BLACK

        if SavegameState.load().current_level == MAPS_FIRST:
            color = arcade.csscolor.WHITE

        self._text_load = arcade.create_text_sprite(
            text=_('Loading...'),
            font_name=FONT_DEFAULT,
            font_size=FONT_SIZE,
            color=color
        )

        self._text_load.visible = False
        self._scene2.add_sprite(SCENE_LAYER_TEXT, self._text_load)

        self._text_version = arcade.create_text_sprite(
            text=" ".join([_('Version'), VERSION_STRING]),
            font_name=FONT_DEFAULT,
            font_size=FONT_SIZE,
            bold=True
        )
        self._scene.add_sprite(SCENE_LAYER_TEXT, self._text_version)

    def setup_icons(self, root_dir: str):
        """ Setup menu icons """

        self._icon_itch_io = arcade.sprite.Sprite(
            path_or_texture=os.path.join(root_dir, 'resources', 'images', 'ui',
                                         'itch-io.jpg'),
            x=0,
            y=0
        )
        self._scene.add_sprite(SCENE_LAYER_ICON, self._icon_itch_io)

        self._icon_exit = arcade.sprite.Sprite(
            path_or_texture=os.path.join(root_dir, 'resources', 'images', 'ui',
                                         'exit.jpg'),
            x=0,
            y=0
        )
        self._scene.add_sprite(SCENE_LAYER_ICON, self._icon_exit)

        self._icon_settings = arcade.sprite.Sprite(
            path_or_texture=os.path.join(root_dir, 'resources', 'images', 'ui',
                                         'settings.png'),
            x=0,
            y=0
        )
        self._scene.add_sprite(SCENE_LAYER_ICON, self._icon_settings)

    def setup_music(self, root_dir: str):
        """ Play music """

        music = arcade.load_sound(
            os.path.join(root_dir, 'resources', 'music', 'DeepSpace.mp3'),
            streaming=True
        )
        self._music = music.play(
            loop=True,
            volume=self.window.audio_volumes.volume_music_normalized
        )

    def setup_sounds(self, root_dir: str):
        """ Setup sounds """

        self._sound_hover = arcade.load_sound(
            os.path.join(root_dir, 'resources', 'sounds', 'common',
                         'hover.mp3'),
        )

    def on_update(self, delta_time: float):
        """ On update """

        self._text_start.center_x = self.window.width / 2
        self._text_start.bottom = MARGIN

        self._text_title.center_x = self.window.width / 2
        self._text_title.center_y = self.window.height / 2

        self._text_version.left = MARGIN
        self._text_version.bottom = MARGIN

        self._text_load.right = self.window.width - MARGIN
        self._text_load.bottom = MARGIN

        self._icon_itch_io.right = self.window.width - MARGIN
        self._icon_itch_io.bottom = MARGIN

        self._icon_exit.right = self.window.width - MARGIN
        self._icon_exit.top = self.window.height - MARGIN

        self._icon_settings.left = MARGIN
        self._icon_settings.top = self.window.height - MARGIN

        if self._manager:
            self._manager.on_update(time_delta=delta_time)

        for effect in self._effects:
            effect.on_update(delta_time)

        if not self._fade_sprite:
            return

        if self._fade_sprite.alpha < 255:
            return

        if self._music.volume > 0:
            return

        self._music.pause()

        save_game_state = SavegameState.load()

        if not SavegameState.exists():
            save_game_state.save()

        if save_game_state.current_level is None:
            view = ToBeContinued()
            view.setup(self._root_dir)
            self.window.show_view(view)
            return

        view = Game()
        view.setup(self._root_dir)

        view.setup_level(save_game_state.current_level)

        self.window.show_view(view)

    def on_fixed_update(self, delta_time: float):

        if not self._fade_sprite:
            return

        # On fading in
        self._fade_sprite.alpha = min(
            self._fade_sprite.alpha + FADE_SPEED,
            FADE_MAX
        )

        self._text_load.visible = self._fade_sprite.alpha >= FADE_MAX
        self._music.volume = max(self._music.volume - MUSIC_FADE_SPEED, 0)

    def on_draw(self):
        """ On draw"""

        # Clear screen
        self.clear()

        # Draw scene

        self._scene.draw()

        if SCENE_LAYER_FADEIN in self._scene:
            self._scene[SCENE_LAYER_FADEIN].draw()
            if self._fade_sprite.alpha >= 255:
                self._scene2.draw()

        for effect in self._effects:
            effect.draw()

        if self._manager:
            self._manager.draw()

        self.window.draw_after()

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle keyboard input """

        if symbol in KEY_ESCAPE:
            if self._manager:
                return

            self.on_exit()

        if symbol in KEY_CONFIRM and self._fade_sprite is None:
            self.on_start_game()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        """ Handle mouse movement """

        self.window.set_mouse_visible(True)

        if self._manager:
            return

        if self._last_hover:
            if not self._last_hover.collides_with_point((x, y)):
                self._last_hover.scale = 1.0
                self._last_hover = None
            return

        sprites = [
            self._icon_itch_io,
            self._text_title,
            self._icon_exit,
            self._icon_settings
        ]

        for sprite in sprites:
            if sprite.collides_with_point((x, y)):
                self._sound_hover.play(
                    volume=self.window.audio_volumes.volume_sound_normalized
                )
                self._last_hover = sprite
                self._last_hover.scale = 1.03
                break

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        """ Handle mouse press """

        if button not in BUTTON_LEFT_CLICK:
            return

        if self._last_hover == self._text_title:
            self.on_start_game()

        if self._last_hover == self._icon_itch_io:
            self.on_itch_io()

        if self._last_hover == self._icon_settings:
            self.on_settings()

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

        self.setup_text()
        color = arcade.csscolor.WHITE

        if SavegameState.load().current_level == MAPS_FIRST:
            color = BACKGROUND_COLOR

        self.window.set_mouse_visible(False)

        self._fade_sprite = arcade.sprite.SpriteSolidColor(
            width=self.window.width,
            height=self.window.height,
            color=color
        )
        self._fade_sprite.center_x = self.window.width / 2
        self._fade_sprite.center_y = self.window.height / 2

        self._fade_sprite.alpha = 0
        self._scene.add_sprite(SCENE_LAYER_FADEIN, self._fade_sprite)

    @staticmethod
    def on_itch_io() -> None:
        """ On open itch.io """

        webbrowser.open_new_tab(URL_ITCH_IO)

    def on_settings(self):
        """ On settings """

        self._scene[SCENE_LAYER_TEXT].visible = False
        self._scene[SCENE_LAYER_ICON].visible = False
        self._manager = Settings()
        self._manager.from_main_menu = True
        self._manager.setup(on_close=self.on_close_settings,
                            on_change=self.on_change_settings)
        self._manager.enable()

    def on_change_settings(
            self,
            state: SettingsState = None,
            refresh_particles: bool = False
    ) -> None:
        """ On change settings """
        if state:
            self._music.volume = state.audio_volumes.volume_music_normalized
            self.window.audio_volumes = state.audio_volumes

        if refresh_particles:
            for effect in self._effects:
                effect.refresh()

    def on_close_settings(self, new_manager=None) -> None:
        """ On close settings"""
        self._manager.disable()
        self._manager = None
        if new_manager:
            self._manager = new_manager
            return

        self._scene[SCENE_LAYER_TEXT].visible = True
        self._scene[SCENE_LAYER_ICON].visible = True

    @staticmethod
    def on_exit() -> None:
        """ On exit game """

        arcade.exit()
