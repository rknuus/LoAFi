# Copyright (C) 2021 R. Knaus

from .context import IncludeMatch


def test_without_substitution_a_match_returns_entire_line():
    filter = IncludeMatch(pattern='foo')
    matched, matched_line = filter.apply(input='bar foo baz')
    assert matched
    assert matched_line == 'bar foo baz'


def test_with_string_substitution_a_match_returns_exact_string():
    filter = IncludeMatch(pattern='foo', substitution='moo')
    matched, matched_line = filter.apply(input='bar foo baz')
    assert matched
    assert matched_line == 'moo'


def test_with_backreference_substitution_a_match_returns_matched_groups():
    filter = IncludeMatch(pattern='(.*) foo (.*)', substitution='moo: \\1 \\2')
    matched, matched_line = filter.apply(input='bar foo baz')
    assert matched
    assert matched_line == 'moo: bar baz'


def test_substitution_without_backreferences_but_a_match_with_groups():
    filter = IncludeMatch(pattern='(.*) foo', substitution='moo moo moo')
    matched, matched_line = filter.apply(input='bar foo baz')
    assert matched
    assert matched_line == 'moo moo moo'
