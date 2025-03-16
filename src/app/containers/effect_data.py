""" Data container for effect setup() method  """

import arcade


class EffectData:
    """ Data container for effect setup() method  """

    def __init__(
            self,
            scene: arcade.scene.Scene = None,
            tilemap: arcade.tilemap.tilemap = None,
            root_dir: str = None,
            options: dict = None
    ):
        """
        Constructor.

        :param scene:
        :param tilemap:
        :param root_dir:
        :param options:
        """
        self.scene = scene
        self.tilemap = tilemap
        self.root_dir = root_dir
        self.options = options
