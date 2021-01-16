# Copyright (C) 2021 R. Knaus

from .context import LogFileManager
from contextlib import contextmanager
from os import path

import tempfile


@contextmanager
def generate_file(file, content):
    with tempfile.TemporaryDirectory() as fixture_directory:
        with open(path.join(fixture_directory, file), 'w') as file:
            file_name = file.name
            file.write(content)
        yield file_name


def test_when_load_log_file_and_file_exists_can_access_file_content():
    with generate_file('file.log', 'foo') as file:
        manager = LogFileManager(logfile=file)
        assert next(line
                    for line in manager.file_access_.lines()
                    if line == 'foo')
