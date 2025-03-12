""" Effect """


class Effect:
    """ Effect """

    def __init__(self):
        """ Constructor """

        self._scene = None
        self._tilemap = None
        self._root_dir = None
        self._width = None
        self._options = {}

    def setup(self, scene, tilemap, root_dir: str, options: dict = None):
        """ Setup animation """

        self._scene = scene
        self._tilemap = tilemap
        self._root_dir = root_dir
        self._options = options

    def update(self, delta_time: float) -> None:
        """
        Update it
        @param delta_time: float
        """

        return

    def draw(self) -> None:
        """ Draw effect """

        return

    def refresh(self) -> None:
        return
