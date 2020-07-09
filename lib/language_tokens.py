from . import NO_RULE
from .hitbasic import Surrogate
from .translations import token as token_module


OP_TOKENS = [ 'AND', 'AS', 'OR', 'XOR' ]
ALLOWED_TOKENS = [ '=', ',', ';', 'AND', 'AS', 'B', 'BF', 'L', 'OR', 'R', 'STEP', 'TAND', 'TO', 'TOR', 'TPRESET', 'TPSET', 'TXOR', 'XOR' ]
token_type = type('Token', (Surrogate,), dict(token_module.__dict__['Token'].__dict__))
nil_type = type('Nil', (Surrogate,), {})


def create_token(*tokens, **kwargs):
    # *tokens allow a composite token
    printable_tokens = ' '.join([token.title() for token in tokens])
    if ALLOWED_TOKENS and not printable_tokens in ALLOWED_TOKENS:
        raise NotImplementedError('token %s are not recognised' % printable_tokens)
    position = kwargs.pop('pos', 0)
    language_tokens = tuple([token.upper() for token in tokens])
    return Surrogate(NO_RULE, position, False, token=language_tokens, **kwargs)


class Token:

    def __init__(self, *tokens):
        self.token = tuple([token.title() for token in tokens])


    def __repr__(self):
        return 'Token(%s)' % ' '.join(self.token)
