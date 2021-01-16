# Copyright (C) 2021 R. Knaus

from LoAFi.raw_file_access import RawFileAccess


class LogFileManager(object):
    """Manages the log file filtering workflow."""
    def __init__(self, logfile):
        super(LogFileManager, self).__init__()
        self.file_access_ = RawFileAccess(file=logfile)
