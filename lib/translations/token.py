from .. import language_tokens as tokens


def translate(self):
    return self.token


def __str__(self):
    return ' '.join(self.token)


def __repr__(self):
    return 'Token(%s)' % str(self)


def __eq__(self, other):
    if isinstance(other, str):
        return self.token == tokens.Token(other)
    if isinstance(other, tokens.Token):
        return self.token == other.token
    return False

