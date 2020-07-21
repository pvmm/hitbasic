from . import NO_RULE
from .hitbasic import Surrogate
from .translations import token as token_module
from .helper import *


ALL_TOKENS = [ '=', ',', ';', 'AND', 'AS', 'B', 'BF', 'L', 'OR', 'R', 'STEP', 'TAND', 'TO', 'TOR', 'TPRESET', 'TPSET', 'THEN', 'TXOR', 'XOR' ]
token_type = type('Token', (Surrogate,), dict(token_module.__dict__['Token'].__dict__))
nil_type = type('Nil', (Surrogate,), {})


def contains(tokens, type=()):
    type = tuple([s.upper() for s in make_tuple(type)])
    return (isinstance(tokens, str) and tokens.upper() in ALL_TOKENS
            or isinstance(tokens, Token) and tokens.token.upper() in ALL_TOKENS and tokens.token == type)


def create_token(*tokens, **kwargs):
    # *tokens allow a composite token
    printable_tokens = ' '.join([token.title() for token in tokens])
    if ALL_TOKENS and not printable_tokens in ALL_TOKENS:
        raise NotImplementedError('token %s are not recognised' % printable_tokens)
    position = kwargs.pop('pos', 0)
    language_tokens = tuple([token.upper() for token in tokens])
    return Surrogate(NO_RULE, position, False, token=language_tokens, **kwargs)


class Token:

    def __init__(self, *tokens):
        self.token = tuple([token.title() for token in tokens])


    def __repr__(self):
        return 'Token(%s)' % ' '.join(self.token)
