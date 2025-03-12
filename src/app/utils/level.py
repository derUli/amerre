""" Level """

import json
import logging
import os

import arcade
import pyglet
from arcade import FACE_RIGHT, FACE_LEFT

from app.constants.layers import (
    LAYER_PLAYER,
    LAYER_WALL,
    LAYERS_VOICEOVER,
    LAYER_FIRST_VOICEOVER, LAYER_FADEOUT
)
from app.effects.bushes import Bushes
from app.effects.tumbleweed import Tumbleweed
from app.effects.cloudanimation import CloudAnimation
from app.effects.filmgrain import Filmgrain
from app.effects.particles import Particles
from app.state.settingsstate import SettingsState
from app.utils.audiovolumes import AudioVolumes
from app.utils.callbacks import Callbacks
from app.utils.voiceovertriggers import VoiceOverTiggers
from app.views.tobecontinued import ToBeContinued

VIEWPORT_BASE_H = 1440
PLAYER_MOVE_SPEED = 4
PLAYER_JUMP_SPEED = 14
PLAYER_MOVE_ANGLE = 2

MODIFIER_WALK = 1.0
MODIFIER_SPRINT = 1.0
MODIFIER_SPEECH = MODIFIER_WALK

GRAVITY_SLOWMO = 0.001
GRAVITY_DEFAULT = 0.8

ALPHA_SPEED = 2
ALPHA_MAX = 255

LIGHT_LAUNCHING_MOVEMENT_SPEED = 10
LIGHT_LAUNCHING_ROTATING_SPEED = 5
LIGHT_COLLISION_CHECK_THRESHOLD = 100

VOLUME_MUSIC_MODIFIER = 0.3
VOLUME_ATMO_MODIFIER = 0.1

WHITE = arcade.csscolor.WHITE


