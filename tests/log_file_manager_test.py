# Copyright (C) 2021 R. Knaus

from .context import LogFileManager
from contextlib import contextmanager
from os import path

import pytest
import tempfile


@contextmanager
def generate_file(file, content):
    with tempfile.TemporaryDirectory() as fixture_directory:
        with open(path.join(fixture_directory, file), 'w') as file:
            file_name = file.name
            file.write(content)
        yield file_name


def test_list_filters():
    manager = LogFileManager(logfile=None)
    filters = manager.list_filters()
    assert 'IncludeAll' in filters


def test_when_load_log_file_and_file_exists_can_access_file_content():
    with generate_file('file.log', 'foo') as file:
        manager = LogFileManager(logfile=file)
        assert next(line
                    for line in manager.file_access_.lines()
                    if line == 'foo')


def test_add_filter_returns_filter_instance_id():
    manager = LogFileManager(logfile=None)
    instance_id = manager.add_filter('IncludeAll')
    assert isinstance(instance_id, int)


def test_add_unknown_filter_type_raises_exception():
    manager = LogFileManager(logfile=None)
    with pytest.raises(ValueError) as exception:
        manager.add_filter('ANonExistingFilterType')
    assert ('Filter type ANonExistingFilterType is unknown.'
            in str(exception.value))


def test_without_any_filter_all_lines_are_excluded():
    with generate_file('file.log', 'foo') as file:
        manager = LogFileManager(logfile=file)
        lines = list(manager.filter_lines())
    assert len(lines) == 0


def test_with_include_all_filter_all_lines_are_included():
    with generate_file('file.log', 'foo\nbar') as file:
        manager = LogFileManager(logfile=file)
        manager.add_filter('IncludeAll')
        lines = list(manager.filter_lines())
    assert 'foo' in lines
    assert 'bar' in lines


def test_for_two_competing_filters_the_first_matching_one_wins():
    with generate_file('file.log', 'foo\nbar') as file:
        manager = LogFileManager(logfile=file)
        manager.add_filter('IncludeAll')
        manager.add_filter('ExcludeAll')
        matching_lines = list(manager.filter_lines())

        manager = LogFileManager(logfile=file)
        manager.add_filter('ExcludeAll')
        manager.add_filter('IncludeAll')
        non_matching_lines = list(manager.filter_lines())
    assert 'foo' in matching_lines
    assert 'bar' in matching_lines
    assert 'foo' not in non_matching_lines
    assert 'bar' not in non_matching_lines
