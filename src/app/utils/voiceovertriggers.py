""" Voice over trigger handling """
import logging
import os
import random

import arcade
import pyglet
from arcade import Sprite

from app.constants.layers import LAYERS_VOICEOVER, LAYER_FIRST_VOICEOVER
from app.containers.callbacks import Callbacks
from app.helpers.string import label_value
from app.utils.audiovolumes import AudioVolumes
from app.utils.subtitle import Subtitle

VOICEOVER_DEFAULT = 'text00.mp3'
MULTIPLIER_MUSIC = 0.66

LIGHT_LAUNCHING_MOVEMENT_SPEED = 1000
LIGHT_LAUNCHING_ROTATING_SPEED = 500
LIGHT_COLLISION_CHECK_THRESHOLD = 100


class VoiceOverTiggers:
    """ Voice over trigger handling """

    def __init__(self):
        """ Voice over trigger handling """
        self.playing = False
        self.randomized_voiceovers = []
        self._media = None
        self._callbacks = None
        self._music = None
        self._initial_volume = 0
        self._subtitle = Subtitle()
        self.launching_sprite = None
        self._tilemap = None
        self._missile_sound = None

    def setup(self, voiceover_range: list, callbacks: Callbacks,
              tilemap: arcade.TileMap):
        """ Setup """

        self._callbacks = callbacks
        self._tilemap = tilemap

        voiceovers = []

        for i in range(voiceover_range[0], voiceover_range[1]):
            voiceovers.append("text" + str(i).rjust(2, '0') + '.mp3')

        random.shuffle(voiceovers)

        self.randomized_voiceovers = voiceovers

        return self

    def on_speech_completed(self) -> None:
        """ Executed after voice playback is completed """

        logging.info('Speech completed')
        self._subtitle.clear()
        self._media = None

        if not any(self.randomized_voiceovers):
            logging.info('All voiceovers played')
            self._callbacks.on_level_completed()

        self.playing = False

        if self._music:
            self._music.volume = self._initial_volume
            self._music = None

    @staticmethod
    def voiceover_path(root_dir: str, language: str, voiceover: str) -> str:
        """ Get path to voiceover """

        return os.path.join(
            root_dir,
            'resources',
            'speech',
            language,
            voiceover
        )

    def play_voiceover(
            self,
            delta_time: float,
            root_dir: str,
            voiceover: str,
            audio_volumes: AudioVolumes,
            music: pyglet.media.player.Player,

    ):
        """ Play voiceover """

        logging.info(label_value('Play speech', voiceover))

        filename = self.voiceover_path(root_dir, os.environ['LANG'], voiceover)
        sound = arcade.load_sound(filename, streaming=True)

        playback = sound.play(volume=audio_volumes.volume_speech_normalized)
        playback.on_player_eos = self.on_speech_completed
        self._subtitle.load(filename)

        self._media = playback

        self._music = music

        if self._music and self._music.playing:
            self._initial_volume = self._music.volume
            self._music.volume = self._initial_volume * MULTIPLIER_MUSIC

    def pop(self, first=False) -> str | None:
        """ Pop voiceover """

        if first:
            return VOICEOVER_DEFAULT

        if not any(self.randomized_voiceovers):
            return None

        return self.randomized_voiceovers.pop(0)

    def draw_subtitle(self) -> None:
        """ Draw subtitle """

        self._subtitle.draw()

    @property
    def media(self):
        """ Get media """

        return self._media

    def on_update(self):
        """ Update voice over trigger """

        if not self._media:
            return

        self._subtitle.on_update(self._media)

    def update_collision_light(self, delta_time: float):
        """ Update voiceover light """

        if not self.launching_sprite:
            return

        self.launching_sprite.center_y += (
                LIGHT_LAUNCHING_MOVEMENT_SPEED * delta_time
        )
        self.launching_sprite.angle = min(
            self.launching_sprite.angle + LIGHT_LAUNCHING_ROTATING_SPEED * delta_time,
            360
        )

        if self.launching_sprite.angle >= 360:
            self.launching_sprite.angle = 0

        map_height = self._tilemap.height * self._tilemap.tile_height

        if self.launching_sprite.bottom > map_height:
            self.launching_sprite.remove_from_sprite_lists()
            self.launching_sprite = None

    def check_for_collision(
            self,
            player,
            scene,
            root_dir,
            volumes,
            music
    ) -> Sprite | None:
        """ Check for collision with voiceover triggers"""

        if self.launching_sprite or self.playing:
            return None

        found_sprite = None
        found_layer = None
        for layer in LAYERS_VOICEOVER:
            if layer in scene:
                for sprite in scene[layer]:
                    if arcade.get_distance_between_sprites(
                            player,
                            sprite
                    ) < LIGHT_COLLISION_CHECK_THRESHOLD:
                        found_sprite = sprite
                        found_layer = layer
                        break

        if not found_sprite:
            return None

        logging.info(f'Collided with {found_layer}')

        self.launching_sprite = found_sprite
        self.missile_sound = arcade.load_sound(
            os.path.join(root_dir, 'resources', 'sounds',
                         'lights',
                         'missle-launch-001.mp3'),
            streaming=True
        ).play(volume=volumes.volume_sound_normalized)

        self.playing = True

        voiceover = self.pop(first=found_layer == LAYER_FIRST_VOICEOVER)

        if not voiceover:
            logging.error('No voiceovers left')
            return None

        pyglet.clock.schedule_once(
            self.play_voiceover,
            2,
            root_dir,
            voiceover,
            volumes,
            music,
        )

        return found_sprite

    @property
    def missile_sound(self) -> arcade.Sound | None:
        """ Get missile sound """

        return self._missile_sound

    @missile_sound.setter
    def missile_sound(self, value: arcade.Sound | None) -> None:
        """ Set missile sound """

        self._missile_sound = value
