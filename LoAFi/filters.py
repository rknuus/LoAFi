# Copyright (C) 2021 R. Knaus

import re


class IncludeAll(object):
    """Include any input."""

    __parameters__ = {}

    def __init__(self):
        super(IncludeAll, self).__init__()

    def apply(self, input):
        return True, input


class ExcludeAll(object):
    """Exclude any input."""

    __parameters__ = {}

    def __init__(self):
        super(ExcludeAll, self).__init__()

    def apply(self, input):
        return True, None


class IncludeMatch(object):
    """Include matching lines.

    Currently returns the entire line in case of a match. Later this will be
    improved.
    """

    __parameters__ = {'pattern': 'A regular expression pattern to match lines with. Required.'}

    def __init__(self, pattern):
        super(IncludeMatch, self).__init__()
        self.pattern_ = re.compile(pattern)

    def apply(self, input):
        match = self.pattern_.search(input)
        return bool(match), input
