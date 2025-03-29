""" Player entity"""
import logging
import os

import arcade

from app.entities.entity import Entity
from app.state.settingsstate import SettingsState

VOLUME_SOUND = 0.2


class Player(Entity):
    """ Player entity"""

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._physics_engine = None
        self._state = None
        self._sounds = {}
        self._can_jump_before = None
        self._jump_count = 1

    def setup(self, sprite: arcade.sprite.Sprite, root_dir) -> None:
        """ Set up the player entity """

        super().setup(sprite, root_dir)

        self.setup_sounds()
        self._state = SettingsState.load()

    def setup_sounds(self) -> None:
        """ Set up the sounds"""
        fx_dir = os.path.join(self._root_dir, 'resources', 'sounds', 'fx')

        self._sounds = {
            'jump': arcade.load_sound(
                os.path.join(fx_dir, 'jump.mp3'),
                streaming=False
            ),
            'landing': arcade.load_sound(
                os.path.join(fx_dir, 'landing.mp3'),
                streaming=False
            )
        }

    def setup_physics_engine(
            self,
            physics_engine: arcade.physics_engines.PhysicsEnginePlatformer
    ) -> None:
        """ Set the vars for the physics """

        self._physics_engine = physics_engine
        self._can_jump_before = self._physics_engine.can_jump()

    def on_update(self, delta_time: float) -> None:
        """ On update """

        if not self._can_jump_before and self._physics_engine.can_jump():
            self.landing_sound()

        self._can_jump_before = self._physics_engine.can_jump()

        # Reset the player to the initial position if he falls out of the map
        if self.sprite.bottom < 0:
            logging.error('Player out bounds')
            self.reset_initial_position()

    def jump_sound(self) -> None:
        """ Play jump sound """

        sound = self._sounds['jump']
        volume = (
                VOLUME_SOUND *
                self._state
                .audio_volumes.volume_sound_normalized

        )
        sound.play(volume)

    def landing_sound(self) -> None:
        """ Play landing sound """

        sound = self._sounds['landing']
        volume = (
                VOLUME_SOUND *
                self._state
                .audio_volumes.volume_sound_normalized

        )
        sound.play(volume)

    def refresh(self) -> None:
        """ Refresh player """

        self._state = SettingsState.load()

    @property
    def jump_count(self) -> int:
        return self._jump_count

    @jump_count.setter
    def jump_count(self, value: int) -> None:
        self._jump_count = value

