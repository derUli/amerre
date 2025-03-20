""" Player entity"""
import logging

from app.entities.entity import Entity


class Player(Entity):
    """ Player entity"""

    def on_update(self) -> None:
        """ On update """

        # Reset the player to the initial position if he falls out of the map
        if self.sprite.bottom < 0:
            logging.error(
                'Player falling out of map. Restoring initial position.'
            )
            self.reset_initial_position()
