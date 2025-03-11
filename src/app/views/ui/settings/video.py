""" Video settings """
import logging

import arcade.gui

from app.constants.fonts import FONT_CONSOLA_MONO
from app.constants.ui import BUTTON_WIDTH
from app.state.settingsstate import SettingsState


class Video(arcade.gui.UIManager):
    """ Settings settings """

    def __init__(self):
        """ Constructor """

        super().__init__()
        self._state = None
        self._callback = None

    def setup(self, callback) -> None:
        """ Setup settings """

        self.disable()
        self.clear()
        self._callback = callback
        self._state = SettingsState.load()

        grid = arcade.gui.UIGridLayout(column_count=3, row_count=1, vertical_spacing=20)

        btn_back = arcade.gui.UIFlatButton(text=_('Back'), width=BUTTON_WIDTH)
        btn_back.on_click = self.on_back
        grid.add(btn_back, col_num=0, row_num=0)

        fullscreen_text = _('Off')
        if arcade.get_window().fullscreen:
            fullscreen_text = _('On')

        btn_toggle_fullscreen = arcade.gui.UIFlatButton(
            text=': '.join([_('Fullscreen'), fullscreen_text]),
            width=BUTTON_WIDTH
        )
        btn_toggle_fullscreen.on_click = self.on_toggle_fullscreen

        # Currently disabled because it's buggy
        btn_toggle_fullscreen.disabled = True

        grid.add(btn_toggle_fullscreen, col_num=1, row_num=0)

        vsync_text = _('Off')
        if arcade.get_window().vsync:
            vsync_text = _('On')

        btn_toggle_vsync = arcade.gui.UIFlatButton(
            text=': '.join([_('V-Sync'), vsync_text]),
            width=BUTTON_WIDTH
        )
        btn_toggle_vsync.on_click = self.on_toggle_vsync
        grid.add(btn_toggle_vsync, col_num=2, row_num=0)

        fps_text = _('Off')
        if arcade.timings_enabled():
            fps_text = _('On')

        btn_toggle_fps = arcade.gui.UIFlatButton(
            text=': '.join([_('Show FPS'), fps_text]),
            width=BUTTON_WIDTH
        )
        btn_toggle_fps.on_click = self.on_toggle_fps
        grid.add(btn_toggle_fps, col_num=3, row_num=0)

        label_particles = arcade.gui.UILabel(text=_('Particles amount'), width=BUTTON_WIDTH, font_name=FONT_CONSOLA_MONO)
        slider_particles = arcade.gui.UISlider(
            value=self._state.particles,
            min_value=0.1,
            max_value=1.0,
            width=BUTTON_WIDTH
        )
        slider_particles.on_change = self.on_change_particles

        widgets = [
            btn_back,
            btn_toggle_fullscreen,
            btn_toggle_vsync,
            btn_toggle_fps,
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

    def on_back(self, event):
        """ On go back """

        logging.debug(event)

        self.disable()
        self._callback()


    def on_toggle_fps(self, event):

        logging.debug(event)

        if arcade.timings_enabled():
            arcade.disable_timings()
        else:
            arcade.enable_timings()

        self._state.show_fps = arcade.timings_enabled()
        self._state.save()

        self.setup(self._callback)

    def on_toggle_fullscreen(self, event):

        logging.debug(event)

        self._state.fullscreen = not arcade.get_window().fullscreen
        self._state.save()

        w, h = self._state.screen_resolution

        arcade.get_window().set_fullscreen(not arcade.get_window().fullscreen, width=w, height=h)

        if not self._state.fullscreen:
            arcade.get_window().set_size(w, h)

        self.setup(self._callback)

    def on_toggle_vsync(self, event):

        logging.debug(event)

        arcade.get_window().set_vsync(not arcade.get_window().vsync)

        self._state.vsync = arcade.get_window().vsync
        self._state.save()
        arcade.get_window().set_draw_rate(self._state.draw_rate)

        self.setup(self._callback)

    def on_change_particles(self, event):
        """ master volume changed """

        logging.debug(event)
        self._state.particles = float(event.new_value)
        self._state.save()
        self._callback(refresh_particles=True)