import os


def writeList(args = []):
    spacing = os.getenv('HITBASIC_SPACING', ' ');
    s = ''

    for i, arg in enumerate(args):
        s += 'f,{spacing}{param}' % param if ''.join(args[i:]) else ''

    return s
