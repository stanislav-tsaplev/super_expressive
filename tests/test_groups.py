import pytest

from ..src import SuperExpressive, RegexError


def test_group():
    regex = r"(?:hello \w!)"
    se = (
        SuperExpressive()
        .group
            .string("hello ")
            .word
            .char('!')
        .end()
    )
    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_capture():
    regex = r"(hello \w!)"
    se = (
        SuperExpressive()
        .capture
            .string("hello ")
            .word
            .char('!')
        .end()
    )
    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_named_capture_error_on_bad_name():
    with pytest.raises(RegexError) as e:
        se = (
            SuperExpressive()
            .named_capture("hello world")
                .string("hello ")
                .word
                .char('!')
            .end()
        )
    assert str(e.value) == "name 'hello world' is not valid (only letters, numbers, and underscores)"


def test_named_capture_error_same_name_more_than_once():
    with pytest.raises(RegexError) as e:
        se = (
            SuperExpressive()
            .named_capture("hello")
                .string("hello ")
                .word
                .char('!')
            .end()
            .named_capture("hello")
                .string("hello ")
                .word
                .char('!')
            .end()
        )
    assert str(e.value) == "cannot use hello again for a capture group"


# XXX: this test uses a different regex syntax (Python, not JS)
def test_named_backreference():
    regex = r"(?P<this_is_the_name>hello \w!)(?P=this_is_the_name)"
    se = (
        SuperExpressive()
        .named_capture("this_is_the_name")
            .string("hello ")
            .word
            .char('!')
        .end()
        .named_backreference('this_is_the_name')
    )
    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_named_backreference_no_capture_group_exists():
    with pytest.raises(RegexError) as e:
        SuperExpressive().named_backreference("not_here")
    assert str(e.value) == "no capture group called 'not_here' exists (create one with .named_capture())"


def test_backreference():
    regex = r"(hello \w!)\1"
    se = (
        SuperExpressive()
        .capture
            .string("hello ")
            .word
            .char('!')
        .end()
        .backreference(1)
    )
    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_backreference_no_capture_group_exists():
    with pytest.raises(RegexError) as e:
        SuperExpressive().backreference(1)
    assert str(e.value) == "invalid index 1. There are 0 capture groups on this SuperExpression"

def test_assert_ahead():
    regex = r"(?=[a-f])[a-z]"
    se = (
        SuperExpressive()
        .assert_ahead
            .range('a', 'f')
        .end()
        .range('a', 'z')
    )
    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_assert_behind():
    regex = r"(?<=hello )[a-z]"
    se = (
        SuperExpressive()
        .assert_behind
            .string("hello ")
        .end()
        .range('a', 'z')
    )
    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_assert_not_ahead():
    regex = r"(?![a-f])[0-9]"
    se = (
        SuperExpressive()
        .assert_not_ahead
            .range('a', 'f')
        .end()
        .range('0', '9')
    )
    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_assert_not_behind():
    regex = r"(?<!hello )[a-z]"
    se = (
        SuperExpressive()
        .assert_not_behind
            .string("hello ")
        .end()
        .range('a', 'z')
    )
    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern
