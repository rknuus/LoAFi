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

    def __init__(self, pattern, substitution=None):
        super(IncludeMatch, self).__init__()
        self.pattern_ = re.compile(pattern)
        self.substitution_ = substitution

    def apply(self, input):
        match = self.pattern_.search(input)

        output = input

        # NOTSURE(KNR): If a pattern contains groups but the substitution
        # doesn't contain backreferences, the right thing seems to happen,
        # namely that the input is replaced by the substitution.
        #
        # It's unclear to me, why this doesn't work if no groups are involved,
        # though.
        if self.substitution_ and len(match.groups()) > 1:
            output = self.pattern_.sub(self.substitution_, input)
        elif self.substitution_:
            output = self.substitution_

        return bool(match), output
