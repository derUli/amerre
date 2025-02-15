""" Audio volumes """


class AudioVolumes:
    """ Audio volumes """

    def __init__(
            self,
            volume_music: int,
            volume_sound: int,
            volume_master: int,
            volume_speech: int
    ):
        """ Constructor """

        self._volume_music = volume_music
        self._volume_sound = volume_sound
        self._volume_speech = volume_speech
        self._volume_master = volume_master

    @property
    def volume_master(self) -> int:
        """ Volume master """

        return self._volume_master

    @volume_master.setter
    def volume_master(self, value: int):
        """ Volume master """

        self._volume_master = value

    @property
    def volume_sound(self) -> int:
        """ Volume sound """

        return self._volume_sound

    @volume_sound.setter
    def volume_sound(self, value: int):
        """ Volume sound """

        self._volume_sound = value

    @property
    def volume_speech(self) -> int:
        """ Volume speech """

        return self._volume_speech

    @volume_speech.setter
    def volume_speech(self, value: int):
        """ Volume speech """

        self._volume_speech = value

    @property
    def volume_music(self) -> int:
        """ Volume music """

        return self._volume_music

    @volume_music.setter
    def volume_music(self, value: int):
        """ Volume music """

        self._volume_music = value

    @property
    def volume_master_normalized(self) -> float:
        """ Normalized master volume as float """

        if self._volume_master <= 0:
            return 0.0

        return self._volume_master / 100

    @property
    def volume_music_normalized(self) -> float:
        """ Normalized music volume as float """

        if self._volume_music <= 0:
            return 0.0

        return self._volume_music / 100 * self.volume_master_normalized

    @property
    def volume_sound_normalized(self) -> float:
        """ Normalized sound volume as float """

        if self._volume_sound <= 0:
            return 0.0

        return self._volume_sound / 100 * self.volume_master_normalized

    @property
    def volume_speech_normalized(self) -> float:
        """ Normalized speech volume as float """

        if self._volume_speech <= 0:
            return 0.0

        return self._volume_speech / 100 * self.volume_master_normalized
