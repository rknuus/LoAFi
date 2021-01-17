# Copyright (C) 2021 R. Knaus


class IncludeAll(object):
    """Include any input."""

    __parameters__ = []

    def __init__(self):
        super(IncludeAll, self).__init__()

    def apply(self, input):
        return True, input


class ExcludeAll(object):
    """Exclude any input."""

    __parameters__ = []

    def __init__(self):
        super(ExcludeAll, self).__init__()

    def apply(self, input):
        return True, None
