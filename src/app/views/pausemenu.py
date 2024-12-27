""" Pause Menu """

import logging

import arcade
import arcade.gui
from arcade.gui import UIOnActionEvent

from app.constants.input.controllers import KEY_START
from app.constants.input.keyboard import KEY_ESCAPE
from app.constants.ui import BUTTON_WIDTH

MODAL_WIDTH = 300
MODAL_HEIGHT = 200


class PauseMenu(arcade.View):
    """ Pause Menu """

    def __init__(self, previous_view: arcade.View):
        """ Constructor """

        super().__init__()

        self.previous_view = previous_view
        self.manager = arcade.gui.UIManager()
        self._root_dir = None

    def setup(self, root_dir):
        self._root_dir = root_dir
        self.window.set_mouse_visible(True)
        self.manager = arcade.gui.UIManager()

        btn_continue = arcade.gui.UIFlatButton(
            text=_('Continue'),
            width=BUTTON_WIDTH,
        )

        @btn_continue.event("on_click")
        def on_click_btn_continue(event):
            """ Continue button clicked """

            logging.debug(event)
            self.on_continue()

        btn_exit = arcade.gui.UIFlatButton(
            text=_('Back to Menu'),
            width=BUTTON_WIDTH
        )

        @btn_exit.event("on_click")
        def on_click_btn_exit(event):
            """ Exit button clicked """

            logging.debug(event)
            self.on_exit()

        grid = arcade.gui.UIGridLayout(column_count=2, row_count=2, vertical_spacing=20)
        grid.add(btn_continue, row=0)
        grid.add(btn_exit, row=1)

        # Passing the main view into menu view as an argument.
        anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=grid,
        )

        self.manager.add(anchor)
        self.manager.enable()

    def on_hide_view(self) -> None:
        """ On hide view """

        self.manager.disable()
        self.manager.clear()
        self.window.set_mouse_visible(False)
        self.manager = None

    def on_draw(self) -> None:
        """ On draw menu """

        self.clear()
        self.manager.draw()

    def on_update(self, delta_time: float) -> None:
        """ On update menu """

        self.manager.on_update(delta_time)

    def on_continue(self) -> None:
        """ On continue game """

        self.window.show_view(self.previous_view)

        self.previous_view.on_continue()

    def on_exit(self, event: UIOnActionEvent | None = None) -> None:
        """ On exit to menu """

        if not event:
            dialog = arcade.gui.UIMessageBox(
                message_text=_('Exit to main menu?'),
                buttons=(_('Yes'), _('No')),
                width=MODAL_WIDTH,
                height=MODAL_HEIGHT
            ).with_background(color=self.window.background_color)
            dialog.on_action = self.on_exit
            self.manager.add(dialog)
            return

        if event.action != _('Yes'):
            return

        self.previous_view.unsetup()
        from app.views.mainmenu import MainMenu
        start_screen = MainMenu()
        start_screen.setup(self._root_dir)
        self.window.show_view(start_screen)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """ On key press """

        if symbol in KEY_ESCAPE:
            self.on_continue()

    def on_button_press(self, joystick, key) -> None:
        """ On controller button press """

        if key == KEY_START:
            self.on_continue()
