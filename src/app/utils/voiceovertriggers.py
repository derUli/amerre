""" Voice over trigger handling """
import logging
import os
import random

import arcade
import pyglet

from app.constants.gameinfo import LOCALE_FALLBACK
from app.containers.callbacks import Callbacks
from app.helpers.string import label_value
from app.utils.audiovolumes import AudioVolumes
from app.utils.subtitle import Subtitle

VOICEOVER_DEFAULT = 'text00.mp3'
MULTIPLIER_MUSIC = 0.66


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

    def setup(self, voiceover_range: list, callbacks: Callbacks):
        """ Setup """

        self._callbacks = callbacks

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
    def voiceover_path(root_dir: str, languages: list, voiceover: str) -> str:
        """ Get path to voiceover """

        for l in languages:
            path = os.path.join(root_dir, 'resources', 'speech', l[0],
                                voiceover)
            if os.path.isfile(path):
                return path

        return os.path.join(
            root_dir,
            'resources',
            'speech',
            LOCALE_FALLBACK,
            voiceover
        )

    def play_voiceover(
            self,
            delta_time: float,
            root_dir: str,
            voiceover: str,
            audio_volumes: AudioVolumes,
            music: pyglet.media.player.Player
    ):
        """ Play voiceover """

        logging.info(label_value('Play speech', voiceover))

        languages = list(
            map(lambda x: x.split('_'), os.environ['LANG'].split(':')))
        filename = self.voiceover_path(root_dir, languages, voiceover)
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
