""" Level """

import json
import logging
import os
import time

import arcade
import pyglet
from arcade import FACE_RIGHT, FACE_LEFT

from app.constants.gameinfo import BASE_HEIGHT, BASE_WIDTH, DEFAULT_ENCODING
from app.constants.layers import (
    LAYER_WALL,
    LAYER_FADEOUT, LAYER_PLAYER
)
from app.constants.player import (
    PLAYER_MOVE_SPEED,
    MODIFIER_SPEECH,
    MODIFIER_SPRINT,
    MODIFIER_WALK,
    PLAYER_JUMP_SPEED,
    PLAYER_MOVE_ANGLE
)
from app.containers.callbacks import Callbacks
from app.effects.effect_manager import EffectManager
from app.entities.player import Player
from app.state.settingsstate import SettingsState
from app.utils.audiovolumes import AudioVolumes
from app.utils.voiceovertriggers import VoiceOverTiggers
from app.views.tobecontinued import ToBeContinued

GRAVITY_SLOWMO = 0.0005
GRAVITY_DEFAULT = 0.8

ALPHA_SPEED = 2
ALPHA_MAX = 255

LIGHT_LAUNCHING_RUMBLE = 100

VOLUME_MUSIC_MODIFIER = 0.3
VOLUME_ATMO_MODIFIER = 0.1

WHITE = arcade.csscolor.WHITE


