""" Video settings """
import logging

import arcade.gui
import pyglet
from arcade.gui.events import UIOnClickEvent, UIOnChangeEvent, UIOnActionEvent

from app.constants.settings import SETTINGS_UNLIMITED_DRAW_RATE, \
    SETTINGS_DRAW_RATES, ANTIALIASING_VALUES
from app.helpers.gui import make_label, make_button, make_slider, make_alert
from app.state.settingsstate import SettingsState


class Video(arcade.gui.UIManager):
    """ Settings settings """

    def __init__(self):
        """ Constructor """

        super().__init__()
        self._state = None
        self._old_state = None
        self._on_close = None
        self._on_change = None

    def setup(self, on_close, on_change) -> None:
        """ Setup settings """

        self.disable()
        self.clear()
        self._on_close = on_close
        self._on_change = on_change
        self._state = SettingsState.load()

        if not self._old_state:
            self._old_state = SettingsState.load()

        grid = arcade.gui.UIGridLayout(column_count=3, row_count=1,
                                       vertical_spacing=20)

        btn_back = make_button(text=_('Back'))
        btn_back.on_click = self.on_back
        grid.add(btn_back, col_num=0, row_num=0)

        fullscreen_text = _('Off')
        if self._state.fullscreen:
            fullscreen_text = _('On')

        btn_toggle_fullscreen = make_button(
            text=': '.join([_('Fullscreen'), fullscreen_text]))
        btn_toggle_fullscreen.on_click = self.on_toggle_fullscreen

        # Currently disabled because it's buggy
        # btn_toggle_fullscreen.disabled = True

        grid.add(btn_toggle_fullscreen, col_num=1, row_num=0)

        vsync_text = _('Off')
        if arcade.get_window().vsync:
            vsync_text = _('On')

        btn_toggle_vsync = make_button(
            text=': '.join([_('V-Sync'), vsync_text]))
        btn_toggle_vsync.on_click = self.on_toggle_vsync
        grid.add(btn_toggle_vsync, col_num=2, row_num=0)

        draw_rate_text = self._state.draw_rate
        if draw_rate_text == SETTINGS_UNLIMITED_DRAW_RATE:
            draw_rate_text = _('Unlimited')

        btn_fps_limit = make_button(
            text=': '.join([_('FPS Limit'), str(draw_rate_text)]))
        btn_fps_limit.on_click = self.on_change_fps_limit

        fps_text = _('Off')
        if arcade.timings_enabled():
            fps_text = _('On')

        btn_toggle_fps = make_button(text=': '.join([_('Show FPS'), fps_text]))
        btn_toggle_fps.on_click = self.on_toggle_fps
        grid.add(btn_toggle_fps, col_num=3, row_num=0)

        antialiasing_text = _('Off')

        if self._state.antialiasing:
            antialiasing_text = "MSAA " + str(self._state.antialiasing) + "x"

        btn_antialiasing = make_button(
            text=': '.join([_('Antialiasing'), antialiasing_text])
        )
        btn_antialiasing.on_click = self.on_change_antialiasing
        grid.add(btn_toggle_fps, col_num=3, row_num=0)

        label_particles = make_label(text=_('Particles amount'))
        slider_particles = make_slider(value=self._state.particles,
                                       min_value=0.1, max_value=1.0)
        slider_particles.on_change = self.on_change_particles

        widgets = [
            btn_back,
            btn_toggle_fullscreen,
            btn_toggle_vsync,
            btn_fps_limit,
            btn_toggle_fps,
            btn_antialiasing,
            label_particles,
            slider_particles,
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=20, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.add(arcade.gui.UIAnchorLayout())

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.enable()

    def on_back(self, event: UIOnClickEvent) -> None:
        """ On go back """

        logging.debug(event)

        compares = [
            (self._old_state.antialiasing, self._state.antialiasing),
            (self.window.fullscreen, self._state.fullscreen),
        ]

        for compare in compares:
            old_value, new_value = compare
            if old_value != new_value:
                alert = make_alert(
                _('A restart is required to apply some settings.')
                )
                alert.on_action = self._on_back
                self.add(alert)
                return

        self._on_back(event)

    def _on_back(self, event: UIOnClickEvent| UIOnActionEvent) -> None:
        logging.debug(event)

        self.disable()
        self._on_close()

    def on_toggle_fps(self, event: UIOnClickEvent) -> None:
        """ On toggle fps display """

        logging.debug(event)

        if arcade.timings_enabled():
            arcade.disable_timings()
        else:
            arcade.enable_timings()

        self._state.show_fps = arcade.timings_enabled()
        self._state.save()

        self.refresh()

    def on_toggle_fullscreen(self, event: UIOnClickEvent) -> None:

        logging.debug(event)

        self._state.fullscreen = not self._state.fullscreen
        self._state.save()
        self.refresh()

    def on_toggle_vsync(self, event: UIOnClickEvent) -> None:

        logging.debug(event)

        arcade.get_window().set_vsync(not arcade.get_window().vsync)

        self._state.vsync = arcade.get_window().vsync
        self._state.save()

        arcade.get_window().set_draw_rate(1 / self._state.actual_draw_rate)

        self.refresh()

    def on_change_particles(self, event: UIOnChangeEvent) -> None:
        """ master volume changed """

        logging.debug(event)
        self._state.particles = float(event.new_value)
        self._state.save()
        self._on_change(refresh_particles=True)

    def on_change_fps_limit(self, event):
        logging.debug(event)
        current_fps = self._state.draw_rate
        draw_rates = SETTINGS_DRAW_RATES

        try:
            index = draw_rates.index(current_fps)
        except ValueError:
            index = 0

        if index <= len(draw_rates) - 2:
            index += 1
        else:
            index = 0

        draw_rate = draw_rates[index]

        if draw_rate == SETTINGS_UNLIMITED_DRAW_RATE and self._state.vsync:
            draw_rate = pyglet.display.get_display().get_default_screen().get_mode().rate

        self._state.draw_rate = draw_rates[index]

        self.window.set_draw_rate(1.0 / draw_rate)

        self._state.save()
        self.refresh()

    def on_change_antialiasing(self, event: UIOnChangeEvent) -> None:
        logging.debug(event)
        index = ANTIALIASING_VALUES.index(self._state.antialiasing)
        index += 1

        try:
            self._state.antialiasing = ANTIALIASING_VALUES[index]
        except IndexError:
            self._state.antialiasing = 0

        self._state.save()

        self.refresh()

    def refresh(self):
        self.setup(self._on_close, self._on_change)
