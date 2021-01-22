# Copyright (C) 2021 R. Knaus

from LoAFi.filters import ExcludeAll, IncludeAll, IncludeMatch
from LoAFi.filters import SortByMatch
from LoAFi.raw_file_access import RawFileAccess

import LoAFi


class LogFileManager(object):
    """Manages the log file filtering workflow."""
    def __init__(self, logfile):
        super(LogFileManager, self).__init__()
        self.file_access_ = RawFileAccess(file=logfile)
        self.filters_ = []
        self.sorters_ = []

    def list_filters(self):
        """Returns a list of supported filters.

        Per filter the following information are returned:
        - the filter name serves as dict key
        - the docstring of the filter class explains the usage
        - an dict mapping parameter name to parameter help describes the
          expected parameters of the filter
        """
        # TODO(KNR): DRY
        return {ExcludeAll.__name__: {
                    'help': ExcludeAll.__doc__,
                    'parameters': ExcludeAll.__parameters__},
                IncludeAll.__name__: {
                    'help': IncludeAll.__doc__,
                    'parameters': IncludeAll.__parameters__},
                IncludeMatch.__name__: {
                    'help': IncludeMatch.__doc__,
                    'parameters': IncludeMatch.__parameters__}}

    def add_filter(self, filter_type, *parameters):
        if filter_type not in self.list_filters():
            raise ValueError('Filter type {} is unknown.'.format(filter_type))
        filter_class = getattr(LoAFi.filters, filter_type)
        self.filters_.append(filter_class(*parameters))
        return len(self.filters_)

    # Because sorters require all lines they are not compatible to the
    # interface of the filters.

    def list_sorters(self):
        """Returns a list of supported filters.

        Per filter the following information are returned:
        - the filter name serves as dict key
        - the docstring of the filter class explains the usage
        - an dict mapping parameter name to parameter help describes the
          expected parameters of the filter
        """
        return {SortByMatch.__name__: {
                    'help': SortByMatch.__doc__,
                    'parameters': SortByMatch.__parameters__}}

    def add_sorter(self, sorter_type, *parameters):
        if sorter_type not in self.list_sorters():
            raise ValueError('Sorter type {} is unknown.'.format(sorter_type))
        sorter_class = getattr(LoAFi.filters, sorter_type)
        self.sorters_.append(sorter_class(*parameters))
        return len(self.sorters_)

    def process_logfile(self):
        """First applies all registered filters, then all registered
        sorters and returns a generator expression with the result."""
        lines = self.filter_lines_(lines=self.file_access_.lines())
        lines = self.sort_lines_(lines=lines)
        return lines

    def filter_lines_(self, lines):
        filtered_lines_or_nones = (self.filter_line_(line)
                                   for line in lines)
        return (line for line in filtered_lines_or_nones if line)

    def filter_line_(self, line):
        for filter in self.filters_:
            matched, matched_line = filter.apply(line)
            if matched:
                return matched_line
        return None

    def sort_lines_(self, lines):
        for sorter in self.sorters_:
            lines = sorter.apply(lines)
        return lines
