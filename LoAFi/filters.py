# Copyright (C) 2021 R. Knaus


class IncludeAll(object):
    """A filter returning the input unchanged."""
    def __init__(self):
        super(IncludeAll, self).__init__()

    def apply(self, input):
        return input
