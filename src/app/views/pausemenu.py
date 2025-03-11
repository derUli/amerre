""" Pause Menu """

import logging
import sys

import arcade
import arcade.gui
from arcade.gui import UIOnActionEvent

from app.constants.input.controllers import KEY_START
from app.constants.input.keyboard import KEY_ESCAPE
from app.constants.ui import BUTTON_WIDTH
from app.views.ui.settings.settings import Settings

MODAL_WIDTH = 300
MODAL_HEIGHT = 200


class PauseMenu(arcade.View):
    """ Pause Menu """

    def __init__(self, previous_view: arcade.View):
        """ Constructor """

        super().__init__()

        self.previous_view = previous_view
        self._manager = arcade.gui.UIManager()
        self._manager2 = None
        self._root_dir = None

    def setup(self, root_dir):
        self._root_dir = root_dir
        self.window.set_mouse_visible(True)

        btn_continue = arcade.gui.UIFlatButton(
            text=_('Continue'),
            width=BUTTON_WIDTH,
        )

        @btn_continue.event("on_click")
        def on_click_btn_continue(event):
            """ Continue button clicked """

            logging.debug(event)
            self.on_continue()

        btn_settings = arcade.gui.UIFlatButton(
            text=_('Settings'),
            width=BUTTON_WIDTH,
        )

        @btn_settings.event("on_click")
        def on_click_settings(event):
            """ settings button clicked """

            logging.debug(event)
            self._manager.disable()
            self._manager2 = Settings()
            self._manager2.setup(self.on_close_settings)

        btn_exit_to_menu = arcade.gui.UIFlatButton(
            text=_('Back to Menu'),
            width=BUTTON_WIDTH
        )

        @btn_exit_to_menu.event("on_click")
        def on_click_btn_exit_to_menu(event):
            """ Exit button clicked """

            logging.debug(event)
            self.on_exit_to_menu()

        btn_exit_to_desktop = arcade.gui.UIFlatButton(
            text=_('Exit to desktop'),
            width=BUTTON_WIDTH
        )

        @btn_exit_to_desktop.event("on_click")
        def on_click_btn_exit_to_desktop(event):
            """ Exit button clicked """

            logging.debug(event)
            self.on_exit_to_desktop()

        grid = arcade.gui.UIGridLayout(column_count=1, row_count=4, vertical_spacing=20)
        grid.add(btn_continue, row=0)
        grid.add(btn_settings, row=1)
        grid.add(btn_exit_to_menu, row=2)
        grid.add(btn_exit_to_desktop, row=3)

        # Passing the main view into menu view as an argument.
        anchor = self._manager.add(arcade.gui.UIAnchorLayout())

        anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=grid,
        )

        self._manager.add(anchor)
        self._manager.enable()

    def on_hide_view(self) -> None:
        """ On hide view """
        self._manager.disable()
        self._manager.clear()
        self.window.set_mouse_visible(False)
        self._manager.disable()

    def on_draw(self) -> None:
        """ On draw menu """

        self.clear()
        if self._manager2:
            self._manager2.draw()
            self.window.draw_after()
            return

        self._manager.draw()

        self.window.draw_after()

    def on_update(self, delta_time: float) -> None:
        """ On update menu """

        self._manager.on_update(delta_time)

        if self._manager2:
            self._manager2.on_update(delta_time)

    def on_continue(self) -> None:
        """ On continue game """

        self.window.show_view(self.previous_view)

        self.previous_view.on_continue()

    def on_exit_to_menu(self, event: UIOnActionEvent | None = None) -> None:
        """ On exit to menu """

        if not event:
            dialog = arcade.gui.UIMessageBox(
                message_text=_('Exit to main menu?'),
                buttons=(_('Yes'), _('No')),
                width=MODAL_WIDTH,
                height=MODAL_HEIGHT
            ).with_background(color=self.window.background_color)
            dialog.on_action = self.on_exit_to_menu
            self._manager.add(dialog)
            return

        if event.action != _('Yes'):
            return

        self.previous_view.unsetup()
        from app.views.mainmenu import MainMenu
        start_screen = MainMenu()
        start_screen.setup(self._root_dir)
        self.window.show_view(start_screen)


    def on_exit_to_desktop(self, event: UIOnActionEvent | None = None) -> None:
        """ On exit to desktop """

        if not event:
            dialog = arcade.gui.UIMessageBox(
                message_text=_('Exit to desktop?'),
                buttons=(_('Yes'), _('No')),
                width=MODAL_WIDTH,
                height=MODAL_HEIGHT
            ).with_background(color=self.window.background_color)
            dialog.on_action = self.on_exit_to_desktop
            self._manager.add(dialog)
            return

        if event.action != _('Yes'):
            return

        self.previous_view.unsetup()
        arcade.exit()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """ On key press """

        if symbol in KEY_ESCAPE:
            if self._manager2:
                return

            self.on_continue()

    def on_button_press(self, joystick, key) -> None:
        """ On controller button press """

        if key == KEY_START:
            self.on_continue()

    def on_close_settings(self, new_manager = None, on_change = None):
        self._manager2.disable()
        self._manager2 = new_manager
        if new_manager:
            return

        self._manager.enable()