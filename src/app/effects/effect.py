""" Effect """

from app.containers.effect_data import EffectData


class Effect:
    """ Effect """

    def __init__(self):
        """ Constructor """

        self._data = None

    def setup(self, data: EffectData) -> None:
        """ Setup animation """

        self._data = data

    def on_update(self, delta_time: float) -> None:
        """
        Update it
        @param delta_time: float
        """

        return

    def on_fixed_update(self, delta_time: float) -> None:
        """
        Update it
        @param delta_time: float
        """

        return

    def draw(self) -> None:
        """ Draw effect """

        return

    def refresh(self) -> None:
        """ Refresh effect """

        return
