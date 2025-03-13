import sys


def is_frozen() -> bool:
    return hasattr(sys, 'frozen')