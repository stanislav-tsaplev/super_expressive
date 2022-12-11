import pytest

from main import SuperExpressive, RegexError


def test_char():
    regex = r"h"
    se = SuperExpressive().char('h')

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_char_more_than_one():
    with pytest.raises(RegexError) as e:
        SuperExpressive().char('hello')
    assert str(e.value) == "char() can only be called with a single character (got hello)"


def test_string():
    regex = r"hello"
    se = SuperExpressive().string("hello")

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_escaping_special_characters():
    regex = r"\^hello\$"
    se = SuperExpressive().char('^').string("hello").string('$')

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_start_of_string():
    regex = r"\A"
    se = SuperExpressive().start_of_string

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_end_of_string():
    regex = r"\Z"
    se = SuperExpressive().end_of_string

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_start_of_input():
    regex = r"^"
    se = SuperExpressive().start_of_input

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_end_of_input():
    regex = r"$"
    se = SuperExpressive().end_of_input

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_end_error_when_called_with_no_stack():
    with pytest.raises(RegexError) as e:
        SuperExpressive().end()
    assert str(e.value) == "Cannot call end while building the root expression"
