from .. import language_tokens as tokens

from ..hitbasic import Surrogate


class Token:

    def __init__(self, rule, position, error, token, **kwargs):
        Surrogate.__init__(self, rule, position, error, **kwargs)
        self.token = tuple(t.title() for t in token)


    def translate(self):
        return tuple(t.upper() for t in self.token)


    def __str__(self):
        return ' '.join(tuple(t.title() for t in self.token))


    def __repr__(self):
        return 'Token(%s)' % str(self)


    def __eq__(self, other):
        if isinstance(other, str):
            return self.token == (other.title(),)
        if isinstance(other, Token):
            return self.token == other.token
        if isinstance(other, tokens.Token):
            return repr(self) == repr(other)
        return False

