""" Video settings """

import arcade.gui
from arcade.gui.events import UIOnClickEvent, UIOnChangeEvent, UIOnActionEvent

from app.constants.settings import SETTINGS_UNLIMITED_DRAW_RATE, \
    SETTINGS_DRAW_RATES, ANTIALIASING_VALUES
from app.helpers.display import default_rate
from app.helpers.gui import make_label, make_button, make_slider, \
    make_restart_to_apply_settings_alert, make_vertical_ui_box_layout, \
    make_ui_anchor_layout
from app.helpers.localization import bool_to_on_off
from app.helpers.string import label_value
from app.views.ui.settings.settingsui import SettingsUi


class Video(SettingsUi):
    """ Video settings menu """

    def setup(self, on_close: callable, on_change: callable) -> None:
        """ Setup settings """

        super().setup(on_close, on_change)

        grid = arcade.gui.UIGridLayout(
            column_count=3,
            row_count=1,
            vertical_spacing=20
        )

        btn_back = make_button(text=_('Back'))
        btn_back.on_click = self.on_back
        grid.add(btn_back, col_num=0, row_num=0)

        btn_toggle_fullscreen = make_button(
            text=label_value(_('Fullscreen'),
                             bool_to_on_off(self._state.fullscreen)
                             ))
        btn_toggle_fullscreen.on_click = self.on_toggle_fullscreen

        grid.add(btn_toggle_fullscreen, col_num=1, row_num=0)

        btn_toggle_vsync = make_button(
            text=label_value(
                _('V-Sync'),
                bool_to_on_off(arcade.get_window().vsync)
            )
        )
        btn_toggle_vsync.on_click = self.on_toggle_vsync
        grid.add(btn_toggle_vsync, col_num=2, row_num=0)

        draw_rate_text = self._state.draw_rate
        if draw_rate_text == SETTINGS_UNLIMITED_DRAW_RATE:
            draw_rate_text = _('Unlimited')

        btn_fps_limit = make_button(
            text=label_value(_('FPS Limit'), str(draw_rate_text)))
        btn_fps_limit.on_click = self.on_change_fps_limit

        btn_toggle_fps = make_button(
            text=label_value(
                _('Show FPS'),
                bool_to_on_off(arcade.timings_enabled()
                               )
            )
        )
        btn_toggle_fps.on_click = self.on_toggle_fps
        grid.add(btn_toggle_fps, col_num=3, row_num=0)

        antialiasing_text = _('Off')

        if self._state.antialiasing:
            antialiasing_text = "MSAA " + str(self._state.antialiasing) + "x"

        btn_antialiasing = make_button(
            text=label_value(_('Anti-aliasing'), antialiasing_text)
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

        self.add(make_ui_anchor_layout([make_vertical_ui_box_layout(widgets)]))
        self.enable()

    def on_back(self, event: UIOnClickEvent) -> None:
        """ On go back """

        compares = [
            (self._old_state.antialiasing, self._state.antialiasing),
            (self.window.fullscreen, self._state.fullscreen),
        ]

        for compare in compares:
            old_value, new_value = compare
            if old_value != new_value:
                alert = make_restart_to_apply_settings_alert(
                    on_action=self._on_back
                )
                self.add(alert)
                return

        self._on_back(event)

    def _on_back(self, event: UIOnClickEvent | UIOnActionEvent) -> None:

        self.disable()
        self._on_close()

    def on_toggle_fps(self, event: UIOnClickEvent) -> None:
        """ On toggle fps display """

        if arcade.timings_enabled():
            arcade.disable_timings()
        else:
            arcade.enable_timings()

        self._state.show_fps = arcade.timings_enabled()
        self._state.save()

        self.refresh()

    def on_toggle_fullscreen(self, event: UIOnClickEvent) -> None:
        """ On toggle fullscreen """

        self._state.fullscreen = not self._state.fullscreen
        self._state.save()
        self.refresh()

    def on_toggle_vsync(self, event: UIOnClickEvent) -> None:
        """ On toggle vsync """

        arcade.get_window().set_vsync(not arcade.get_window().vsync)

        self._state.vsync = arcade.get_window().vsync
        self._state.save()

        arcade.get_window().set_draw_rate(1 / self._state.actual_draw_rate)

        self.refresh()

    def on_change_particles(self, event: UIOnChangeEvent) -> None:
        """ master volume changed """

        self._state.particles = float(event.new_value)
        self._state.save()
        self._on_change(refresh_particles=True)

    def on_change_fps_limit(self, event):
        """ On change fps limit  """

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
            draw_rate = default_rate()

        self._state.draw_rate = draw_rates[index]

        self.window.set_draw_rate(1.0 / draw_rate)

        self._state.save()
        self.refresh()

    def on_change_antialiasing(self, event: UIOnChangeEvent) -> None:
        """ On change antialiasing """
        index = ANTIALIASING_VALUES.index(self._state.antialiasing)
        index += 1

        try:
            self._state.antialiasing = ANTIALIASING_VALUES[index]
        except IndexError:
            self._state.antialiasing = 0

        self._state.save()
        self.refresh()

    def refresh(self):
        """ On refresh view """

        self.setup(self._on_close, self._on_change)
