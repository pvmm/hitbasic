__version__ = 1.0

import os


spacing = os.getenv('HITBASIC_SPACING', ' ')


def write(object):
    for attr, value in object.__dict__.items():
        print(type(object).__name__, attr, value)
