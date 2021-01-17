# Copyright (C) 2021 R. Knaus

from LoAFi.filters import ExcludeAll, IncludeAll
from LoAFi.raw_file_access import RawFileAccess

import LoAFi


class LogFileManager(object):
    """Manages the log file filtering workflow."""
    def __init__(self, logfile):
        super(LogFileManager, self).__init__()
        self.file_access_ = RawFileAccess(file=logfile)
        self.filters_ = []

    def list_filters(self):
        """Returns a list of supported filters.

        Per filter the following information are returned:
        - the filter name serves as dict key
        - the docstring of the filter class explains the usage
        - an array of parameter name and parameter help pairs
          describe the expected parameters of the filter
        """
        return {ExcludeAll.__name__: {
                    'help': ExcludeAll.__doc__,
                    'parameters': ExcludeAll.__parameters__},
                IncludeAll.__name__: {
                    'help': IncludeAll.__doc__,
                    'parameters': IncludeAll.__parameters__}}

    def add_filter(self, filter_type):
        if filter_type not in self.list_filters():
            raise ValueError('Filter type {} is unknown.'.format(filter_type))
        filter_class = getattr(LoAFi.filters, filter_type)
        self.filters_.append(filter_class())
        return len(self.filters_)

    def filter_lines(self):
        filtered_lines_or_nones = (self.filter_line_(line)
                                   for line in self.file_access_.lines())
        return (line for line in filtered_lines_or_nones if line)

    def filter_line_(self, line):
        for filter in self.filters_:
            matched, matched_line = filter.apply(line)
            if matched:
                return matched_line
        return None
