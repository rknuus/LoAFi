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

    __parameters__ = {'pattern': 'A regular expression pattern to match lines. Currently outputs the entire line in case of a match. Required.'}

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


class SortByMatch(object):
    """Sorts the lines by a pattern which must contain exactly one group,
    by which the lines are sorted.

    Currently loads all lines into memory before sorting. One idea optimized
    for partially sorted input would be to use itertools.tee (if it returns
    generator expressions) to iterate over the input twice. The first time to
    store all sort pattern matches in sorted way, the second time to create a
    temporary container to hold all intermediate lines until the next one
    according to sorting order is found. Because the sort pattern matches are
    sorted we can calculate the distance between a too big element and the
    expected one to construct the temporary container.

    If the sorters and filters would be converted into plugins, we could offer
    a global strategy like optimize for memory consumption or for speed and
    use different file accesses and different filters."""

    __parameters__ = {'pattern': 'A regular expression pattern to match the sort key in a line, which must be unique. Required.'}

    def __init__(self, sort_pattern):
        super(SortByMatch, self).__init__()
        self.sort_pattern_ = re.compile(sort_pattern)

    def apply(self, lines):
        lines_by_group = dict()
        for line in lines:
            match = self.sort_pattern_.search(line)
            if not match:
                raise ValueError("Sort pattern '{}' doesn't match line '{}'.".format(self.sort_pattern_, line))
            if len(match.groups()) == 0 or len(match.groups()) > 1:
                raise ValueError("Sort pattern '{}' must contain exactly one group.".format(self.sort_pattern_))
            if match.group(1) in lines_by_group:
                raise ValueError("Sort key '{}' is not unique and appears in multiple lines: at least in '{}' and '{}'".format(match.group(1), lines_by_group[match.group(1)], line))
            lines_by_group[match.group(1)] = line
        return (lines_by_group[key] for key in sorted(lines_by_group.keys()))
