""" Audio settings """

import arcade.gui
from arcade.gui.events import UIOnChangeEvent, UIOnClickEvent, UIOnActionEvent

from app.constants.settings import SETTINGS_DEFAULT_AUDIO_DRIVER
from app.helpers.audio import audio_drivers
from app.helpers.gui import make_label, make_button, make_slider, \
    make_restart_to_apply_settings_alert, make_vertical_ui_box_layout, \
    make_ui_anchor_layout
from app.helpers.localization import bool_to_on_off
from app.helpers.string import label_value
from app.state.settingsstate import SettingsState


class Audio(arcade.gui.UIManager):
    """ Audio settings menu """

    def __init__(self):
        """ Constructor """

        super().__init__()
        self._state = None
        self._old_state = None

        self._on_close = None
        self._on_change = None

    def setup(self, on_close, on_change) -> None:
        """ Setup settings """

        self.clear()

        self._on_close = on_close
        self._on_change = on_change

        self._state = SettingsState.load()

        if not self._old_state:
            self._old_state = SettingsState.load()

        grid = arcade.gui.UIGridLayout(column_count=3, row_count=1)

        btn_back = make_button(text=_('Back'))
        btn_back.on_click = self.on_back
        grid.add(btn_back, col_num=0, row_num=0)

        label_master = make_label(text=_('Master volume'))
        slider_master = make_slider(
            value=self._state.audio_volumes.volume_master,
            min_value=0,
            max_value=100
        )
        slider_master.on_change = self.on_change_volume_master

        label_sound = make_label(text=_('Sound volume'))
        slider_sound = make_slider(
            value=self._state.audio_volumes.volume_sound,
            min_value=0,
            max_value=100
        )
        slider_sound.on_change = self.on_change_volume_sound

        label_speech = make_label(text=_('Speech volume'))
        slider_speech = make_slider(
            value=self._state.audio_volumes.volume_speech,
            min_value=0,
            max_value=100
        )
        slider_speech.on_change = self.on_change_volume_speech

        label_music = make_label(text=_('Music volume'))
        slider_music = make_slider(
            value=self._state.audio_volumes.volume_music,
            min_value=0,
            max_value=100
        )
        slider_music.on_change = self.on_change_volume_music

        label_subtitle_size = make_label(text=_('Size of subtitles'))
        slider_subtitle_size = make_slider(
            value=self._state.subtitle_size,
            min_value=14,
            max_value=20
        )
        slider_subtitle_size.on_change = self.on_change_subtitle_size

        btn_toggle_subtitles = make_button(
            text=label_value(
                _('Subtitles'),
                bool_to_on_off(self._state.subtitle_enabled)
            ))

        btn_toggle_subtitles.on_click = self.on_toggle_subtitles

        label_subtitle_size.disabled = not self._state.subtitle_enabled
        slider_subtitle_size.disabled = not self._state.subtitle_enabled

        audio_driver = self._state.audio_driver

        if audio_driver == SETTINGS_DEFAULT_AUDIO_DRIVER:
            audio_driver = _('Auto detect')

        btn_audio_driver = make_button(
            label_value(_('Audio driver'), audio_driver)
        )
        btn_audio_driver.on_click = self.on_change_driver

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
            slider_subtitle_size,
            btn_audio_driver
        ]

        self.add(make_ui_anchor_layout([make_vertical_ui_box_layout(widgets)]))

        self.enable()

    def on_back(self, event):
        """ On go back """

        if self._old_state.audio_driver == self._state.audio_driver:
            self._on_back(event)
            return

        alert = make_restart_to_apply_settings_alert(on_action=self._on_back)
        self.add(alert)

    def _on_back(self, event: UIOnClickEvent | UIOnActionEvent) -> None:
        self._state.save()
        self.disable()
        self._on_close()

    def on_change_volume_master(self, event: UIOnChangeEvent) -> None:
        """ master volume changed """

        self._state.audio_volumes.volume_master = int(event.new_value)
        self._on_change(self._state)

    def on_change_volume_sound(self, event: UIOnChangeEvent) -> None:
        """ Sound volume changed """

        self._state.audio_volumes.volume_sound = int(event.new_value)
        self._on_change(self._state)

    def on_change_volume_speech(self, event: UIOnChangeEvent) -> None:
        """ Speech volume changed """

        self._state.audio_volumes.volume_speech = int(event.new_value)
        self._on_change(self._state)

    def on_change_volume_music(self, event: UIOnChangeEvent) -> None:
        """ On change music volume """

        self._state.audio_volumes.volume_music = int(event.new_value)
        self._on_change(self._state)

    def on_change_subtitle_size(self, event: UIOnChangeEvent) -> None:
        """ On change subtitle size """

        self._state.subtitle_size = int(event.new_value)
        self._on_change(self._state)

    def on_toggle_subtitles(self, event: UIOnClickEvent) -> None:
        """ On toggle subtitles """

        self._state.subtitle_enabled = not self._state.subtitle_enabled
        self._on_change(self._state)
        self._state.save()
        self.setup(self._on_close, self._on_change)

    def on_change_driver(self, event: UIOnClickEvent) -> None:
        """ On change driver """

        old_value = self._state.audio_driver

        try:
            index = audio_drivers().index(self._state.audio_driver)
            index += 1
        except ValueError:
            index = 0

        try:
            new_value = audio_drivers()[index]
        except IndexError:
            new_value = SETTINGS_DEFAULT_AUDIO_DRIVER

        if new_value == old_value:
            return

        self._state.audio_driver = new_value
        self._state.save()

        self.refresh()

    def refresh(self) -> None:
        """ On refresh view  """

        self.setup(self._on_close, self._on_change)