class Level:
    """ Level """

    def __init__(self):
        """ Constructor"""

        self._scene = None
        self._tilemap = None
        self._camera = None
        self._camera_gui = None
        self._physics_engine = None
        self._can_walk = False
        self._voiceover_triggers = None
        self._music = None
        self._atmo = None
        self._root_dir = None
        self._effect_manager = None
        self._rumble = 0
        self._player = None

    def setup(self, root_dir: str, map_name: str, audio_volumes: AudioVolumes):
        """ Setup level """

        self._root_dir = root_dir

        self.load_tilemap(
            os.path.join(root_dir, 'resources', 'maps', f"{map_name}.tmx"))
        config = self.load_config()

        h = arcade.get_window().height

        zoom = h / BASE_HEIGHT
        self._camera = arcade.camera.Camera2D(zoom=zoom)

        self._camera_gui = arcade.camera.Camera2D()

        self.setup_physics_engine()
        self.wait_for_begin()

        map_config = {}

        if map_name in config:
            map_config = config[map_name]

        if 'music' in map_config:
            music_file = os.path.join(root_dir, 'resources', 'music',
                                      map_config['music'])
            music = arcade.load_sound(music_file, streaming=True)
            loop = 'musicLoop' in map_config and map_config['musicLoop']
            self._music = music.play(
                volume=audio_volumes.volume_music_normalized *
                       VOLUME_MUSIC_MODIFIER,
                loop=loop
            )

        atmo_file = os.path.join(
            root_dir,
            'resources',
            'sounds',
            'atmos',
            f"{map_name}.mp3"
        )

        if os.path.exists(atmo_file):
            atmo = arcade.load_sound(atmo_file, streaming=True)
            self._atmo = atmo.play(
                volume=audio_volumes.volume_sound_normalized * VOLUME_ATMO_MODIFIER,
                loop=True)

        callbacks = Callbacks(on_level_completed=self.on_level_completed)
        self._voiceover_triggers = VoiceOverTiggers().setup(
            voiceover_range=map_config['voiceovers'],
            callbacks=callbacks,
            tilemap=self._tilemap
        )
        self.scroll_to_player()

        self._effect_manager = EffectManager()
        self._effect_manager.setup(
            map_config,
            self._scene,
            self._tilemap,
            root_dir
        )

    def setup_physics_engine(self):
        """ Setup physics engine """

        self._physics_engine = arcade.PhysicsEnginePlatformer(
            self._player.sprite,
            ladders=None,
            walls=self._scene[LAYER_WALL],
            gravity_constant=GRAVITY_SLOWMO
        )

    def load_tilemap(self, path):
        """ Load tilemap """

        time_start = time.time()

        self._tilemap = arcade.load_tilemap(path)
        self._scene = arcade.Scene.from_tilemap(self._tilemap)
        self._player = Player()
        self._player.setup(self._scene[LAYER_PLAYER][0], self._root_dir)

        time_end = time.time() - time_start
        logging.info(f"Scene loaded in f{time_end} seconds")
        self._player.sprite.alpha = 0

    def on_update(self, delta_time: float) -> None:
        """ On update"""

        self._voiceover_triggers.update_collision_light(delta_time)
        self._effect_manager.vhs.enabled = self._voiceover_triggers.media is not None
        self._effect_manager.on_update(delta_time)

        if (
                self._voiceover_triggers.missile_sound
                and not self._voiceover_triggers.missile_sound.playing
        ):
            self._rumble = 0

        self._scene.update(delta_time)
        self._scene.update_animation(delta_time)
        self.scroll_to_player()

        # Respawn on level start if the player falls through the map
        self._player.on_update()

    def on_fixed_update(
            self,
            delta_time: float,
            window,
            move_horizontal: int = None,
            jump: bool = False,
            sprint: bool = False
    ) -> None:
        """ On fixed update """

        if jump:
            self.jump()
        if move_horizontal == FACE_RIGHT:
            self.move_right(delta_time, sprint)
        elif move_horizontal == FACE_LEFT:
            self.move_left(delta_time, sprint)
        else:
            self.move_stop()

        self._player.sprite.alpha = min(self._player.sprite.alpha + ALPHA_SPEED, 255)

        self.check_collision_lights(window.root_dir, window.audio_volumes)
        self.update_fade()
        self._effect_manager.on_fixed_update(delta_time)

        self._voiceover_triggers.on_update()

        self._physics_engine.update()

        if self._music and not self._music.playing:
            self._music.delete()

    def scroll_to_player(self, camera_speed: float = 1.0) -> None:
        """ Scroll the window to the player. """

        self._camera.position = arcade.math.lerp_2d(
            self._camera.position, self._player.position, camera_speed
        )

    def draw(self) -> None:
        """ Draw level """

        self._camera.use()
        self._scene.draw()

        self._effect_manager.draw()

        self._camera_gui.use()
        self._voiceover_triggers.draw_subtitle()

    def move_left(self, delta_time: float, sprint: bool = False) -> None:
        """ Move left """

        if not self._can_walk:
            return

        modifier = MODIFIER_WALK

        if sprint:
            modifier = MODIFIER_SPRINT

        if self._voiceover_triggers.playing:
            modifier = MODIFIER_SPEECH

        self._player.sprite.change_x = -PLAYER_MOVE_SPEED * modifier * delta_time
        self._player.sprite.angle -= PLAYER_MOVE_ANGLE * modifier * delta_time

        if self._player.sprite.angle <= 0:
            self._player.sprite.angle = 360 - abs(self._player.sprite.angle)

    def move_right(self, delta_time: float, sprint: bool = False):
        """ Move right """

        if not self._can_walk:
            return

        modifier = MODIFIER_WALK

        if sprint:
            modifier = MODIFIER_SPRINT

        if self._voiceover_triggers.playing:
            modifier = MODIFIER_SPEECH

        self._player.sprite.change_x = PLAYER_MOVE_SPEED * modifier * delta_time
        self._player.sprite.angle += PLAYER_MOVE_ANGLE * modifier * delta_time

        if self._player.sprite.angle > 360:
            self._player.sprite.angle = self._player.sprite.angle - 360

    def move_stop(self):
        """ Stop walking """

        if not self._can_walk:
            return

        self._player.sprite.change_x = 0

    def jump(self):
        """ Do jump """

        if not self._can_walk:
            return

        if not self._physics_engine.can_jump():
            return

        speed = PLAYER_JUMP_SPEED

        self._player.jump_sound()

        if self._voiceover_triggers.playing:
            speed *= MODIFIER_SPEECH

        self._physics_engine.jump(speed)

    def wait_for_begin(self, delta_time: float = 0.0):
        """ Wait for begin of level """

        if self._physics_engine.can_jump():
            self._can_walk = True
            self._physics_engine.gravity_constant = GRAVITY_DEFAULT
            return

        pyglet.clock.schedule_once(self.wait_for_begin, 1 / 4)

    def check_collision_lights(self, root_dir: str, volumes: AudioVolumes):
        """ Check for collisions with lights """

        found = self._voiceover_triggers.check_for_collision(
            self._player.sprite,
            self._scene,
            root_dir,
            volumes,
            self._music,
        )

        if not found:
            return

        self._rumble = LIGHT_LAUNCHING_RUMBLE

    def unsetup(self):
        """ On exit stop and delete sounds """

        sounds = [
            self._music,
            self._atmo,
            self._voiceover_triggers.media,
        ]

        for sound in sounds:
            if sound:
                arcade.stop_sound(sound)

    def on_pause(self):
        """ On pause game """

        sounds = [
            self._music,
            self._atmo,
            self._voiceover_triggers.media,
        ]

        # Pause audio
        for sound in sounds:
            if sound:
                sound.pause()

    def on_continue(self):
        """ On continue """

        sounds = [
            self._music,
            self._atmo,
            self._voiceover_triggers.media,
        ]

        state = SettingsState.load()

        if self._music:
            self._music.volume = state.audio_volumes.volume_music_normalized * VOLUME_MUSIC_MODIFIER

        if self._atmo:
            self._atmo.volume = state.audio_volumes.volume_sound_normalized * VOLUME_ATMO_MODIFIER

        if self._voiceover_triggers.media:
            self._voiceover_triggers.media.volume = state.audio_volumes.volume_speech_normalized

        # Start sound playback
        for sound in sounds:
            if sound:
                sound.play()

        self._effect_manager.refresh()
        self._player.refresh()

    def on_level_completed(self) -> None:
        """ Called when a level is completed """

        w, h = BASE_WIDTH, BASE_HEIGHT

        # Add fade sprite to scene
        sprite = arcade.sprite.SpriteSolidColor(width=w, height=h, color=WHITE)

        # It is initially hidden
        # On next update it will change to visible
        sprite.alpha = 0
        sprite.visible = False

        self._scene.add_sprite(LAYER_FADEOUT, sprite)
        self.update_fade()

    def update_fade(self) -> None:
        """ Update fade """

        if LAYER_FADEOUT not in self._scene:
            return

        if not any(self._scene[LAYER_FADEOUT]):
            return

        sprite = self._scene[LAYER_FADEOUT][0]

        camera_x, camera_y = self._camera.position

        sprite.center_x = camera_x
        sprite.center_y = camera_y
        sprite.visible = True

        if sprite.alpha < ALPHA_MAX:
            sprite.alpha = min(sprite.alpha + ALPHA_SPEED, ALPHA_MAX)

            if sprite.alpha >= ALPHA_MAX:
                self.unsetup()
                view = ToBeContinued()
                view.setup(self._root_dir)

                arcade.get_window().show_view(view)

    def load_config(self) -> None:
        """ Load config """

        path = os.path.join(self._root_dir, 'resources', 'maps', 'maps.json')
        with open(path, mode='r', encoding=DEFAULT_ENCODING) as file:
            return json.load(file)

    @property
    def rumble(self) -> int:
        """ Get rumble """

        return self._rumble
