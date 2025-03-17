#!/usr/bin/env python3
# coding=utf-8

""" Main file """

import logging
import os
import sys
from stopwatch import Stopwatch

from app.helpers.dev import is_frozen, configure_pyglet
from app.utils.log import configure_logger

# Start a stopwatch
stopwatch = Stopwatch()
stopwatch.start()

# Configure logger
configure_logger()

# Configure pyglet
configure_pyglet()

if is_frozen():
    root_dir = os.path.dirname(os.path.abspath(sys.executable))
else:
    root_dir = os.path.dirname(os.path.abspath(__file__))

from app.startup import Startup


try:
    Startup().setup(root_dir).start()
except KeyboardInterrupt as e:
    logging.debug(e)

stopwatch.stop()

logging.info(f'Running time: {stopwatch.elapsed}')
logging.info('Exit')
