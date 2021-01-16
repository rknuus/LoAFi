# Copyright (C) 2021 R. Knaus


class NonFilter(object):
    """A filter returning the input unchanged."""
    def __init__(self):
        super(NonFilter, self).__init__()

    def apply(input):
        return input
