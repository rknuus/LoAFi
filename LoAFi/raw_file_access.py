# Copyright (C) 2021 R. Knaus


class RawFileAccess(object):
    """docstring for RawFileAccess"""
    def __init__(self, file):
        super(RawFileAccess, self).__init__()
        self.file_ = file

    def lines(self):
        """Returns a generator to iterate over all lines.

        Currently we don't cache the lines, because right now speed is not our
        main concern and keeping the entire file in memory might consume too
        much memory.
        """
        with open(self.file_) as file:
            for line in file:
                yield line
