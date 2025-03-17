""" Logging utilities """

import locale
import logging
import os
import platform
import sys
from logging.handlers import RotatingFileHandler

import psutil
import pyglet

from app.helpers.audio import audio_drivers
from app.helpers.display import default_mode
from app.helpers.paths import log_path
from app.helpers.string import label_value

try:
    import sounddevice
except ImportError as e:
    logging.error(e)
    sounddevice = None
except OSError as e:
    logging.error(e)
    sounddevice = None


def get_handlers() -> list:
    """ Get log handlers """

    if not os.path.exists(log_path()):
        os.makedirs(log_path())

    log_file = os.path.join(log_path(), 'debug.log')

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,  # Maximum log file size 5 MB
        # Keep previous 3 log files
        backupCount=3,
    )
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    return [file_handler, stdout_handler]


def configure_logger(log_level: int | str = logging.INFO) -> None:
    """
    Configure logger
    @param log_level: Log level
    """

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=get_handlers()
    )


def log_hardware_info() -> None:
    """
    Log hardware info
    """

    # Log OS info
    uname = platform.uname()
    logging.info(label_value('OS', f"{uname.system} {uname.version}"))

    # Log CPU model
    logging.info(label_value('CPU', uname.processor))

    # Log the ram size
    ram_size = round(psutil.virtual_memory().total / 1024 / 1024 / 1024)
    logging.info(label_value('RAM', f"{ram_size} GB"))

    # Renderer is the GPU
    import arcade
    window = arcade.get_window()

    logging.info(label_value('GPU VENDOR', window.ctx.info.VENDOR))
    logging.info(label_value('GPU RENDERER', window.ctx.info.RENDERER))
    logging.info(
        label_value('GPU MAX_TEXTURE_SIZE', window.ctx.info.MAX_TEXTURE_SIZE))

    logging.info(
        label_value('OpenGL version', pyglet.gl.gl_info.get_version_string()))

    logging.info(
        label_value(
            'Display mode',
            default_mode()
        )
    )

    log_audio_info_audio()

    logging.info(label_value('Locale', locale.getlocale()))


def log_audio_info_audio() -> None:
    """ Log audio info """

    logging.info(label_value("Available audio drivers", audio_drivers()))
    logging.info(
        label_value("Audio driver", pyglet.media.get_audio_driver())
    )

    if not sounddevice:
        logging.info(label_value('Audio', 'Unknown'))
        return

    # Log the audio devices
    for device in sounddevice.query_devices():
        logging.info(label_value('Audio', device['name']))