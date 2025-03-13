import time
from typing import Iterable

from arcade import PhysicsEnginePlatformer, Sprite, SpriteList
from arcade.physics_engines import _move_sprite

# TODO: naming
LAST_DELTA_MAX = 1 / 60

class PhysicsEngine(PhysicsEnginePlatformer):
    def __init__(
            self,
            player_sprite: Sprite,
            platforms: SpriteList | Iterable[SpriteList] | None = None,
            gravity_constant: float = 0.5,
            ladders: SpriteList | Iterable[SpriteList] | None = None,
            walls: SpriteList | Iterable[SpriteList] | None = None
    ):
        super().__init__(player_sprite, platforms, gravity_constant, ladders, walls)
        self._falling = False

    def handle_gravity(self, delta_time):
        if not self.is_on_ladder() and not self._falling:
            self.player_sprite.change_y -= self.gravity_constant

    def update(self):
        """Move the player and platforms, then return colliding sprites.

              The returned sprites will in a :py:class:`list` of individual
              sprites taken from all :py:class:`arcade.SpriteList` instances
              in the following:

              * :attr:`~platforms`
              * :attr:`~walls`

              The :py:attr:`~ladders` are not included.

              Returns:
                  A list of all sprites the player collided with. If there
                  were no collisions, the list will be empty.
              """
        # start_time = time.time()
        # print(f"Spot A ({self.player_sprite.center_x}, {self.player_sprite.center_y})")

        # --- Add gravity if we aren't on a ladder

        # print(f"Spot B ({self.player_sprite.center_x}, {self.player_sprite.center_y})")

        for platform_list in self.platforms:
            for platform in platform_list:
                if platform.change_x != 0 or platform.change_y != 0:
                    # Check x boundaries and move the platform in x direction
                    if platform.boundary_left and platform.left <= platform.boundary_left:
                        platform.left = platform.boundary_left
                        if platform.change_x < 0:
                            platform.change_x *= -1

                    if platform.boundary_right and platform.right >= platform.boundary_right:
                        platform.right = platform.boundary_right
                        if platform.change_x > 0:
                            platform.change_x *= -1

                    platform.center_x += platform.change_x

                    # Check y boundaries and move the platform in y direction
                    if platform.boundary_top is not None and platform.top >= platform.boundary_top:
                        platform.top = platform.boundary_top
                        if platform.change_y > 0:
                            platform.change_y *= -1

                    if (
                            platform.boundary_bottom is not None
                            and platform.bottom <= platform.boundary_bottom
                    ):
                        platform.bottom = platform.boundary_bottom
                        if platform.change_y < 0:
                            platform.change_y *= -1

                    platform.center_y += platform.change_y

        complete_hit_list = _move_sprite(self.player_sprite, self._all_obstacles, ramp_up=True)

        # print(f"Spot Z ({self.player_sprite.center_x}, {self.player_sprite.center_y})")
        # Return list of encountered sprites
        # end_time = time.time()
        # print(f"Update - {end_time - start_time:7.4f}\n")

        return complete_hit_list
