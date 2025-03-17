""" Logging utilities """
import locale
import logging
import os
import platform
import sys
from logging.handlers import RotatingFileHandler

import arcade
import psutil
import pyglet

try:
    import sounddevice
except ImportError as e:
    logging.error(e)
    sounddevice = None
except OSError as e:
    logging.error(e)
    sounddevice = None

from app.helpers.paths import log_path
from app.helpers.string import label_value


def get_handlers():
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


def log_hardware_info(window: arcade.Window) -> None:
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
    logging.info(label_value('GPU VENDOR', window.ctx.info.VENDOR))
    logging.info(label_value('GPU RENDERER', window.ctx.info.RENDERER))
    logging.info(
        label_value('GPU MAX_TEXTURE_SIZE', window.ctx.info.MAX_TEXTURE_SIZE))

    logging.info(
        label_value('OpenGL version', pyglet.gl.gl_info.get_version_string()))

    logging.info(
        label_value(
            'Screen resolution',
            pyglet.display.get_display().get_default_screen().get_mode()
        )
    )

    if not sounddevice:
        logging.info(label_value('Audio', 'Unknown'))
        return

    # Log the audio devices
    for audio in sounddevice.query_devices():
        logging.info(label_value('Audio', audio['name']))

    logging.info(label_value('Locale', locale.getlocale()))