class Level:
    """ Level """

    def __init__(self):
        """ Constructor"""

        self._scene = None
        self.tilemap = None
        self._camera = None
        self._camera_gui = None
        self._physics_engine = None
        self._can_walk = False
        self._launching_sprite = None
        self._voiceover_triggers = None
        self._music = None
        self._atmo = None
        self._animations = []

        self._root_dir = None

    def setup(self, root_dir: str, map_name: str, audio_volumes: AudioVolumes):
        """ Setup level """

        self._root_dir = root_dir

        self.load_tilemap(os.path.join(root_dir, 'resources', 'maps', f"{map_name}.tmx"))
        config = self.load_config()

        self._camera = arcade.camera.Camera2D()
        self._camera_gui = arcade.camera.Camera2D()

        self.setup_physics_engine()
        self.wait_for_begin()

        # TODO: play music by map triggers

        map_config = {}
        if map_name in config:
            map_config = config[map_name]

        if 'music' in map_config:
            music_file = os.path.join(root_dir, 'resources', 'music', map_config['music'])
            music = arcade.load_sound(music_file, streaming=True)
            loop = 'musicLoop' in map_config and map_config['musicLoop']
            self._music = music.play(volume=audio_volumes.volume_music_normalized * VOLUME_MUSIC_MODIFIER, loop=loop)

        atmo_file = os.path.join(root_dir, 'resources', 'sounds', 'atmos', f"{map_name}.mp3")

        if os.path.exists(atmo_file):
            atmo = arcade.load_sound(atmo_file, streaming=True)
            self._atmo = atmo.play(volume=audio_volumes.volume_sound_normalized * VOLUME_ATMO_MODIFIER, loop=True)

        callbacks = Callbacks(on_level_completed=self.on_level_completed)
        self._voiceover_triggers = VoiceOverTiggers().setup(callbacks=callbacks)
        self.scroll_to_player()

        animations = []

        if 'particles' in map_config and map_config['particles']:
            animations += [Particles()]

        if 'tumbleweed' in map_config and map_config['tumbleweed']:
            print('tumble')
            animations += [Tumbleweed()]

        animations += [
            CloudAnimation(),
            Bushes(),
            Filmgrain()
        ]
        self._animations = animations

        for animation in self._animations:
            animation.setup(self._scene, self.tilemap, root_dir, map_config)

    def read_config(self):

        with open('smartphone.json') as file:
            smartphone_dict = json.load(file)

        print(type(smartphone_dict))  # <class 'dict'>

    def setup_physics_engine(self):
        """ Setup physics engine """

        self._physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            ladders=None,
            walls=self._scene[LAYER_WALL],
            gravity_constant=GRAVITY_SLOWMO
        )

    def load_tilemap(self, path):
        """ Load tilemap """

        w, h = arcade.get_window().get_size()
        zoom = h / VIEWPORT_BASE_H

        self.tilemap = arcade.load_tilemap(path, scaling=zoom)
        self._scene = arcade.Scene.from_tilemap(self.tilemap)
        self.player.alpha = 0

    def update(
            self,
            delta_time: float,
            window,
            move_horizontal: int = None,
            jump: bool = False,
            sprint: bool = False
    ):
        """ Update """

        if jump:
            self.jump()

        if move_horizontal == FACE_RIGHT:
            self.move_right(sprint)
        elif move_horizontal == FACE_LEFT:
            self.move_left(sprint)
        else:
            self.move_stop()

        self.player.alpha = min(self.player.alpha + ALPHA_SPEED, 255)
        self.scroll_to_player()

        self._scene.update(delta_time)
        self._scene.update_animation(delta_time)
        self.check_collision_lights(window.root_dir, window.audio_volumes)
        self.update_collision_light()
        self.update_fade()

        for animation in self._animations:
            animation.update(delta_time)

        self._voiceover_triggers.update()

        if self._music and not self._music.playing:
            self._music.delete()

    def update_fixed(self):
        """ On Fixed update """

        self._physics_engine.update()

    def scroll_to_player(self, camera_speed=1):
        """ Scroll the window to the player. """

        player = self.player

        x, y = player.position

        self._camera.position = arcade.math.lerp_2d(
            self._camera.position, (x, y), camera_speed
        )

    def draw(self):
        """ Draw level """

        self._camera.use()
        self._scene.draw()

        for animation in self._animations:
            animation.draw()

        self._camera_gui.use()
        self._voiceover_triggers.draw_subtitle()

    def move_left(self, sprint: bool = False):
        """ Move left """

        if not self._can_walk:
            return

        modifier = MODIFIER_WALK

        if sprint:
            modifier = MODIFIER_SPRINT

        if self._voiceover_triggers.playing:
            modifier = MODIFIER_SPEECH

        self.player.change_x = -PLAYER_MOVE_SPEED * modifier
        self.player.angle -= PLAYER_MOVE_ANGLE * modifier

        if self.player.angle <= 0:
            self.player.angle = 360 - abs(self.player.angle)

    def move_right(self, sprint: bool = False):
        """ Move right """

        if not self._can_walk:
            return

        modifier = MODIFIER_WALK

        if sprint:
            modifier = MODIFIER_SPRINT

        if self._voiceover_triggers.playing:
            modifier = MODIFIER_SPEECH

        self.player.change_x = PLAYER_MOVE_SPEED * modifier
        self.player.angle += PLAYER_MOVE_ANGLE * modifier

        if self.player.angle > 360:
            self.player.angle = self.player.angle - 360

    def move_stop(self):
        """ Stop walking """

        if not self._can_walk:
            return

        self.player.change_x = 0

    def jump(self):
        """ Do jump """
        if not self._can_walk:
            return

        if not self._physics_engine.can_jump():
            return

        speed = PLAYER_JUMP_SPEED

        if self._voiceover_triggers.playing:
            speed *= MODIFIER_SPEECH

        self._physics_engine.jump(speed)

    @property
    def player(self):
        """ The player sprite """

        return self._scene[LAYER_PLAYER][0]

    def wait_for_begin(self, dt: float = 0.0):
        """ Wait for begin of level """

        if self._physics_engine.can_jump():
            self._can_walk = True
            self._physics_engine.gravity_constant = GRAVITY_DEFAULT
            return

        pyglet.clock.schedule_once(self.wait_for_begin, 1 / 4)

    def check_collision_lights(self, root_dir: str, volumes: AudioVolumes):
        """ Check for collisions with lights """

        if self._launching_sprite or self._voiceover_triggers.playing:
            return

        found = None

        for layer in LAYERS_VOICEOVER:
            if layer in self._scene:
                for sprite in self._scene[layer]:
                    if arcade.get_distance_between_sprites(
                            self.player,
                            sprite
                    ) < LIGHT_COLLISION_CHECK_THRESHOLD:
                        logging.info(f'Collided with {layer}')
                        self._launching_sprite = sprite
                        found = layer
                        break

        if not found:
            return

        arcade.load_sound(
            os.path.join(root_dir, 'resources', 'sounds', 'lights', 'missle-launch-001.mp3'),
            streaming=True
        ).play(volume=volumes.volume_sound_normalized)

        self._voiceover_triggers.playing = True

        voiceover = self._voiceover_triggers.pop(
            first=found == LAYER_FIRST_VOICEOVER
        )

        if not voiceover:
            logging.error('No voiceovers left')
            return

        pyglet.clock.schedule_once(
            self._voiceover_triggers.play_voiceover,
            2,
            root_dir,
            voiceover,
            volumes,
            self._music
        )

    def update_collision_light(self):
        """ Update voiceover light """

        if not self._launching_sprite:
            return

        self._launching_sprite.center_y += LIGHT_LAUNCHING_MOVEMENT_SPEED
        self._launching_sprite.angle = min(
            self._launching_sprite.angle + LIGHT_LAUNCHING_ROTATING_SPEED,
            360
        )

        if self._launching_sprite.angle >= 360:
            self._launching_sprite.angle = 0

        map_height = self.tilemap.height * self.tilemap.tile_height

        if self._launching_sprite.bottom > map_height:
            self._launching_sprite.remove_from_sprite_lists()
            self._launching_sprite = None

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

        for effect in self._animations:
            effect.refresh()

    def on_level_completed(self):
        """ Called when a level is completed """

        w, h = arcade.get_window().get_size()

        # Add fade sprite to scene
        sprite = arcade.sprite.SpriteSolidColor(width=w, height=h, color=WHITE)

        # It is initially hidden
        # On next update it will change to visible
        sprite.alpha = 0
        sprite.visible = False

        self._scene.add_sprite(LAYER_FADEOUT, sprite)
        self.update_fade()

    def update_fade(self):
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

                arcade.get_window().show_view(
                    ToBeContinued().setup(self._root_dir)
                )

    def load_config(self):
        path = os.path.join(self._root_dir, 'resources', 'maps', 'maps.json')
        with open(path) as file:
            return json.load(file)
