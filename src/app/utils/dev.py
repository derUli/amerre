""" Dev utils """

import sys

def is_frozen() -> bool:
    """ Check is the app is frozen """

    return hasattr(sys, 'frozen')