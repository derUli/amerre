""" Settings menu """

from arcade.gui import UIOnClickEvent
from arcade.gui.events import UIOnActionEvent

from app.helpers.gui import make_button, make_vertical_ui_box_layout, \
    make_ui_anchor_layout
from app.state.savegamestate import SavegameState
from app.state.settingsstate import SettingsState
from app.views.ui.settings.audio import Audio
from app.views.ui.settings.general import General
from app.views.ui.settings.language import Language
from app.views.ui.settings.settingsui import SettingsUi
from app.views.ui.settings.video import Video


class Settings(SettingsUi):
    """ Settings menu """

    def setup(self, on_close: callable, on_change: callable) -> None:
        """ Setup settings """

        super().setup(on_close, on_change)

        btn_back = make_button(text=_('Back'))
        btn_back.on_click = self.on_back

        btn_video = make_button(text=_('Video'))
        btn_video.on_click = self.on_video

        btn_audio = make_button(text=_('Audio'))
        btn_audio.on_click = self.on_audio

        btn_general = make_button(text=_('Game'))
        btn_general.on_click = self.on_general

        btn_language = make_button(text=_('Language'))
        btn_language.on_click = self.on_language

        btn_delete_savegame = make_button(text=_('Delete Save game'))
        btn_delete_savegame.on_click = self.on_delete_savegame

        widgets = [
            btn_back,
            btn_video,
            btn_audio,
            btn_general,
            btn_language
        ]

        # TODO: Only show it in main menu
        if SavegameState.exists():
            widgets += [btn_delete_savegame]

        self.add(make_ui_anchor_layout([make_vertical_ui_box_layout(widgets)]))
        self.enable()

    def on_video(self, event: UIOnClickEvent) -> None:
        """ On click "Video" """

        self.disable()
        menu = Video()
        menu.setup(self.on_enable, self._on_change)
        self._on_close(menu)

    def on_audio(self, event: UIOnClickEvent) -> None:
        """ On click "Audio" """

        self.disable()
        menu = Audio()
        menu.setup(self.on_enable, self._on_change)
        self._on_close(menu)

    def on_general(self, event: UIOnClickEvent) -> None:
        """ On click "Game" """

        self.disable()
        menu = General()
        menu.setup(self.on_enable, self._on_change)
        self._on_close(menu)

    def on_language(self, event: UIOnClickEvent) -> None:
        """ On click "Language" """

        self.disable()
        menu = Language()
        menu.setup(self.on_enable, self._on_change)
        self._on_close(menu)

    def on_delete_savegame(self, event: UIOnClickEvent|UIOnActionEvent) -> None:
        """ delete savegame """

        # TODO ask for confirmation
        SavegameState.delete()
        self.refresh()

    def on_enable(self, refresh_particles: bool = False):
        """ On enable settings """

        self.enable()
        self._on_close(self)

    def on_back(self, event, refresh_particles=False):
        """ On go back """

        if refresh_particles:
            self._on_change(refresh_particles=True)

        self.disable()
        self._on_close()

    def refresh(self):
        """ On refresh view """

        self.setup(self._on_close, self._on_change)