import os

import userpaths

from app.constants.gameinfo import DIRECTORY_GAME_NAME_WIN


def data_path() -> str:
    """ Data directory """

    if os.name == 'nt':
        return str(os.path.join(userpaths.get_my_documents(), 'My Games', DIRECTORY_GAME_NAME_WIN))
    else:
        return str(os.path.join(userpaths.get_profile(), DIRECTORY_GAME_NAME_WIN))


def screenshot_path() -> str:
    """ Screenshot path """

    return os.path.join(data_path(), 'screenshots')


def settings_path() -> str:
    """ Settings path """

    return os.path.join(data_path(), 'settings', 'settings.json')


def log_path() -> str:
    """ Log path """

    return os.path.join(data_path(), 'logs')
