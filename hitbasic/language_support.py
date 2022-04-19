class Builder:
    def __init__(self, identifier, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.identifier = identifier


class Function(Builder):
    pass


class Array(Builder):
    pass


class Scalar(Builder):
    pass
