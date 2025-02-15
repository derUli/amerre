#!/usr/bin/env python3

""" cx_freeze setup file """

import os
import sys

import cx_Freeze

target_name = 'amerre'
base = None

if sys.platform == 'win32':
    target_name = 'Amerre.exe'
    base = 'Win32GUI'

target = cx_Freeze.Executable(
    script="amerre.py",
    icon=os.path.join(
        os.path.dirname(__file__),
        'resources',
        'images',
        'ui',
        'icon.ico'
    ),
    base=base,
    target_name=target_name
)

options = {
    'build_exe': {
        "include_msvcr": True,
        'optimize': 2,
        'silent_level': 3,
        'includes': [
            'pyogg'
        ],
        'include_files': [
            'resources/',
            '../CREDITS.txt',
            '../CHANGES.txt'
        ],
    }
}

cx_Freeze.setup(
    name='Amerre',
    options=options,
    executables=[
        target
    ]
)
