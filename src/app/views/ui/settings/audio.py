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

        self.disable()
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

        widgets = [
            btn_back,
            label_master,
            slider_master,
            label_sound,
            slider_sound,
            label_speech,
            slider_speech,
            label_music,
            slider_music
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


    def on_toggle_fps(self, event):

        logging.debug(event)

        if arcade.timings_enabled():
            arcade.disable_timings()
        else:
            arcade.enable_timings()

        self._state.show_fps = arcade.timings_enabled()
        self._state.save()

        self.setup(self._on_close)

    def on_toggle_fullscreen(self, event):

        logging.debug(event)

        self._state.fullscreen = not arcade.get_window().fullscreen
        self._state.save()

        w, h = self._state.screen_resolution

        arcade.get_window().set_fullscreen(not arcade.get_window().fullscreen, width=w, height=h)

        if not self._state.fullscreen:
            arcade.get_window().set_size(w, h)

        self.setup(self._on_close)

    def on_toggle_vsync(self, event):

        logging.debug(event)

        arcade.get_window().set_vsync(not arcade.get_window().vsync)

        self._state.vsync = arcade.get_window().vsync
        self._state.save()
        arcade.get_window().set_draw_rate(self._state.draw_rate)

        self.setup(self._on_close)

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