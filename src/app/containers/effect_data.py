import arcade


class EffectData:
    def __init__(
            self,
            scene: arcade.scene.Scene = None,
            tilemap: arcade.tilemap.tilemap = None,
            root_dir: str = None,
            options: dict = None
    ):
        self.scene = scene
        self.tilemap = tilemap
        self.root_dir = root_dir
        self.options = options
