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
    input = ['foo']
    manager = LogFileManager(logfile=None)
    output = list(manager.filter_lines_(input))
    assert len(output) == 0


def test_with_include_all_filter_all_lines_are_included():
    input = ['foo', 'bar']
    manager = LogFileManager(logfile=None)
    manager.add_filter('IncludeAll')
    lines = list(manager.filter_lines_(input))
    assert 'foo' in lines
    assert 'bar' in lines


def test_for_two_competing_filters_the_first_matching_one_wins():
    input = ['foo', 'bar']
    manager = LogFileManager(logfile=None)
    manager.add_filter('IncludeAll')
    manager.add_filter('ExcludeAll')
    matching_lines = list(manager.filter_lines_(input))

    manager = LogFileManager(logfile=None)
    manager.add_filter('ExcludeAll')
    manager.add_filter('IncludeAll')
    non_matching_lines = list(manager.filter_lines_(input))

    assert 'foo' in matching_lines
    assert 'bar' in matching_lines
    assert 'foo' not in non_matching_lines
    assert 'bar' not in non_matching_lines


def test_passing_parameter_to_parameterized_filter():
    input = ['foo', 'bar']
    manager = LogFileManager(logfile=None)
    manager.add_filter('IncludeMatch', '^foo$')
    lines = list(manager.filter_lines_(input))
    assert 'foo' in lines
    assert 'bar' not in lines


def test_add_sorter_returns_sorter_instance_id():
    manager = LogFileManager(logfile=None)
    instance_id = manager.add_sorter('SortByMatch', '')
    assert isinstance(instance_id, int)


def test_sorter_with_unsorted_lines_retursn_sorted_lines():
    input = ['3', '7', '2']
    expected = ['2', '3', '7']
    manager = LogFileManager(logfile=None)
    manager.add_sorter('SortByMatch', r'(\d)')
    output = manager.sort_lines_(input)
    assert list(output) == expected


def test_apply_if_no_filter_is_defined():
    input = []
    expected = []
    with generate_file('file.log', '\n'.join(input)) as file:
        manager = LogFileManager(logfile=file)
        output = manager.process_logfile()
        # convert to list inside with-block, otherwise the file gets closed
        # too early
        output = list(output)
    assert output == expected


def test_apply_if_one_filter_and_one_sorter_is_defined():
    input = ['2', 'foo', '3', '1', 'bar']
    expected = ['1', '2', '3']
    with generate_file('file.log', '\n'.join(input)) as file:
        manager = LogFileManager(logfile=file)
        manager.add_filter('IncludeMatch', r'^\d$')
        manager.add_sorter('SortByMatch', r'(\d)')
        output = manager.process_logfile()
        # convert to list inside with-block, otherwise the file gets closed
        # too early
        output = list(output)
    assert output == expected


# TEST LIST
# =========
# - test_add_unknown_sorter_type_raises_exception
# - test_without_any_sorter_line_order_doesnt_change
# - test_multiple_sorters_are_applied_sequentially
# - test_passing_parameter_to_parameterized_sorter
