""" Video settings """
import logging

import arcade.gui

from app.constants.fonts import FONT_CONSOLA_MONO
from app.constants.ui import BUTTON_WIDTH
from app.state.settingsstate import SettingsState

MARGIN = 20

class Audio(arcade.gui.UIManager):
    """ Settings settings """

    def __init__(self):
        """ Constructor """

        super().__init__()
        self._state = None

        self._on_close = None
        self._on_change = None

    def setup(self, on_close, on_change) -> None:
        """ Setup settings """

        self.clear()
        self._on_close = on_close
        self._on_change = on_change

        self._state = SettingsState.load()

        grid = arcade.gui.UIGridLayout(column_count=3, row_count=1)

        btn_back = arcade.gui.UIFlatButton(text=_('Back'), width=BUTTON_WIDTH)
        btn_back.on_click = self.on_back
        grid.add(btn_back, col_num=0, row_num=0)

        label_master = arcade.gui.UILabel(text=_('Master volume'), width=BUTTON_WIDTH, font_name=FONT_CONSOLA_MONO)
        slider_master = arcade.gui.UISlider(
            value=self._state.audio_volumes.volume_master,
            min_value=0,
            max_value=100,
            width=BUTTON_WIDTH
        )
        slider_master.on_change = self.on_change_volume_master

        label_sound = arcade.gui.UILabel(text=_('Sound volume'), width=BUTTON_WIDTH, font_name=FONT_CONSOLA_MONO)
        slider_sound = arcade.gui.UISlider(
            value=self._state.audio_volumes.volume_sound,
            min_value=0,
            max_value=100,
            width=BUTTON_WIDTH
        )
        slider_sound.on_change = self.on_change_volume_sound

        label_speech = arcade.gui.UILabel(text=_('Speech volume'), width=BUTTON_WIDTH, font_name=FONT_CONSOLA_MONO)
        slider_speech = arcade.gui.UISlider(
            value=self._state.audio_volumes.volume_speech,
            min_value=0,
            max_value=100,
            width=BUTTON_WIDTH
        )
        slider_speech.on_change = self.on_change_volume_speech


        label_music = arcade.gui.UILabel(text=_('Music volume'), width=BUTTON_WIDTH, font_name=FONT_CONSOLA_MONO)
        slider_music = arcade.gui.UISlider(
            value=self._state.audio_volumes.volume_music,
            min_value=0,
            max_value=100,
            width=BUTTON_WIDTH
        )
        slider_music.on_change = self.on_change_volume_music


        label_subtitle_size = arcade.gui.UILabel(text=_('Size of subtitles'), width=BUTTON_WIDTH, font_name=FONT_CONSOLA_MONO)
        slider_subtitle_size = arcade.gui.UISlider(
            value=self._state.subtitle_size,
            min_value=0,
            max_value=24,
            width=BUTTON_WIDTH
        )
        slider_subtitle_size.on_change = self.on_change_subtitle_size

        subtitles_text = _('Off')
        if self._state.subtitle_enabled:
            subtitles_text = _('On')

        btn_toggle_subtitles = arcade.gui.UIFlatButton(
            text=': '.join([_('Subtitles'), subtitles_text]),
            width=BUTTON_WIDTH
        )

        btn_toggle_subtitles.on_click = self.on_toggle_subtitles

        label_subtitle_size.disabled = not self._state.subtitle_enabled
        slider_subtitle_size.disabled = not self._state.subtitle_enabled

        widgets = [
            btn_back,
            label_master,
            slider_master,
            label_sound,
            slider_sound,
            label_speech,
            slider_speech,
            label_music,
            slider_music,
            btn_toggle_subtitles,
            label_subtitle_size,
            slider_subtitle_size
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(align='center', space_between=MARGIN)

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.add(arcade.gui.UIAnchorLayout())

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.enable()

    def on_back(self, event):
        """ On go back """

        logging.debug(event)

        self._state.save()
        self.disable()
        self._on_close()

    def on_change_volume_master(self, event):
        self._state.audio_volumes.volume_master = int(event.new_value)
        self._on_change(self._state)

    def on_change_volume_sound(self, event):
        self._state.audio_volumes.volume_sound = int(event.new_value)
        self._on_change(self._state)

    def on_change_volume_speech(self, event):
        self._state.audio_volumes.volume_speech = int(event.new_value)
        self._on_change(self._state)

    def on_change_volume_music(self, event):
        self._state.audio_volumes.volume_music = int(event.new_value)
        self._on_change(self._state)

    def on_change_subtitle_size(self, event):
        self._state.subtitle_size = int(event.new_value)
        self._on_change(self._state)

    def on_toggle_subtitles(self, event):
        self._state.subtitle_enabled = not self._state.subtitle_enabled
        self._on_change(self._state)
        self._state.save()
        self.setup(self._on_close, self._on_change)