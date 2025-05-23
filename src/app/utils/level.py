""" Level """

import json
import logging
import os
import time

import arcade
import pyglet
from arcade import FACE_RIGHT, FACE_LEFT

from app.constants.gameinfo import DEFAULT_ENCODING, MAPS_FIRST
from app.constants.layers import (
    LAYER_WALL,
    LAYER_FADEOUT, LAYER_PLAYER, LAYER_FADEIN, LAYER_DOUBLEJUMP
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
from app.state.savegamestate import SavegameState
from app.state.settingsstate import SettingsState
from app.utils.audiovolumes import AudioVolumes
from app.utils.camera import Camera
from app.utils.voiceovertriggers import VoiceOverTiggers, \
    LIGHT_COLLISION_CHECK_THRESHOLD
from app.views.tobecontinued import ToBeContinued

GRAVITY_SLOWMO = 0.0003
GRAVITY_DEFAULT = 0.8

ALPHA_SPEED = 1
ALPHA_MAX = 255

LIGHT_LAUNCHING_RUMBLE = 100

VOLUME_MUSIC_MODIFIER = 0.2
VOLUME_ATMO_MODIFIER = 0.1

WHITE = arcade.csscolor.WHITE
BLUE = (58, 158, 236, 255)

VOLUME_MODIFIER_ABILITY_LEARN = 0.2


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
        self._state = None
        self._first_drawed = False

    def setup(self, root_dir: str, map_name: str, audio_volumes: AudioVolumes):
        """ Setup level """

        self._first_drawed = False
        self._root_dir = root_dir
        self._state = SettingsState().load()

        self.load_tilemap(
            os.path.join(root_dir, 'resources', 'maps', f"{map_name}.tmx"))
        self.load_config()

        h = arcade.get_window().height

        zoom = h / self._state.base_height
        self._camera = Camera(zoom=zoom)
        self._camera.setup(player=self._player.sprite)
        self._camera.on_update(0)

        self._camera_gui = arcade.camera.Camera2D()

        self.setup_physics_engine()
        self.wait_for_begin()

        config = self.load_config()
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

        self._effect_manager = EffectManager()
        self._effect_manager.setup(
            map_config,
            self._scene,
            self._tilemap,
            root_dir
        )
        color = WHITE

        # If the level is the first
        if map_name == MAPS_FIRST:
            color = BLUE

        # Add fade sprite to scene
        sprite = arcade.sprite.SpriteSolidColor(
            width=self._state.base_width,
            height=self._state.base_height,
            color=color
        )

        camera_x, camera_y = self._camera.position

        sprite.alpha = 255
        sprite.center_x = camera_x
        sprite.center_y = camera_y

        self._scene.add_sprite(LAYER_FADEIN, sprite)

    def setup_physics_engine(self):
        """ Setup physics engine """

        gravity = GRAVITY_SLOWMO

        if self._state.skip_slowmo:
            gravity = GRAVITY_DEFAULT

        self._physics_engine = arcade.PhysicsEnginePlatformer(
            self._player.sprite,
            ladders=None,
            walls=self._scene[LAYER_WALL],
            gravity_constant=gravity,
        )

        self._player.setup_physics_engine(self._physics_engine)

    def load_tilemap(self, path):
        """ Load tilemap """

        time_start = time.time()

        self._tilemap = arcade.load_tilemap(path)
        self._scene = arcade.Scene.from_tilemap(self._tilemap)
        self._player = Player()
        self._player.setup(self._scene[LAYER_PLAYER][0], self._root_dir)

        time_end = time.time() - time_start
        logging.info(f"Scene loaded in f{time_end} seconds")

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
        self._camera.on_update(delta_time)

        # Respawn on level start if the player falls through the map
        self._player.on_update(delta_time=delta_time)

    def on_fixed_update(
            self,
            delta_time: float,
            window,
            move_horizontal: int = None,
            camera_movement: tuple = (0, 0),
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

        self._camera.camera_movement = camera_movement

        self.check_collisions()
        self.check_powerup()

        self._effect_manager.on_fixed_update(delta_time)

        self._voiceover_triggers.on_update()

        self._physics_engine.update()

        if self._music and not self._music.playing:
            self._music.delete()

        self.update_fade()

    def check_powerup(self):

        # TODO: Move this into a separate class
        if not LAYER_DOUBLEJUMP in self._scene:
            return

        for sprite in self._scene[LAYER_DOUBLEJUMP]:
            if arcade.get_distance_between_sprites(self._player.sprite,
                                                   sprite) < LIGHT_COLLISION_CHECK_THRESHOLD:
                sprite.remove_from_sprite_lists()
                self._player.jump_count += 1
                self._physics_engine.enable_multi_jump(self._player.jump_count)
                file = os.path.join(
                    self._root_dir,
                    'resources',
                    'sounds',
                    'fx',
                    'ability_learn.mp3'
                )
                
                sound = arcade.load_sound(file, streaming=True)
                sound.play(
                    volume=self._state.audio_volumes.volume_sound_normalized * VOLUME_MODIFIER_ABILITY_LEARN
                )
                return

    def draw(self) -> None:
        """ Draw level """

        self._first_drawed = True
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

        self._player.change_x = -PLAYER_MOVE_SPEED * modifier * delta_time
        self._player.angle -= PLAYER_MOVE_ANGLE * modifier * delta_time

        if self._player.angle <= 0:
            self._player.angle = 360 - abs(self._player.angle)

    def move_right(self, delta_time: float, sprint: bool = False):
        """ Move right """

        if not self._can_walk:
            return

        modifier = MODIFIER_WALK

        if sprint:
            modifier = MODIFIER_SPRINT

        if self._voiceover_triggers.playing:
            modifier = MODIFIER_SPEECH

        self._player.change_x = PLAYER_MOVE_SPEED * modifier * delta_time
        self._player.angle += PLAYER_MOVE_ANGLE * modifier * delta_time

        if self._player.angle > 360:
            self._player.angle = self._player.angle - 360

    def move_stop(self):
        """ Stop walking """

        if not self._can_walk:
            return

        self._player.change_x = 0

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

    def check_collisions(self):
        """ Check for collisions """

        # Check for collisions with Power Ups
        self.check_powerup()

        if self._voiceover_triggers.check_for_collision(
                self._player.sprite,
                self._scene,
                self._root_dir,
                self._state.audio_volumes,
                self._music,
        ):
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

        self._state = SettingsState.load()

        if self._music:
            self._music.volume = (
                    self._state.audio_volumes.volume_music_normalized *
                    VOLUME_MUSIC_MODIFIER
            )

        if self._atmo:
            self._atmo.volume = (
                    self._state.audio_volumes.volume_sound_normalized *
                    VOLUME_ATMO_MODIFIER
            )

        if self._voiceover_triggers.media:
            self._voiceover_triggers.media.volume = (
                self._state.audio_volumes.volume_speech_normalized
            )

        # Start sound playback
        for sound in sounds:
            if sound:
                sound.play()

        self._effect_manager.refresh()
        self._player.refresh()

    def on_level_completed(self) -> None:
        """ Called when a level is completed """

        savegame_state = SavegameState.load()
        savegame_state.next_level()
        savegame_state.save()

        # Add fade sprite to scene
        sprite = arcade.sprite.SpriteSolidColor(
            width=self._state.base_width,
            height=self._state.base_height,
            color=WHITE
        )

        # It is initially hidden
        # On next update it will change to visible
        sprite.alpha = 0
        sprite.visible = False

        self._scene.add_sprite(LAYER_FADEOUT, sprite)
        self.update_fade()

    def on_unlock_double_jump(self) -> None:
        """ CHEAT - Unlock the double jump"""

        self._physics_engine.enable_multi_jump(allowed_jumps=2)

    def update_fade(self) -> None:
        """ Update fade """

        camera_x, camera_y = self._camera.position

        if LAYER_FADEIN in self._scene:
            sprite = self._scene[LAYER_FADEIN][0]
            sprite.center_x = camera_x
            sprite.center_y = camera_y

            sprite.alpha = max(0, sprite.alpha - ALPHA_SPEED)

            if sprite.alpha <= 0:
                self._scene.remove_sprite_list_by_name(LAYER_FADEIN)
            return

        if LAYER_FADEOUT not in self._scene:
            return

        if not any(self._scene[LAYER_FADEOUT]):
            return

        sprite = self._scene[LAYER_FADEOUT][0]

        sprite.center_x = camera_x
        sprite.center_y = camera_y
        sprite.visible = True

        if sprite.alpha < ALPHA_MAX:
            sprite.alpha = min(sprite.alpha + ALPHA_SPEED, ALPHA_MAX)

            if sprite.alpha >= ALPHA_MAX:
                self.unsetup()

                current_level = SavegameState.load().current_level
                if current_level is not None:
                    self.setup(
                        root_dir=self._root_dir,
                        map_name=current_level,
                        audio_volumes=self._state.audio_volumes
                    )
                else:
                    view = ToBeContinued()
                    view.setup(self._root_dir)
                    arcade.get_window().show_view(view)

    def load_config(self) -> dict:
        """ Load map config """

        path = os.path.join(self._root_dir, 'resources', 'maps', 'maps.json')
        with open(path, mode='r', encoding=DEFAULT_ENCODING) as file:
            return json.load(file)

    @property
    def rumble(self) -> int:
        """ Get rumble """

        return self._rumble
