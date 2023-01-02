import pytest

from ..src.super_expressive import SuperExpressive, RegexError


def test_any_of_chars():
    regex = r"[aeiou\.\-]"
    se = SuperExpressive().any_of_chars("aeiou.-")

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_any_of_chars_special_characters():
    regex = r"[\[\]\\\^]"
    se = SuperExpressive().any_of_chars(r"[]\^")

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_anything_but_chars():
    regex = r"[^aeiou\.\-]"
    se = SuperExpressive().anything_but_chars("aeiou.-")

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern

    
def test_range():
    regex = r"[a-z]"
    se = SuperExpressive().range('a', 'z')

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_any_of_basic():
    regex = r"(?:hello|\d|\w|[\.#])"
    se = (
        SuperExpressive()
        .any_of
            .string("hello")
            .digit
            .word
            .char('.')
            .char('#')
        .end()
    )
    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_any_of_range_fusion():
    regex = r"[a-zA-Z0-9\.#]"
    se = (
        SuperExpressive()
        .any_of
            .range('a', 'z')
            .range('A', 'Z')
            .range('0', '9')
            .char('.')
            .char('#')
        .end()
    )
    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_any_of_range_fusion_with_other_choices():
    regex = r"(?:XXX|[a-zA-Z0-9\.#])"
    se = (
        SuperExpressive()
        .any_of
            .range('a', 'z')
            .range('A', 'Z')
            .range('0', '9')
            .char('.')
            .char('#')
            .string("XXX")
        .end()
    )
    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_anything_but_range():
    regex = r"[^0-9]"
    se = SuperExpressive().anything_but_range('0', '9')

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_anything_but_string():
    regex = r"(?:(?!hello).{5})"
    se = SuperExpressive().anything_but_string("hello")

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_anything_but_string_not_ascii():
    regex = r"(?:(?!привет).{6})"
    se = SuperExpressive().anything_but_string("привет")

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern
