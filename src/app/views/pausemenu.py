""" Pause Menu """

import arcade
import arcade.gui
from arcade.gui import UIOnActionEvent

from app.constants.input.controllers import KEY_START
from app.constants.input.keyboard import KEY_ESCAPE
from app.constants.ui import MODAL_WIDTH, MODAL_HEIGHT
from app.helpers.gui import make_button, make_vertical_ui_box_layout, \
    make_ui_anchor_layout
from app.views.ui.settings.settings import Settings


class PauseMenu(arcade.View):
    """ Pause Menu """

    def __init__(self, previous_view: arcade.View):
        """ Constructor """

        super().__init__()

        self.previous_view = previous_view
        self._manager = arcade.gui.UIManager()
        self._manager2 = None
        self._root_dir = None

    def setup(self, root_dir: str) -> None:
        """ Setup pause menu """

        self._root_dir = root_dir
        self.window.set_mouse_visible(True)

        btn_continue = make_button(text=_('Continue'))

        @btn_continue.event("on_click")
        def on_click_btn_continue(event):
            """ Continue button clicked """

            self.on_continue()

        btn_settings = make_button(text=_('Settings'))

        @btn_settings.event("on_click")
        def on_click_settings(event):
            """ settings button clicked """

            self._manager.disable()
            self._manager2 = Settings()
            self._manager2.setup(self.on_close_settings,
                                 self.on_change_settings)

        btn_exit_to_menu = make_button(text=_('Back to Menu'))

        @btn_exit_to_menu.event("on_click")
        def on_click_btn_exit_to_menu(event):
            """ Exit button clicked """

            self.on_exit_to_menu()

        btn_exit_to_desktop = make_button(text=_('Exit to desktop'))

        @btn_exit_to_desktop.event("on_click")
        def on_click_btn_exit_to_desktop(event):
            """ Exit button clicked """

            self.on_exit_to_desktop()

        widgets = [
            btn_continue,
            btn_settings,
            btn_exit_to_menu,
            btn_exit_to_desktop
        ]

        # Passing the main view into menu view as an argument.
        self._manager.add(
            make_ui_anchor_layout([make_vertical_ui_box_layout(widgets)])
        )

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

        # pylint: disable=import-outside-toplevel
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

    def on_close_settings(self, new_manager=None, on_change=None):
        """ On close settings """

        self._manager2.disable()
        self._manager2 = new_manager
        if new_manager:
            return

        self._manager.enable()

    def on_change_settings(self, refresh_particles=False):
        """ On change settings """

        return
