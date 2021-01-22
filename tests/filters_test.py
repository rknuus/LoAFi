# Copyright (C) 2021 R. Knaus

from .context import IncludeMatch, SortByMatch

import pytest


def test_IncludeMatch_without_substitution_a_match_returns_entire_line():
    filter = IncludeMatch(pattern='foo')
    matched, matched_line = filter.apply(input='bar foo baz')
    assert matched
    assert matched_line == 'bar foo baz'


def test_IncludeMatch_with_substitution_a_match_returns_exact_string():
    filter = IncludeMatch(pattern='foo', substitution='moo')
    matched, matched_line = filter.apply(input='bar foo baz')
    assert matched
    assert matched_line == 'moo'


def test_IncludeMatch_with_backreference_a_match_returns_matched_groups():
    filter = IncludeMatch(pattern='(.*) foo (.*)', substitution='moo: \\1 \\2')
    matched, matched_line = filter.apply(input='bar foo baz')
    assert matched
    assert matched_line == 'moo: bar baz'


def test_IncludeMatch_without_backreferences_but_a_match_with_groups():
    filter = IncludeMatch(pattern='(.*) foo', substitution='moo moo moo')
    matched, matched_line = filter.apply(input='bar foo baz')
    assert matched
    assert matched_line == 'moo moo moo'


def test_SortByMatch_fails_if_no_match():
    sorter = SortByMatch(r'\d+')
    with pytest.raises(ValueError) as exception:
        sorter.apply(['foo'])
    assert (r"Sort pattern 're.compile('\\d+')' doesn't match line 'foo'."
            in str(exception.value))


def test_SortByMatch_fails_without_group():
    sorter = SortByMatch(r'\d+')
    with pytest.raises(ValueError) as exception:
        sorter.apply(['1'])
    assert (r"Sort pattern 're.compile('\\d+')' must contain exactly one group."
            in str(exception.value))


def test_SortByMatch_fails_with_more_than_one_group():
    sorter = SortByMatch(r'(\d)(\d*)')
    with pytest.raises(ValueError) as exception:
        sorter.apply(['1'])
    assert (r"Sort pattern 're.compile('(\\d)(\\d*)')' must contain exactly one group."
            in str(exception.value))


def test_SortByMatch_for_sorted_input_returns_same_output():
    sorter = SortByMatch(r'(\d)')
    input = ['1', '2', '3']
    expected = input
    output = sorter.apply(input)
    assert list(output) == expected


def test_SortByMatch_for_unsorted_input_returns_sorted_output():
    sorter = SortByMatch(r'(\d)')
    input = ['1', '2', '3']
    expected = input
    output = sorter.apply(input)
    assert list(output) == expected


def test_SortByMatch_fails_if_key_is_not_unique():
    sorter = SortByMatch(r'(\d)')
    with pytest.raises(ValueError) as exception:
        sorter.apply(['1', '1'])
    assert (r"Sort key '1' is not unique and appears in multiple lines"
            in str(exception.value))
