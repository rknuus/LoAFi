# Copyright (C) 2021 R. Knaus

from LoAFi.filters import IncludeAll
from LoAFi.raw_file_access import RawFileAccess


class LogFileManager(object):
    """Manages the log file filtering workflow."""
    def __init__(self, logfile):
        super(LogFileManager, self).__init__()
        self.file_access_ = RawFileAccess(file=logfile)
        self.filters_ = []

    def list_filters(self):
        return ['IncludeAll']

    def add_filter(self, filter_type):
        assert filter_type == 'IncludeAll'
        self.filters_.append(IncludeAll())
        return len(self.filters_)

    def filter_lines(self):
        lines_or_nones = (self.filter_line_(line)
                          for line in self.file_access_.lines())
        return (line for line in lines_or_nones if line)

    def filter_line_(self, line):
        included_line = ''
        for filter in self.filters_:
            included_line = filter.apply(line)
            if included_line:
                return included_line
        return None
