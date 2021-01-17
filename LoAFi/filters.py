# Copyright (C) 2021 R. Knaus


class IncludeAll(object):
    """A filter including any input."""
    def __init__(self):
        super(IncludeAll, self).__init__()

    def apply(self, input):
        return True, input


class ExcludeAll(object):
    """A filter excluding any input."""
    def __init__(self):
        super(ExcludeAll, self).__init__()

    def apply(self, input):
        return True, None
