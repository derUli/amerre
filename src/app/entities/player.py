""" Player entity"""
import logging
import os

import arcade

from app.entities.entity import Entity
from app.state.settingsstate import SettingsState

VOLUME_SOUND = 0.2


class Player(Entity):
    """ Player entity"""

    def setup(self, sprite: arcade.sprite.Sprite, root_dir) -> None:
        super().setup(sprite, root_dir)

        self._attributes["sounds"] = {}
        self._attributes["state"] = SettingsState.load()

    def on_update(self) -> None:
        """ On update """

        # Reset the player to the initial position if he falls out of the map
        if self.sprite.bottom < 0:
            logging.error('Player out bounds')
            self.reset_initial_position()

    def jump_sound(self) -> None:
        """ Play jump sound """

        if 'jump' not in self._attributes['sounds']:
            jump_sound_file = os.path.join(
                self._root_dir, 'resources', 'sounds', 'fx', 'jump.mp3'
            )
            sound = arcade.load_sound(jump_sound_file, streaming=False)
            self._attributes['sounds']['jump'] = sound

        sound = self._attributes['sounds']['jump']
        volume = (
                VOLUME_SOUND *
                self._attributes['state']
                .audio_volumes.volume_sound_normalized

        )
        sound.play(volume)

    def refresh(self):
        self._attributes['state'] = SettingsState.load()
