class GenericBuilder:
    def __init__(self, identifier, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.identifier = identifier


class Function(GenericBuilder):
    pass


class Array(GenericBuilder):
    pass


class Scalar(GenericBuilder):
    pass
